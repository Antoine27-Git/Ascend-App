// Fonction Supabase « intervals-activities » (lecture seule).
// Rôle : relayer la liste des activités d'intervals.icu vers Ascend, sans jamais exposer la clé d'API.
// Secret requis (Edge Functions → Secrets) : INTERVALS_API_KEY.
// « Verify JWT » reste activé : seul un utilisateur connecté à Ascend peut l'appeler.
// Entrée  (POST, JSON) : { "oldest": "AAAA-MM-JJ", "newest": "AAAA-MM-JJ" }  (400 jours maximum)
// Sortie  : { "activities": [ { id, date, name, type, dur_s, dist_m, dplus, hr_avg, hr_max, device } ] }
// Seules les activités sont lues : aucune donnée de santé (sommeil, VFC, poids…) ne transite ici.

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });

const DAY = /^\d{4}-\d{2}-\d{2}$/;
const num = (v: unknown) => (typeof v === "number" && isFinite(v) ? v : null);

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST attendu" }, 405);

  const key = Deno.env.get("INTERVALS_API_KEY");
  if (!key) return json({ error: "Secret INTERVALS_API_KEY absent" }, 500);

  let body: { oldest?: string; newest?: string } = {};
  try { body = await req.json(); } catch { /* corps vide : valeurs par défaut ci-dessous */ }
  const today = new Date().toISOString().slice(0, 10);
  const newest = body.newest && DAY.test(body.newest) ? body.newest : today;
  const oldest = body.oldest && DAY.test(body.oldest)
    ? body.oldest
    : new Date(Date.now() - 7 * 864e5).toISOString().slice(0, 10);
  const span = (Date.parse(newest) - Date.parse(oldest)) / 864e5;
  if (!(span >= 0 && span <= 400)) return json({ error: "Période invalide (400 jours maximum)" }, 400);

  // Athlète « 0 » = le propriétaire de la clé d'API.
  const url = `https://intervals.icu/api/v1/athlete/0/activities?oldest=${oldest}&newest=${newest}`;
  let r: Response;
  try {
    r = await fetch(url, {
      headers: {
        Authorization: "Basic " + btoa("API_KEY:" + key),
        Accept: "application/json",
        "User-Agent": "ascend-sync",
      },
    });
  } catch {
    return json({ error: "intervals.icu injoignable" }, 502);
  }
  if (r.status === 401 || r.status === 403) return json({ error: "Clé d'API refusée par intervals.icu" }, 502);
  if (!r.ok) return json({ error: "intervals.icu a répondu " + r.status }, 502);

  const raw = await r.json();
  const list = Array.isArray(raw) ? raw : [];
  const activities = list
    .filter((a) => a && a.id != null && num(a.moving_time) && a.moving_time > 0) // ignore les activités vides (ex. Strava non lisibles)
    .map((a) => ({
      id: String(a.id),
      date: String(a.start_date_local || "").slice(0, 10),
      name: typeof a.name === "string" ? a.name : "",
      type: typeof a.type === "string" ? a.type : "",
      dur_s: num(a.moving_time),
      dist_m: num(a.distance),
      dplus: num(a.total_elevation_gain),
      hr_avg: num(a.average_heartrate),
      hr_max: num(a.max_heartrate),
      device: typeof a.device_name === "string" ? a.device_name : "", // modèle de montre (D-86)
    }));
  return json({ activities });
});
