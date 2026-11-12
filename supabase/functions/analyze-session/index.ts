// Fonction Supabase « analyze-session » (D-99) : rédige l'analyse d'une séance à partir du bilan calculé par l'appli.
// Secret requis (Edge Functions → Secrets) : ANTHROPIC_API_KEY.
// « Verify JWT » activé : seul un utilisateur connecté à Ascend peut l'appeler (garde-fou de coût).
// Entrée (POST, JSON) : { bilan: {...étage A...}, profil: { objectif, phase }, model?: "claude-sonnet-5-5" | "claude-opus-5-5" }
// Sortie : { interpretation, conseil, texte, model } (texte = repli si la réponse n'est pas du JSON)
// Le LLM ne reçoit que des chiffres déjà calculés (pas de trace, pas de lieu) et ne modifie jamais le plan.

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });

const MODELES = ["claude-sonnet-5-5", "claude-opus-5-5"];

const CONSIGNES = `Tu es le coach d'Antoine dans l'application Ascend (préparation d'un trail d'environ 80 km et 3 000 à 6 000 m de D+).
Antoine voit déjà à l'écran tous les chiffres du bilan (tableaux, constats). Ton rôle n'est PAS de les répéter : c'est de relier les données entre elles pour expliquer POURQUOI la séance s'est passée ainsi, puis d'en tirer un conseil.
Tu reçois en JSON le bilan d'une séance, calculé par l'application. Réponds UNIQUEMENT par un objet JSON, sans texte autour :
{"interpretation": "...", "conseil": "..."}
- interpretation : 2 à 3 phrases, 60 mots au plus. Relie au moins deux éléments (ex. : terrain et FC, départ et FC stabilisée, dérive et durée, CrossFit la veille et ressenti). Un chiffre seulement s'il appuie un lien.
- conseil : 1 à 2 phrases, 40 mots au plus, concret et applicable à la prochaine séance du même type (allure, FC à viser, gestion des montées, ravitaillement, technique). Ne change jamais la durée ni le D+ prévus par le plan.
- Français, tutoiement, phrases courtes, pas de markdown.
- N'invente aucun chiffre ni aucune règle : utilise seulement ceux du bilan. Si les données ne permettent pas de conclure, dis-le.
- Une séance isolée dit peu de choses (fatigue, terrain, capteur au poignet) : reste prudent.
- Ce qui n'est pas établi scientifiquement (seuils, marche en montée, etc.) se présente comme une habitude d'entraîneur, pas comme une règle.
- Si « lecture » est présente, c'est la lecture d'Antoine avant ton analyse : commence l'interprétation en disant en quelques mots ce qui est juste ou non.
- Champs : dur = minutes en mouvement ; rpe = effort ressenti de 1 à 10 ; hautBase = haut de sa zone facile (bpm) ; dessusBase = % du temps au-dessus ; veilleCF = CrossFit la veille ; msgs = constats déjà affichés ; effet.prochaine = prochaine sortie longue prévue.
- flux (données seconde par seconde) : croisiere = FC stabilisée après 10 min (fc), départ (depart), temps pour l'atteindre (montee_s) ; terrain = montee (> +3 %), fpm (faux plat montant +1 à +3 %), plat, fpd (faux plat descendant), descente (< −3 %), chacun {min, allure en s/km, eq = allure équivalente plat en s/km (Minetti, absente en descente), fc} ; vam = mètres montés par heure en montée ; tranches = par km (ou 5 km) {allure s/km, fc, dp, dm} ; derive = 1re contre 2e moitié hors départ et descentes {fc1, fc2, eq1, eq2, pct} (pct > 5 : efficacité en baisse ; FC qui monte = dérive cardiaque, FC qui baisse = fatigue des jambes).
- Pas de conseil médical : en cas de douleur signalée, renvoie vers un professionnel.`;

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST attendu" }, 405);
  const key = Deno.env.get("ANTHROPIC_API_KEY");
  if (!key) return json({ error: "Secret ANTHROPIC_API_KEY absent" }, 500);

  let body: { bilan?: unknown; profil?: unknown; model?: string } = {};
  try { body = await req.json(); } catch { return json({ error: "JSON invalide" }, 400); }
  if (!body.bilan || typeof body.bilan !== "object") return json({ error: "Bilan manquant" }, 400);
  const data = JSON.stringify({ bilan: body.bilan, profil: body.profil ?? null });
  if (data.length > 20000) return json({ error: "Bilan trop volumineux" }, 413);
  const model = MODELES.includes(String(body.model)) ? String(body.model) : MODELES[0];

  let r: Response;
  try {
    r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json" },
      body: JSON.stringify({
        model, max_tokens: 2500, system: CONSIGNES,
        messages: [{ role: "user", content: "Bilan de la séance (JSON) :\n" + data }],
      }),
    });
  } catch {
    return json({ error: "Service d'analyse injoignable" }, 502);
  }
  if (!r.ok) {
    let detail = "";
    try { detail = (await r.json())?.error?.message ?? ""; } catch { /* rien */ }
    return json({ error: "Le service d'analyse a répondu " + r.status, detail }, 502);
  }
  const out = await r.json();
  const texte = Array.isArray(out?.content) ? out.content.filter((c: { type: string }) => c.type === "text").map((c: { text: string }) => c.text).join("\n").trim() : "";
  if (!texte) {
    const types = Array.isArray(out?.content) ? out.content.map((c: { type: string }) => c.type).join(", ") : "aucun";
    return json({ error: "Réponse vide", detail: "arrêt : " + (out?.stop_reason ?? "?") + " · blocs : " + types }, 502);
  }
  let interpretation = "", conseil = "";
  try {
    const m = texte.match(/\{[\s\S]*\}/);
    const o = m ? JSON.parse(m[0]) : null;
    interpretation = String(o?.interpretation ?? "").trim();
    conseil = String(o?.conseil ?? "").trim();
  } catch { /* repli sur le texte brut */ }
  return json({ interpretation, conseil, texte: interpretation || conseil ? "" : texte, model });
});
