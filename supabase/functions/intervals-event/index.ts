// Fonction Supabase « intervals-event » : envoie (ou retire) UNE séance prévue dans le calendrier intervals.icu.
// intervals.icu la transmet ensuite à Garmin Connect, puis à la montre (si « Envoyer les entraînements planifiés » est coché).
// Secret requis : INTERVALS_API_KEY (le même que pour intervals-activities). « Verify JWT » reste activé.
// Entrée (POST, JSON) :
//   { "action": "send",   "external_id": "ascend:<id>", "date": "AAAA-MM-JJ", "name": "…", "description": "<séance en texte intervals.icu>" }
//   { "action": "remove", "external_id": "ascend:<id>", "date": "AAAA-MM-JJ" }
// Sortie : { ok: true, result: "created" | "updated" | "removed" | "absent", id }
// Garde-fous : seuls les événements dont l'identifiant externe commence par « ascend: » sont créés, modifiés ou supprimés ;
// date entre hier et dans 60 jours ; texte limité à 4000 caractères.

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });
const DAY = /^\d{4}-\d{2}-\d{2}$/;
const BASE = "https://intervals.icu/api/v1/athlete/0";

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST attendu" }, 405);
  const key = Deno.env.get("INTERVALS_API_KEY");
  if (!key) return json({ error: "Secret INTERVALS_API_KEY absent" }, 500);

  let b: { action?: string; external_id?: string; date?: string; name?: string; description?: string } = {};
  try { b = await req.json(); } catch { return json({ error: "JSON invalide" }, 400); }
  const ext = String(b.external_id || "");
  if (!/^ascend:[\w.\-]{1,70}$/.test(ext)) return json({ error: "external_id invalide" }, 400);
  if (!b.date || !DAY.test(b.date)) return json({ error: "date invalide" }, 400);
  const days = (Date.parse(b.date) - Date.parse(new Date().toISOString().slice(0, 10))) / 864e5;
  if (!(days >= -1 && days <= 60)) return json({ error: "date hors de la fenêtre (hier à +60 jours)" }, 400);
  if (b.action !== "send" && b.action !== "remove") return json({ error: "action inconnue" }, 400);

  const H = {
    Authorization: "Basic " + btoa("API_KEY:" + key),
    Accept: "application/json",
    "Content-Type": "application/json",
    "User-Agent": "ascend-sync",
  };
  const call = async (method: string, path: string, body?: unknown) => {
    const r = await fetch(BASE + path, { method, headers: H, body: body ? JSON.stringify(body) : undefined });
    const txt = await r.text();
    let data: unknown = null;
    try { data = txt ? JSON.parse(txt) : null; } catch { data = txt; }
    return { ok: r.ok, status: r.status, data };
  };
  const fail = (r: { status: number; data: unknown }) =>
    json({ error: "intervals.icu a répondu " + r.status, detail: typeof r.data === "string" ? r.data.slice(0, 300) : r.data }, 502);

  // Événement déjà envoyé pour cet identifiant ?
  const list = await call("GET", `/events?oldest=${b.date}&newest=${b.date}&category=WORKOUT`);
  if (!list.ok) return fail(list);
  const found = Array.isArray(list.data) ? (list.data as Record<string, unknown>[]).find((e) => e.external_id === ext) : null;

  if (b.action === "remove") {
    if (!found) return json({ ok: true, result: "absent" });
    const d = await call("DELETE", `/events/${found.id}`);
    return d.ok ? json({ ok: true, result: "removed", id: found.id }) : fail(d);
  }

  const description = String(b.description || "").slice(0, 4000);
  const event = {
    category: "WORKOUT",
    start_date_local: b.date + "T00:00:00",
    type: "Run",
    name: String(b.name || "Séance Ascend").slice(0, 120),
    description,
    external_id: ext,
  };
  const w = found ? await call("PUT", `/events/${found.id}`, event) : await call("POST", "/events", event);
  if (!w.ok) return fail(w);
  const id = (w.data as Record<string, unknown> | null)?.id ?? found?.id ?? null;
  return json({ ok: true, result: found ? "updated" : "created", id });
});
