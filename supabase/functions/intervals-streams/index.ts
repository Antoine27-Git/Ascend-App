// Fonction Supabase « intervals-streams » (lecture seule, D-100).
// Rôle : relayer les données seconde par seconde d'UNE activité d'intervals.icu (temps, FC, distance, altitude) vers Ascend.
// Jamais la position GPS : le type « latlng » n'est ni demandé ni renvoyé.
// Secret requis : INTERVALS_API_KEY (le même que pour intervals-activities). « Verify JWT » reste activé.
// Entrée  (POST, JSON) : { "id": "i12345678" }  (identifiant intervals.icu de l'activité)
// Sortie  : { "time": [s], "hr": [bpm], "dist": [m], "alt": [m], "altSource": "fixed_altitude" | "altitude" | null }

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });

const ID = /^[A-Za-z0-9_-]{1,40}$/;
const TYPES = ["time", "heartrate", "distance", "altitude", "fixed_altitude"]; // pas de latlng

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST attendu" }, 405);
  const key = Deno.env.get("INTERVALS_API_KEY");
  if (!key) return json({ error: "Secret INTERVALS_API_KEY absent" }, 500);

  let body: { id?: string } = {};
  try { body = await req.json(); } catch { return json({ error: "JSON invalide" }, 400); }
  const id = String(body.id ?? "").replace(/^icu:/, "");
  if (!ID.test(id)) return json({ error: "Identifiant d'activité invalide" }, 400);

  let r: Response;
  try {
    r = await fetch(`https://intervals.icu/api/v1/activity/${id}/streams.json?types=${TYPES.join(",")}`, {
      headers: { Authorization: "Basic " + btoa("API_KEY:" + key), Accept: "application/json", "User-Agent": "ascend-sync" },
    });
  } catch {
    return json({ error: "intervals.icu injoignable" }, 502);
  }
  if (r.status === 401 || r.status === 403) return json({ error: "Clé d'API refusée par intervals.icu" }, 502);
  if (r.status === 404) return json({ error: "Activité introuvable dans intervals.icu" }, 404);
  if (!r.ok) return json({ error: "intervals.icu a répondu " + r.status }, 502);

  const raw = await r.json();
  const list: { type?: string; data?: unknown[] }[] = Array.isArray(raw) ? raw : [];
  const get = (t: string) => {
    const s = list.find((x) => x && x.type === t);
    return s && Array.isArray(s.data) ? s.data.map((v) => (typeof v === "number" && isFinite(v) ? v : null)) : null;
  };
  const time = get("time"), hr = get("heartrate");
  if (!time || !hr) return json({ error: "Pas de FC seconde par seconde pour cette activité" }, 422);
  const fixed = get("fixed_altitude"), alt = fixed ?? get("altitude");
  const r1 = (a: (number | null)[] | null) => (a ? a.map((v) => (v == null ? null : Math.round(v * 10) / 10)) : null);
  return json({ time, hr, dist: r1(get("distance")), alt: r1(alt), altSource: fixed ? "fixed_altitude" : alt ? "altitude" : null });
});
