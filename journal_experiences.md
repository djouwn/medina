# Journal d'expériences — Médina 2.0

Graine G = 1234  ·  k = 64

> Tableaux et courbes générés automatiquement par `experiences.py`. Voir `ANALYSES.md` pour les interprétations.

## Partie 1 — La carte

- Graine G = 1234, k = 60 + (G mod 41) = 64
- Passages du labyrinthe parfait : 599 (attendu P×Q−1 = 599)
- Passages après ouverture : 663 (= 599 + 64)
- Escaliers : 28 cases

![carte](figures/carte.png)

## Partie 2 — Le touriste perdu

### Q6b — Contre-exemples BFS (pas minimal ≠ coût minimal)

35 paires de points d'intérêt sur 132 où BFS est strictement plus cher que le coût uniforme. Exemples :

| trajet | BFS : pas | BFS : coût | UCS : pas | UCS : coût |
|---|---|---|---|---|
| 0→1 | 36 | 46 | 40 | 43 |
| 0→9 | 30 | 33 | 30 | 31 |
| 1→0 | 36 | 44 | 40 | 41 |
| 1→4 | 11 | 18 | 11 | 11 |
| 1→5 | 28 | 35 | 32 | 32 |

### Q7 — DFS vs BFS : labyrinthe parfait (k=0) vs Médina (k>0)

| carte | trajet | pas BFS | pas DFS | coût BFS | coût DFS |
|---|---|---|---|---|---|
| parfait k=0 | 0→1 | 96 | 96 | 107 | 107 |
| parfait k=0 | 9→11 | 188 | 188 | 214 | 214 |
| Médina k=64 | 0→1 | 36 | 86 | 46 | 99 |
| Médina k=64 | 9→11 | 38 | 130 | 38 | 144 |

### Q11 — Trajet Bab Bhar (0) → Mosquée Zitouna (1)

| Méthode | Nombre de pas | Coût | Cases explorées | Optimal en coût ? | Temps (ms) |
|---|---|---|---|---|---|
| BFS | 36 | 46 | 318 | non | 1.45 |
| DFS | 86 | 99 | 107 | non | 0.48 |
| Coût uniforme | 40 | 43 | 370 | oui | 1.72 |
| Glouton (Manhattan) | 42 | 45 | 76 | non | 0.35 |
| A* (h nulle) | 40 | 43 | 370 | oui | 1.74 |
| A* (Tchebychev) | 40 | 43 | 302 | oui | 1.68 |
| A* (Euclide) | 40 | 43 | 300 | oui | 1.56 |
| A* (Manhattan) | 40 | 43 | 290 | oui | 2.63 |
| A* pondéré (Manhattan, w=2) | 40 | 43 | 111 | oui | 0.59 |

![trajet](figures/trajet_0_1.png)

### Q11 — Trajet Bab Souika (9) → Bab Jedid (11)

| Méthode | Nombre de pas | Coût | Cases explorées | Optimal en coût ? | Temps (ms) |
|---|---|---|---|---|---|
| BFS | 38 | 38 | 500 | oui | 1.29 |
| DFS | 130 | 144 | 519 | non | 1.20 |
| Coût uniforme | 38 | 38 | 463 | oui | 1.24 |
| Glouton (Manhattan) | 50 | 62 | 62 | non | 0.17 |
| A* (h nulle) | 38 | 38 | 463 | oui | 1.25 |
| A* (Tchebychev) | 38 | 38 | 287 | oui | 0.83 |
| A* (Euclide) | 38 | 38 | 250 | oui | 0.72 |
| A* (Manhattan) | 38 | 38 | 185 | oui | 0.66 |
| A* pondéré (Manhattan, w=2) | 38 | 46 | 93 | non | 0.29 |

![trajet](figures/trajet_9_11.png)

## Partie 3 — Le circuit du guide

### Q12 — Matrice des coûts (132 appels à A*, 57 ms)

```
  0  43  42  64  34  26  43  48  61  31  28  37
 41   0  10  42  11  32  10  45  36  28  25  18
 40  10   0  48  14  31  16  44  42  27  24  24
 62  42  48   0  39  50  30  25  28  41  36  28
 34  13  16  41   0  25   9  38  35  21  18  17
 26  34  33  52  25   0  30  47  46  30  27  22
 43  12  18  32   9  30   0  37  26  30  27   8
 48  47  46  27  38  47  37   0  35  27  22  35
 61  38  44  30  35  46  26  35   0  37  41  24
 31  30  29  43  21  30  30  27  37   0   7  38
 28  27  26  38  18  27  27  22  41   7   0  35
 37  20  26  30  17  22   8  35  24  38  35   0
```

Paires (i,j) asymétriques : 27/66. Relation vérifiée `M[i][j] − M[j][i] = cout(j) − cout(i)` pour toutes les paires : **True**.

### Q13-Q14 — Référence

- Plus proche voisin : [0, 5, 11, 6, 4, 1, 2, 10, 9, 7, 3, 8], coût 262
- Held-Karp : coût **234**, tournée [0, 9, 10, 7, 3, 8, 11, 6, 1, 2, 4, 5], 11264 états, 30 ms

### Q15 — Descente 2-opt depuis 10 tournées aléatoires

Coûts atteints : [236, 234, 236, 234, 234, 236, 256, 234, 234, 236] (optimum 234) → optimum atteint 5/10 fois.

### Q16 — Recuit simulé (T0=50, palier=50, 10 graines)

| voisinage | α | itérations | meilleur coût | coût moyen | pire coût |
|---|---|---|---|---|---|
| échange | 0.8 | 1951 | 234 | 249.7 | 257 |
| échange | 0.95 | 8351 | 234 | 247.0 | 257 |
| échange | 0.995 | 85001 | 234 | 234.8 | 242 |
| 2-opt | 0.8 | 1951 | 234 | 234.2 | 236 |
| 2-opt | 0.95 | 8351 | 234 | 234.0 | 234 |
| 2-opt | 0.995 | 85001 | 234 | 234.0 | 234 |

![recuit](figures/recuit.png)

### Q17 — Algorithme génétique (pop 60, 300 gén., tournoi 3, élite 2)

| p_mut | meilleur coût | coût moyen | pire coût | diversité finale (graine G) |
|---|---|---|---|---|
| 0.01 | 234 | 248.4 | 260 | 2 |
| 0.1 | 234 | 243.6 | 252 | 10 |
| 0.3 | 234 | 245.2 | 256 | 21 |

![ag](figures/ag.png)

### Q18 — Comparaison finale (10 graines G … G+9)

| Méthode | Écart moyen (%) | Meilleur écart (%) | Pire écart (%) | Temps moyen (ms) |
|---|---|---|---|---|
| Plus proche voisin | 11.97 | 11.97 | 11.97 | 0.0 |
| Descente 2-opt (départ aléatoire) | 1.71 | 0.00 | 5.98 | 0.7 |
| Recuit simulé (2-opt, α=0.95) | 0.00 | 0.00 | 0.00 | 30.6 |
| Algorithme génétique (p_mut=0.1) | 4.10 | 0.00 | 7.69 | 189.0 |
| Held-Karp | 0.00 | 0.00 | 0.00 | 39.1 |

## Partie 4 — Le souk réaménagé

### Q19 — Force brute

10 emplacements pour 8 artisans : 10⁸ affectations sans tenir compte de « tous différents », 10!/2! = 1 814 400 affectations injectives.

### Q20-Q21 — 82 solutions au total

| Variante | Nœuds (1re sol.) | Retours (1re sol.) | Temps (ms) | Nœuds (toutes) | Retours (toutes) |
|---|---|---|---|---|---|
| Backtracking simple | 10 | 1 | 0.19 | 260 | 93 |
| + MRV et degré | 9 | 0 | 0.65 | 344 | 111 |
| + forward checking | 9 | 1 | 0.17 | 187 | 93 |
| + MRV, degré et forward checking | 9 | 0 | 0.56 | 265 | 111 |
| AC-3 puis MRV, degré et forward checking | 9 | 0 | 0.50 | 265 | 110 |

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
0  ● · ● ● ●
1  ● · ● ● ●
2  ● ● · · ○
3  ○ ○ ○ ○ ○
4  ○ ○ ○ ○ ·
```

### Q26-Q27 — Nœuds explorés (eval_1)

| Profondeur | Nœuds Minimax | Nœuds alpha-bêta | Nœuds alpha-bêta + ordre (Q27) | Temps alpha-bêta (ms) |
|---|---|---|---|---|
| 1 | 6 | 6 | 6 | 0.0 |
| 2 | 43 | 18 | 18 | 0.2 |
| 3 | 286 | 60 | 56 | 0.5 |
| 4 | 2199 | 173 | 163 | 1.3 |
| 5 | 13950 | 482 | 420 | 3.9 |

Vérification : alpha-bêta = Minimax (profondeur 3, eval_1 et eval_2) sur 20/20 positions.

### Q28 — Tournoi eval_1 vs eval_2 (10 parties, profondeur 3, 10 s)

Score : **eval_1 = 5.0**, **eval_2 = 5.0**

| partie | Blancs | résultat | pions eval_2 − eval_1 |
|---|---|---|---|
| 1 | eval_1 | nul | 0 |
| 2 | eval_2 | nul | 0 |
| 3 | eval_1 | nul | 1 |
| 4 | eval_2 | nul | 1 |
| 5 | eval_1 | nul | 1 |
| 6 | eval_2 | nul | 0 |
| 7 | eval_1 | nul | 2 |
| 8 | eval_2 | nul | 0 |
| 9 | eval_1 | nul | 1 |
| 10 | eval_2 | nul | 0 |

## Bonus — Branch and Bound vs Held-Karp

| n | HK temps (ms) | HK mémoire (Mo) | B&B temps (ms) | B&B mémoire (Mo) | B&B nœuds | HK états |
|---|---|---|---|---|---|---|
| 6 | 0.6 | 0.01 | 1.0 | 0.004 | 64 | 80 |
| 8 | 3.0 | 0.08 | 4.1 | 0.006 | 254 | 448 |
| 10 | 19.3 | 0.54 | 8.1 | 0.008 | 432 | 2304 |
| 12 | 133.7 | 3.76 | 75.8 | 0.010 | 3742 | 11264 |
| 14 | 663.7 | 16.52 | 288.7 | 0.012 | 12302 | 53248 |
| 16 | 3926.5 | 71.29 | 488.0 | 0.014 | 18674 | 245760 |

![bonus](figures/bonus.png)

