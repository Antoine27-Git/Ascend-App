# tests/audit — scripts de l'audit de novembre 2026

Scripts de simulation et cas reproductibles produits par l'audit (rapports dans `docs/audit/`).
Ils ne modifient pas le moteur. Ils ne sont **pas** dans `tools/test.py`, sauf mention contraire :
certains reproduisent un défaut connu et sont donc rouges tant que le défaut existe.

| Fichier | Rôle | Vert sur main ? |
|---|---|---|
| `sim_adherence.js` | mission 1 : rejoue le moteur semaine après semaine avec des semaines perdues au hasard | sans objet (mesure) |
| `sim_coupure.js` | mission 1 : une coupure totale de k semaines placée à chaque semaine | sans objet (mesure) |
| `variante.js` | charge une copie du moteur avec une constante interne changée, pour chiffrer une proposition | sans objet (outil) |
| `t_audit_heure_ete.js` | numéro de semaine faux le lundi en heure d'été | **rouge attendu** |

Reproduire la mission 1 (environ 30 min sur 2 cœurs, graine fixe) :
`node tests/audit/sim_adherence.js 400 1 "" 0/2` et `… 1/2`, puis `node tests/audit/sim_coupure.js "2 jours"`.
Résultats de référence : `docs/audit/data/01-adherence.json`.
