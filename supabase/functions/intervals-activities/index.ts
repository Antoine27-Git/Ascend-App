// Fonction Supabase « intervals-activities » (lecture seule).
// Rôle : relayer la liste des activités d'intervals.icu vers Ascend, sans jamais exposer la clé d'API.
// Secret requis (Edge Functions → Secrets) : INTERVALS_API_KEY.
// « Verify JWT » reste activé : seul un utilisateur connecté à Ascend peut l'appeler.
// Entrée  (POST, JSON) : { "oldest": "AAAA-MM-JJ", "newest": "AAAA-MM-JJ" }  (400 jours maximum)
// Sortie  : { "activities": [ { id, date, name, type, dur_s, dist_m, dplus, hr_avg, hr_max } ] }
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
