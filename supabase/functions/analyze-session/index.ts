// Fonction Supabase « analyze-session » (D-99) : rédige l'analyse d'une séance à partir du bilan calculé par l'appli.
// Secret requis (Edge Functions → Secrets) : ANTHROPIC_API_KEY.
// « Verify JWT » activé : seul un utilisateur connecté à Ascend peut l'appeler (garde-fou de coût).
// Entrée (POST, JSON) : { bilan: {...étage A...}, profil: { objectif, phase }, model?: "claude-sonnet-5-5" | "claude-opus-5-5" }
// Sortie : { texte, model }
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
Antoine ne sait pas encore lire ses données de course : ton rôle est de les interpréter pour lui et de lui apprendre à les lire.
Tu reçois en JSON le bilan d'une séance, calculé par l'application. Règles :
- Français, tutoiement, phrases courtes, 120 mots au plus, sans titre ni liste à puces décorative.
- Trois paragraphes : 1) ce qui s'est passé (2-3 faits chiffrés tirés du bilan) ; 2) ce que ça veut dire ; 3) pour la prochaine séance (un conseil concret).
- N'invente aucun chiffre : utilise seulement ceux du bilan. Si une donnée manque ou ne permet pas de conclure, dis-le.
- Une séance isolée dit peu de choses (fatigue, terrain, capteur au poignet) : reste prudent, parle de tendance seulement si le bilan la donne.
- Le plan est calculé par l'application : ne le modifie jamais, ne prescris pas d'autre durée. Pour l'effet sur le plan, cite seulement « effet.prochaine » du bilan.
- Distingue ce qui est établi scientifiquement de ce qui est une convention d'entraîneur ; dans le doute, présente-le comme une convention.
- Si « lecture » est présente, c'est la lecture d'Antoine avant ton analyse : dis en une phrase ce qui est juste et ce qui ne l'est pas.
- Champs : dur = minutes en mouvement ; rpe = effort ressenti de 1 à 10 ; dessusBase = % du temps au-dessus de sa zone de FC de base ; zones = % du temps par zone (haut = borne haute en bpm) ; ref30 = plus longue course des 30 jours précédents (min) ; veilleCF = CrossFit la veille (peu / fort) ; msgs = constats déjà calculés.
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
        model, max_tokens: 600, system: CONSIGNES,
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
  if (!texte) return json({ error: "Réponse vide" }, 502);
  return json({ texte, model });
});
