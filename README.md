**G = 1234** *(valeur par défaut — à remplacer : renseigner `NUMEROS_INSCRIPTION` dans `config.py`, G = somme mod 10 000)*

# Médina 2.0 — moteur algorithmique (1CINFO1, Algorithm Engineering & Problem Solving)

Groupe : *(noms des membres)*

## Installation
```
python3 -m pip install -r requirements.txt     # seule dépendance : matplotlib
```

## Lancement
| Commande | Effet |
|---|---|
| `python main.py` | journée complète sans interaction (Parties 1 à 5) |
| `python main.py jouer` | partie de Kharbga humain contre IA (soutenance) ; coup = `l1 c1 l2 c2` |
| `python main.py carte` | affiche la Médina |
| `python tests.py` | 29 tests (Pile, File, labyrinthe, recherches, TSP, CSP, Kharbga…) |
| `python experiences.py` | régénère `journal_experiences.md` et `figures/` (parties 1 à 5) |
| `python experiences.py bonus` | bonus Branch and Bound vs Held-Karp |

## Organisation du code
| Fichier | Contenu | Questions |
|---|---|---|
| `config.py` | graine G, k, les 12 points d'intérêt | — |
| `structures.py` | `Pile`, `File` (deux piles) | Q1-Q2 |
| `medina.py` | `Medina` : DFS, `ouvrir_passages`, `voisins`, `cout`, `afficher` | Q3-Q5 |
| `recherche.py` | BFS, DFS, coût uniforme, A*, glouton, 4 heuristiques | Q6-Q11 |
| `tsp.py` | matrice, plus proche voisin, Held-Karp, 2-opt, recuit, AG (OX), Branch & Bound | Q12-Q18, bonus |
| `csp.py` | `CSP`, backtracking (MRV, FC), AC-3, problème du souk | Q19-Q23 |
| `kharbga.py` | moteur de jeu (état immuable) | Q24 |
| `jeu_ia.py` | Minimax, alpha-bêta, `eval_1`/`eval_2`, tournoi, boucle humain-IA | Q25-Q29 |
| `tests.py` | tests | — |
| `experiences.py` | produit tous les tableaux/courbes du journal | Q6-Q28 |
| `ANALYSES.md` | réponses rédigées aux questions « Analyse » | — |

## Reproductibilité (ordre imposé des tirages)
`Medina.__init__` crée `rng = random.Random(G)` ; `generer_dfs()` tire la case de départ avec
`(rng.randrange(P), rng.randrange(Q))`, examine les voisines dans l'ordre N, S, E, O et choisit avec
`rng.choice` ; `ouvrir_passages(k)` liste les murs ligne par ligne / colonne par colonne (est puis sud)
et tire avec `rng.sample(murs, k)` **avec le même `rng`**. Les escaliers utilisent un **second**
`random.Random(G)`.

## Conventions
- Chemin = liste de cases `[(l, c), …]` ; tournée = liste d'indices commençant par 0, sans répéter 0.
- Fonctions de recherche : `(chemin, cout, nb_explores)` ; `nb_explores` = cases retirées de la frontière
  (paramètre optionnel `trace=` pour récupérer la liste des cases développées).
- CSP : `noeuds` = états visités (appels récursifs), `retours` = affectations défaites sans solution dessous.
