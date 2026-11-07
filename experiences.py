"""Génère le journal d'expériences (journal_experiences.md + figures/).

    python experiences.py            # parties 1 à 5
    python experiences.py 2 3        # seulement certaines parties
    python experiences.py bonus      # Branch and Bound vs Held-Karp
"""
import math
import os
import random
import statistics as st
import sys
import time
import tracemalloc

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import config
from config import G, P, Q, K_PASSAGES, POINTS, NOMS
from medina import creer_medina
from recherche import (bfs, dfs, cout_uniforme, a_star, glouton, h_nulle,
                       h_manhattan, h_euclide, h_tchebychev)
from tsp import *
from csp import creer_csp_souk, backtracking, ac3
from kharbga import Kharbga
from jeu_ia import (minimax, alphabeta, eval_1, eval_2, ouverture_aleatoire,
                    tournoi)

FIG = "figures"
os.makedirs(FIG, exist_ok=True)


def table(entetes, lignes):
    s = "| " + " | ".join(entetes) + " |\n|" + "---|" * len(entetes) + "\n"
    for l in lignes:
        s += "| " + " | ".join(str(x) for x in l) + " |\n"
    return s + "\n"


def chrono(f, *a, **k):
    t = time.perf_counter()
    r = f(*a, **k)
    return r, (time.perf_counter() - t) * 1000


# ===================================================================== P1
def partie1():
    md = "## Partie 1 — La carte\n\n"
    m = creer_medina(P, Q, G, K_PASSAGES)
    parfaite = creer_medina(P, Q, G)
    md += (f"- Graine G = {G}, k = 60 + (G mod 41) = {K_PASSAGES}\n"
           f"- Passages du labyrinthe parfait : {parfaite.nb_passages()} "
           f"(attendu P×Q−1 = {P*Q-1})\n"
           f"- Passages après ouverture : {m.nb_passages()} "
           f"(= {P*Q-1} + {K_PASSAGES})\n"
           f"- Escaliers : {len(m.escaliers)} cases\n\n")
    m.afficher(fichier=f"{FIG}/carte.png")
    md += f"![carte]({FIG}/carte.png)\n\n"
    return md


# ===================================================================== P2
METHODES = [
    ("BFS", lambda m, a, b, t: bfs(m, a, b, t)),
    ("DFS", lambda m, a, b, t: dfs(m, a, b, t)),
    ("Coût uniforme", lambda m, a, b, t: cout_uniforme(m, a, b, t)),
    ("Glouton (Manhattan)", lambda m, a, b, t: glouton(m, a, b, h_manhattan, t)),
    ("A* (h nulle)", lambda m, a, b, t: a_star(m, a, b, h_nulle, 1, t)),
    ("A* (Tchebychev)", lambda m, a, b, t: a_star(m, a, b, h_tchebychev, 1, t)),
    ("A* (Euclide)", lambda m, a, b, t: a_star(m, a, b, h_euclide, 1, t)),
    ("A* (Manhattan)", lambda m, a, b, t: a_star(m, a, b, h_manhattan, 1, t)),
    ("A* pondéré (Manhattan, w=2)", lambda m, a, b, t: a_star(m, a, b, h_manhattan, 2, t)),
]


def partie2():
    md = "## Partie 2 — Le touriste perdu\n\n"
    m = creer_medina(P, Q, G, K_PASSAGES)
    parfaite = creer_medina(P, Q, G)
    # Q6b : contre-exemple BFS (moins de pas) mais pas moins coûteux
    cex = []
    for i in range(12):
        for j in range(12):
            if i != j:
                cb = bfs(m, POINTS[i], POINTS[j])
                cu = cout_uniforme(m, POINTS[i], POINTS[j])
                if cb[1] > cu[1]:
                    cex.append((i, j, len(cb[0]) - 1, cb[1], len(cu[0]) - 1, cu[1]))
    md += (f"### Q6b — Contre-exemples BFS (pas minimal ≠ coût minimal)\n\n"
           f"{len(cex)} paires de points d'intérêt sur 132 où BFS est strictement plus cher "
           f"que le coût uniforme. Exemples :\n\n")
    md += table(["trajet", "BFS : pas", "BFS : coût", "UCS : pas", "UCS : coût"],
                [(f"{i}→{j}", a, b, c, d) for i, j, a, b, c, d in cex[:5]])
    # Q7 : parfait vs Médina
    md += "### Q7 — DFS vs BFS : labyrinthe parfait (k=0) vs Médina (k>0)\n\n"
    lignes = []
    for nom, med in (("parfait k=0", parfaite), (f"Médina k={K_PASSAGES}", m)):
        for (i, j) in ((0, 1), (9, 11)):
            b, d = bfs(med, POINTS[i], POINTS[j]), dfs(med, POINTS[i], POINTS[j])
            lignes.append((nom, f"{i}→{j}", len(b[0]) - 1, len(d[0]) - 1, b[1], d[1]))
    md += table(["carte", "trajet", "pas BFS", "pas DFS", "coût BFS", "coût DFS"], lignes)
    # Q11 : tableau de bord
    for (i, j) in ((0, 1), (9, 11)):
        a, b = POINTS[i], POINTS[j]
        opt = cout_uniforme(m, a, b)[1]
        lignes, traces = [], {}
        for nom, f in METHODES:
            tr = []
            (ch, c, nb), ms = chrono(f, m, a, b, tr)
            traces[nom] = (ch, tr)
            lignes.append((nom, len(ch) - 1, c, nb, "oui" if c == opt else "non", f"{ms:.2f}"))
        md += f"### Q11 — Trajet {NOMS[i]} ({i}) → {NOMS[j]} ({j})\n\n"
        md += table(["Méthode", "Nombre de pas", "Coût", "Cases explorées",
                     "Optimal en coût ?", "Temps (ms)"], lignes)
        f = f"{FIG}/trajet_{i}_{j}.png"
        m.afficher(chemins={"BFS": traces["BFS"][0], "A* Manhattan": traces["A* (Manhattan)"][0]},
                   explores={"BFS": traces["BFS"][1], "A* Manhattan": traces["A* (Manhattan)"][1]},
                   titre=f"{NOMS[i]} → {NOMS[j]} : BFS vs A* (Manhattan)", fichier=f)
        md += f"![trajet]({f})\n\n"
    return md


# ===================================================================== P3
def partie3():
    md = "## Partie 3 — Le circuit du guide\n\n"
    m = creer_medina(P, Q, G, K_PASSAGES)
    M, ms = chrono(matrice_couts, m, POINTS)
    md += (f"### Q12 — Matrice des coûts ({matrice_couts.nb_appels} appels à A*, {ms:.0f} ms)\n\n")
    md += "```\n" + "\n".join(" ".join(f"{x:3d}" for x in l) for l in M) + "\n```\n\n"
    asym = sum(1 for i in range(12) for j in range(i + 1, 12) if M[i][j] != M[j][i])
    ok = all(M[i][j] - M[j][i] == m.cout(POINTS[j]) - m.cout(POINTS[i])
             for i in range(12) for j in range(12))
    md += (f"Paires (i,j) asymétriques : {asym}/66. Relation vérifiée "
           f"`M[i][j] − M[j][i] = cout(j) − cout(i)` pour toutes les paires : **{ok}**.\n\n")
    nn = plus_proche_voisin(M)
    (opt, topt), ms_hk = chrono(held_karp, M)
    md += (f"### Q13-Q14 — Référence\n\n- Plus proche voisin : {nn}, coût {cout_tournee(nn, M)}\n"
           f"- Held-Karp : coût **{opt}**, tournée {topt}, {held_karp.nb_etats} états, {ms_hk:.0f} ms\n\n")
    # Q15
    rng = random.Random(G)
    res = [descente_2opt(tournee_aleatoire(12, rng), M)[1] for _ in range(10)]
    md += (f"### Q15 — Descente 2-opt depuis 10 tournées aléatoires\n\nCoûts atteints : {res} "
           f"(optimum {opt}) → optimum atteint {sum(c == opt for c in res)}/10 fois.\n\n")
    # Q16
    configs = {}
    lignes = []
    for vn, vf in (("échange", voisin_echange), ("2-opt", voisin_2opt)):
        for alpha in (0.8, 0.95, 0.995):
            cs, hs = [], None
            for s in range(10):
                b, h = recuit_simule(M, 50, alpha, 50, vf, random.Random(G + s))
                cs.append(cout_tournee(b, M))
                if s == 0:
                    hs = h
            configs[(vn, alpha)] = st.mean(cs)
            lignes.append((vn, alpha, len(hs), min(cs), f"{st.mean(cs):.1f}", max(cs)))
    md += "### Q16 — Recuit simulé (T0=50, palier=50, 10 graines)\n\n"
    md += table(["voisinage", "α", "itérations", "meilleur coût", "coût moyen", "pire coût"], lignes)
    plt.figure(figsize=(9, 4.5))
    for alpha in (0.8, 0.95, 0.995):
        _, h = recuit_simule(M, 50, alpha, 50, voisin_2opt, random.Random(G))
        plt.plot(h, lw=0.6, label=f"α = {alpha}")
    plt.axhline(opt, color="k", ls="--", label="optimum")
    plt.xscale("log"); plt.xlabel("itérations"); plt.ylabel("coût courant")
    plt.title("Recuit simulé (voisin 2-opt)"); plt.legend(); plt.tight_layout()
    plt.savefig(f"{FIG}/recuit.png", dpi=110); plt.close()
    md += f"![recuit]({FIG}/recuit.png)\n\n"
    meilleur_sa = min(configs, key=configs.get)
    # Q17
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    lignes, ga_moy = [], {}
    for pm in (0.01, 0.1, 0.3):
        cs = []
        for s in range(10):
            t, c, hc, hd = algo_genetique(M, 60, 300, pm, 3, 2, random.Random(G + s))
            cs.append(c)
            if s == 0:
                a1.plot(hc, label=f"p_mut={pm}"); a2.plot(hd, label=f"p_mut={pm}")
        ga_moy[pm] = st.mean(cs)
        lignes.append((pm, min(cs), f"{st.mean(cs):.1f}", max(cs), hd[-1]))
    a1.axhline(opt, color="k", ls="--"); a1.set_title("meilleur coût"); a1.set_xlabel("génération")
    a2.set_title("individus distincts"); a2.set_xlabel("génération"); a1.legend(); a2.legend()
    fig.tight_layout(); fig.savefig(f"{FIG}/ag.png", dpi=110); plt.close(fig)
    md += "### Q17 — Algorithme génétique (pop 60, 300 gén., tournoi 3, élite 2)\n\n"
    md += table(["p_mut", "meilleur coût", "coût moyen", "pire coût", "diversité finale (graine G)"], lignes)
    md += f"![ag]({FIG}/ag.png)\n\n"
    best_pm = min(ga_moy, key=ga_moy.get)
    # Q18
    vn, alpha = meilleur_sa
    vf = voisin_echange if vn == "échange" else voisin_2opt
    algos = {
        "Plus proche voisin": lambda s: cout_tournee(plus_proche_voisin(M), M),
        "Descente 2-opt (départ aléatoire)": lambda s: descente_2opt(
            tournee_aleatoire(12, random.Random(G + s)), M)[1],
        f"Recuit simulé ({vn}, α={alpha})": lambda s: cout_tournee(
            recuit_simule(M, 50, alpha, 50, vf, random.Random(G + s))[0], M),
        f"Algorithme génétique (p_mut={best_pm})": lambda s: algo_genetique(
            M, 60, 300, best_pm, 3, 2, random.Random(G + s))[1],
        "Held-Karp": lambda s: held_karp(M)[0],
    }
    lignes = []
    for nom, f in algos.items():
        ecarts, temps = [], []
        for s in range(10):
            c, ms = chrono(f, s)
            ecarts.append(100 * (c - opt) / opt); temps.append(ms)
        lignes.append((nom, f"{st.mean(ecarts):.2f}", f"{min(ecarts):.2f}",
                       f"{max(ecarts):.2f}", f"{st.mean(temps):.1f}"))
    md += "### Q18 — Comparaison finale (10 graines G … G+9)\n\n"
    md += table(["Méthode", "Écart moyen (%)", "Meilleur écart (%)", "Pire écart (%)",
                 "Temps moyen (ms)"], lignes)
    return md


# ===================================================================== P4
def partie4():
    md = "## Partie 4 — Le souk réaménagé\n\n"
    csp = creer_csp_souk()
    md += ("### Q19 — Force brute\n\n10 emplacements pour 8 artisans : 10⁸ affectations sans "
           "tenir compte de « tous différents », 10!/2! = 1 814 400 affectations injectives.\n\n")
    variantes = [("Backtracking simple", {}), ("+ MRV et degré", {"mrv": True}),
                 ("+ forward checking", {"fc": True}),
                 ("+ MRV, degré et forward checking", {"mrv": True, "fc": True})]
    lignes = []
    def une(c, kw):
        r1 = backtracking(c, **kw)
        r2 = backtracking(c, toutes=True, **kw)
        return r1, r2
    for nom, kw in variantes:
        r1, r2 = une(csp, kw)
        lignes.append((nom, r1["noeuds"], r1["retours"], f"{r1['temps_ms']:.2f}",
                       r2["noeuds"], r2["retours"]))
    c2 = csp.copie(); ac3(c2)
    r1, r2 = une(c2, {"mrv": True, "fc": True})
    lignes.append(("AC-3 puis MRV, degré et forward checking", r1["noeuds"], r1["retours"],
                   f"{r1['temps_ms']:.2f}", r2["noeuds"], r2["retours"]))
    md += f"### Q20-Q21 — {r2['nb_solutions']} solutions au total\n\n"
    md += table(["Variante", "Nœuds (1re sol.)", "Retours (1re sol.)", "Temps (ms)",
                 "Nœuds (toutes)", "Retours (toutes)"], lignes)
    md += f"Première solution : {backtracking(csp)['solution']}\n\n"
    # Q22
    avant = csp.copie(); apres = csp.copie(); ac3(apres)
    md += "### Q22 — Domaines avant / après AC-3\n\n"
    md += table(["variable", "avant", "après"],
                [(v, f"{len(avant.domaines[v])} valeurs", f"{apres.domaines[v]}") for v in csp.variables])
    # Q23
    c = creer_csp_souk(lumiere=True)
    ac = ac3(c.copie())
    r = backtracking(c, toutes=True)
    md += (f"### Q23 — La contrainte de trop\n\n- AC-3 seul renvoie **{ac}** "
           f"(il ne détecte pas l'impossibilité)\n- Backtracking : {r['nb_solutions']} solution, "
           f"{r['noeuds']} nœuds, {r['retours']} retours\n\n")
    return md


# ===================================================================== P5
def partie5():
    md = "## Partie 5 — La Kharbga\n\n"
    rng = random.Random(G)
    milieu = ouverture_aleatoire(rng, 8)
    md += "Position de milieu de partie (8 demi-coups aléatoires, graine G) :\n\n```\n" + str(milieu) + "\n```\n\n"
    lignes = []
    for d in range(1, 6):
        s1, s2, s3 = {"noeuds": 0}, {"noeuds": 0}, {"noeuds": 0}
        minimax(milieu, d, eval_1, stats=s1)
        _, ms = chrono(alphabeta, milieu, d, -math.inf, math.inf, eval_1, stats=s2)
        alphabeta(milieu, d, -math.inf, math.inf, eval_1, stats=s3, ordre=True)
        lignes.append((d, s1["noeuds"], s2["noeuds"], s3["noeuds"], f"{ms:.1f}"))
    md += "### Q26-Q27 — Nœuds explorés (eval_1)\n\n"
    md += table(["Profondeur", "Nœuds Minimax", "Nœuds alpha-bêta",
                 "Nœuds alpha-bêta + ordre (Q27)", "Temps alpha-bêta (ms)"], lignes)
    # vérification sur 20 positions
    ok = 0
    for _ in range(20):
        e = ouverture_aleatoire(rng, rng.randint(4, 14))
        ok += all(minimax(e, 3, ev)[0] == alphabeta(e, 3, -math.inf, math.inf, ev)[0]
                  for ev in (eval_1, eval_2))
    md += f"Vérification : alpha-bêta = Minimax (profondeur 3, eval_1 et eval_2) sur {ok}/20 positions.\n\n"
    # tournoi
    (pts, det), ms = chrono(tournoi, G, 10, 3)
    md += f"### Q28 — Tournoi eval_1 vs eval_2 (10 parties, profondeur 3, {ms/1000:.0f} s)\n\n"
    md += f"Score : **eval_1 = {pts['eval_1']}**, **eval_2 = {pts['eval_2']}**\n\n"
    md += table(["partie", "Blancs", "résultat", "pions eval_2 − eval_1"],
                [(i, b, r, d) for i, b, r, d in det])
    return md


# =================================================================== BONUS
def bonus():
    md = "## Bonus — Branch and Bound vs Held-Karp\n\n"
    tailles = list(range(6, 17, 2))
    th, tb, mh, mb, nb = [], [], [], [], []
    lignes = []
    for n in tailles:
        rng = random.Random(G + n)
        M = [[0 if i == j else rng.randint(1, 100) for j in range(n)] for i in range(n)]
        tracemalloc.start(); t = time.perf_counter()
        o1, _ = held_karp(M)
        th.append(time.perf_counter() - t); mh.append(tracemalloc.get_traced_memory()[1] / 1e6)
        tracemalloc.stop()
        tracemalloc.start(); t = time.perf_counter()
        o2, _ = branch_and_bound(M)
        tb.append(time.perf_counter() - t); mb.append(tracemalloc.get_traced_memory()[1] / 1e6)
        tracemalloc.stop()
        assert o1 == o2
        lignes.append((n, f"{th[-1]*1000:.1f}", f"{mh[-1]:.2f}", f"{tb[-1]*1000:.1f}",
                       f"{mb[-1]:.3f}", branch_and_bound.nb_noeuds, held_karp.nb_etats))
    md += table(["n", "HK temps (ms)", "HK mémoire (Mo)", "B&B temps (ms)",
                 "B&B mémoire (Mo)", "B&B nœuds", "HK états"], lignes)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    a1.semilogy(tailles, th, "o-", label="Held-Karp"); a1.semilogy(tailles, tb, "s-", label="Branch & Bound")
    a1.set_title("temps (s)"); a1.set_xlabel("n"); a1.legend()
    a2.semilogy(tailles, mh, "o-", label="Held-Karp"); a2.semilogy(tailles, mb, "s-", label="Branch & Bound")
    a2.set_title("mémoire de pointe (Mo)"); a2.set_xlabel("n"); a2.legend()
    fig.tight_layout(); fig.savefig(f"{FIG}/bonus.png", dpi=110); plt.close(fig)
    return md + f"![bonus]({FIG}/bonus.png)\n\n"


PARTIES = {"1": partie1, "2": partie2, "3": partie3, "4": partie4, "5": partie5, "bonus": bonus}

if __name__ == "__main__":
    choix = sys.argv[1:] or ["1", "2", "3", "4", "5"]
    texte = (f"# Journal d'expériences — Médina 2.0\n\nGraine G = {G}  ·  k = {K_PASSAGES}\n\n"
             "> Tableaux et courbes générés automatiquement par `experiences.py`. "
             "Voir `ANALYSES.md` pour les interprétations.\n\n")
    for c in choix:
        t = time.time()
        print("Partie", c, "...", end=" ", flush=True)
        texte += PARTIES[c]()
        print(f"{time.time() - t:.1f} s")
    nom = "journal_experiences.md" if len(choix) > 1 else f"journal_{choix[0]}.md"
    open(nom, "w", encoding="utf-8").write(texte)
    print("Écrit :", nom)
