# Journal d'expériences — Médina 2.0

Graine G = 7952  ·  k = 99

> Tableaux et courbes générés automatiquement par `experiences.py`. Voir `ANALYSES.md` pour les interprétations.

## Partie 1 — La carte

- Graine G = 7952, k = 60 + (G mod 41) = 99
- Passages du labyrinthe parfait : 599 (attendu P×Q−1 = 599)
- Passages après ouverture : 698 (= 599 + 99)
- Escaliers : 28 cases

![carte](figures/carte.png)

## Partie 2 — Le touriste perdu

### Q6b — Contre-exemples BFS (pas minimal ≠ coût minimal)

53 paires de points d'intérêt sur 132 où BFS est strictement plus cher que le coût uniforme. Exemples :

| trajet | BFS : pas | BFS : coût | UCS : pas | UCS : coût |
|---|---|---|---|---|
| 0→1 | 24 | 29 | 24 | 27 |
| 0→2 | 22 | 30 | 22 | 29 |
| 0→3 | 31 | 39 | 31 | 38 |
| 0→4 | 19 | 21 | 19 | 20 |
| 0→5 | 20 | 22 | 20 | 21 |

### Q7 — DFS vs BFS : labyrinthe parfait (k=0) vs Médina (k>0)

| carte | trajet | pas BFS | pas DFS | coût BFS | coût DFS |
|---|---|---|---|---|---|
| parfait k=0 | 0→1 | 200 | 200 | 234 | 234 |
| parfait k=0 | 9→11 | 100 | 100 | 128 | 128 |
| Médina k=99 | 0→1 | 24 | 172 | 29 | 202 |
| Médina k=99 | 9→11 | 32 | 170 | 34 | 190 |

### Q11 — Trajet Bab Bhar (0) → Mosquée Zitouna (1)

| Méthode | Nombre de pas | Coût | Cases explorées | Optimal en coût ? | Temps (ms) |
|---|---|---|---|---|---|
| BFS | 24 | 29 | 234 | non | 0.57 |
| DFS | 172 | 202 | 386 | non | 0.83 |
| Coût uniforme | 24 | 27 | 230 | oui | 0.59 |
| Glouton (Manhattan) | 24 | 29 | 42 | non | 0.12 |
| A* (h nulle) | 24 | 27 | 230 | oui | 0.58 |
| A* (Tchebychev) | 24 | 27 | 161 | oui | 0.46 |
| A* (Euclide) | 24 | 27 | 147 | oui | 0.43 |
| A* (Manhattan) | 24 | 27 | 112 | oui | 0.32 |
| A* pondéré (Manhattan, w=2) | 24 | 28 | 37 | non | 0.11 |

![trajet](figures/trajet_0_1.png)

### Q11 — Trajet Bab Souika (9) → Bab Jedid (11)

| Méthode | Nombre de pas | Coût | Cases explorées | Optimal en coût ? | Temps (ms) |
|---|---|---|---|---|---|
| BFS | 32 | 34 | 519 | oui | 1.36 |
| DFS | 170 | 190 | 217 | non | 0.51 |
| Coût uniforme | 32 | 34 | 472 | oui | 1.30 |
| Glouton (Manhattan) | 32 | 34 | 45 | oui | 0.13 |
| A* (h nulle) | 32 | 34 | 472 | oui | 1.34 |
| A* (Tchebychev) | 32 | 34 | 246 | oui | 0.73 |
| A* (Euclide) | 32 | 34 | 209 | oui | 0.67 |
| A* (Manhattan) | 32 | 34 | 157 | oui | 0.48 |
| A* pondéré (Manhattan, w=2) | 32 | 34 | 56 | oui | 0.17 |

![trajet](figures/trajet_9_11.png)

## Partie 3 — Le circuit du guide

### Q12 — Matrice des coûts (132 appels à A*, 41 ms)

```
  0  27  29  38  20  21  35  41  55  36  29  38
 25   0  16  15   5   8  16  18  32  22  19  20
 27  16   0  23   9  14  24  14  31  14  11  28
 36  15  23   0  16  19  19  13  17  20  28  23
 20   7  11  18   0   5  15  21  35  21  14  19
 21  10  16  21   5   0  14  24  38  26  19  18
 35  18  26  21  15  14   0  26  38  30  29   4
 41  20  16  15  21  24  26   0  19  11  21  30
 55  34  33  19  35  38  38  19   0  28  38  42
 36  24  16  22  21  26  30  11  28   0  11  34
 29  21  13  30  14  19  29  21  38  11   0  33
 38  22  30  25  19  18   4  30  42  34  33   0
```

Paires (i,j) asymétriques : 27/66. Relation vérifiée `M[i][j] − M[j][i] = cout(j) − cout(i)` pour toutes les paires : **True**.

### Q13-Q14 — Référence

- Plus proche voisin : [0, 4, 5, 1, 3, 7, 9, 10, 2, 6, 11, 8], coût 223
- Held-Karp : coût **176**, tournée [0, 5, 11, 6, 3, 8, 7, 9, 10, 2, 4, 1], 11264 états, 39 ms

### Q15 — Descente 2-opt depuis 10 tournées aléatoires

Coûts atteints : [176, 176, 176, 176, 176, 176, 176, 176, 178, 176] (optimum 176) → optimum atteint 9/10 fois.

### Q16 — Recuit simulé (T0=50, palier=50, 10 graines)

| voisinage | α | itérations | meilleur coût | coût moyen | pire coût |
|---|---|---|---|---|---|
| échange | 0.8 | 1951 | 176 | 181.6 | 198 |
| échange | 0.95 | 8351 | 176 | 177.7 | 183 |
| échange | 0.995 | 85001 | 176 | 176.0 | 176 |
| 2-opt | 0.8 | 1951 | 176 | 176.0 | 176 |
| 2-opt | 0.95 | 8351 | 176 | 176.0 | 176 |
| 2-opt | 0.995 | 85001 | 176 | 176.0 | 176 |

![recuit](figures/recuit.png)

### Q17 — Algorithme génétique (pop 60, 300 gén., tournoi 3, élite 2)

| p_mut | meilleur coût | coût moyen | pire coût | diversité finale (graine G) |
|---|---|---|---|---|
| 0.01 | 176 | 178.9 | 188 | 1 |
| 0.1 | 176 | 178.1 | 185 | 14 |
| 0.3 | 176 | 178.1 | 183 | 19 |

![ag](figures/ag.png)

### Q18 — Comparaison finale (10 graines G … G+9)

| Méthode | Écart moyen (%) | Meilleur écart (%) | Pire écart (%) | Temps moyen (ms) |
|---|---|---|---|---|
| Plus proche voisin | 26.70 | 26.70 | 26.70 | 0.0 |
| Descente 2-opt (départ aléatoire) | 0.00 | 0.00 | 0.00 | 1.5 |
| Recuit simulé (échange, α=0.995) | 0.00 | 0.00 | 0.00 | 332.9 |
| Algorithme génétique (p_mut=0.1) | 1.19 | 0.00 | 5.11 | 211.2 |
| Held-Karp | 0.00 | 0.00 | 0.00 | 31.1 |

## Partie 4 — Le souk réaménagé

### Q19 — Force brute

10 emplacements pour 8 artisans : 10⁸ affectations sans tenir compte de « tous différents », 10!/2! = 1 814 400 affectations injectives.

### Q20-Q21 — 82 solutions au total

| Variante | Nœuds (1re sol.) | Retours (1re sol.) | Temps (ms) | Nœuds (toutes) | Retours (toutes) |
|---|---|---|---|---|---|
| Backtracking simple | 10 | 1 | 0.19 | 260 | 93 |
| + MRV et degré | 9 | 0 | 0.83 | 344 | 111 |
| + forward checking | 9 | 1 | 0.22 | 187 | 93 |
| + MRV, degré et forward checking | 9 | 0 | 0.66 | 265 | 111 |
| AC-3 puis MRV, degré et forward checking | 9 | 0 | 0.64 | 265 | 110 |

Première solution : {'PA': 1, 'PB': 3, 'CH': 2, 'DI': 7, 'BI': 5, 'TI': 4, 'LI': 8, 'PT': 9}

### Q22 — Domaines avant / après AC-3

| variable | avant | après |
|---|---|---|
| PA | 3 valeurs | [1, 3] |
| PB | 3 valeurs | [1, 3] |
| CH | 10 valeurs | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] |
| DI | 7 valeurs | [5, 6, 7] |
| BI | 10 valeurs | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] |
| TI | 10 valeurs | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] |
| LI | 3 valeurs | [8, 9, 10] |
| PT | 10 valeurs | [1, 2, 3, 4, 5, 7, 8, 9, 10] |

### Q23 — La contrainte de trop

- AC-3 seul renvoie **True** (il ne détecte pas l'impossibilité)
- Backtracking : 0 solution, 18 nœuds, 17 retours

## Partie 5 — La Kharbga

Position de milieu de partie (8 demi-coups aléatoires, graine G) :

```
   0 1 2 3 4
0  ● ● · ● ●
1  ● · ● ● ●
2  · ● · ○ ○
3  ○ ○ ● ○ ○
4  ○ ○ ○ ○ ·
```

### Q26-Q27 — Nœuds explorés (eval_1)

| Profondeur | Nœuds Minimax | Nœuds alpha-bêta | Nœuds alpha-bêta + ordre (Q27) | Temps alpha-bêta (ms) |
|---|---|---|---|---|
| 1 | 5 | 5 | 5 | 0.1 |
| 2 | 49 | 18 | 18 | 0.2 |
| 3 | 336 | 121 | 93 | 1.5 |
| 4 | 2770 | 303 | 195 | 3.1 |
| 5 | 20272 | 1367 | 719 | 13.3 |

Vérification : alpha-bêta = Minimax (profondeur 3, eval_1 et eval_2) sur 20/20 positions.

### Q28 — Tournoi eval_1 vs eval_2 (10 parties, profondeur 3, 8 s)

Score : **eval_1 = 5.0**, **eval_2 = 5.0**

| partie | Blancs | résultat | pions eval_2 − eval_1 |
|---|---|---|---|
| 1 | eval_1 | nul | 0 |
| 2 | eval_2 | nul | -1 |
| 3 | eval_1 | nul | 2 |
| 4 | eval_2 | nul | 0 |
| 5 | eval_1 | nul | -1 |
| 6 | eval_2 | nul | 0 |
| 7 | eval_1 | nul | 2 |
| 8 | eval_2 | nul | 1 |
| 9 | eval_1 | nul | 0 |
| 10 | eval_2 | nul | 0 |

