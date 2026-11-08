# Journal d'expériences — Médina 2.0

Graine G = 9064  ·  k = 63

> Tableaux et courbes générés automatiquement par `experiences.py`. Voir `ANALYSES.md` pour les interprétations.

## Bonus — Branch and Bound vs Held-Karp

| n | HK temps (ms) | HK mémoire (Mo) | B&B temps (ms) | B&B mémoire (Mo) | B&B nœuds | HK états |
|---|---|---|---|---|---|---|
| 6 | 0.8 | 0.02 | 1.0 | 0.004 | 56 | 80 |
| 8 | 3.9 | 0.13 | 11.7 | 0.006 | 563 | 448 |
| 10 | 23.9 | 0.63 | 19.2 | 0.007 | 823 | 2304 |
| 12 | 127.3 | 3.92 | 147.3 | 0.009 | 5881 | 11264 |
| 14 | 606.6 | 17.34 | 106.9 | 0.011 | 3982 | 53248 |
| 16 | 3443.4 | 75.19 | 747.8 | 0.015 | 21169 | 245760 |

![bonus](figures/bonus.png)

