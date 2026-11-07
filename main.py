"""Médina 2.0 — démonstration d'une journée complète.

    python main.py            # journée complète (Parties 1 à 5, sans interaction)
    python main.py jouer      # partie de Kharbga contre l'IA (pour la soutenance)
    python main.py carte      # affiche la Médina (fenêtre matplotlib)
"""
import math
import random
import sys

import config
from config import G, P, Q, K_PASSAGES, POINTS, NOMS
from medina import creer_medina
from recherche import bfs, a_star, cout_uniforme, h_manhattan
from tsp import (matrice_couts, plus_proche_voisin, cout_tournee, held_karp,
                 recuit_simule, voisin_2opt)
from csp import creer_csp_souk, backtracking, ac3
from kharbga import Kharbga
from jeu_ia import coup_ia, eval_2, jeu_humain, jouer_partie


def journee():
    print(f"=== Médina 2.0 — graine G = {G} ===\n")
    print("Matin : génération de la carte")
    m = creer_medina(P, Q, G, K_PASSAGES)
    print(f"  {P}x{Q}, {m.nb_passages()} passages, {len(m.escaliers)} escaliers")

    print("\n9 h : le touriste perdu (Bab Bhar -> Zitouna)")
    for nom, f in (("BFS", bfs), ("Coût uniforme", cout_uniforme)):
        ch, c, nb = f(m, POINTS[0], POINTS[1])
        print(f"  {nom:14s}: {len(ch)-1} pas, coût {c}, {nb} cases explorées")
    ch, c, nb = a_star(m, POINTS[0], POINTS[1], h_manhattan)
    print(f"  {'A* Manhattan':14s}: {len(ch)-1} pas, coût {c}, {nb} cases explorées")

    print("\n10 h : le circuit du guide")
    M = matrice_couts(m, POINTS)
    opt, tour = held_karp(M)
    nn = plus_proche_voisin(M)
    sa, _ = recuit_simule(M, 50, 0.95, 50, voisin_2opt, random.Random(G))
    print(f"  plus proche voisin : {cout_tournee(nn, M)}")
    print(f"  recuit simulé      : {cout_tournee(sa, M)}")
    print(f"  Held-Karp (optimum): {opt}  {[NOMS[i] for i in tour]}")

    print("\n14 h : le souk réaménagé")
    csp = creer_csp_souk()
    ac3(csp)
    r = backtracking(csp, mrv=True, fc=True)
    print("  affectation :", {k: v for k, v in sorted(r['solution'].items(), key=lambda kv: kv[1])})

    print("\n17 h : la pause au café (IA contre IA, démonstration)")
    ia = lambda e: coup_ia(e, 3, eval_2)
    fin = jouer_partie(ia, ia)
    print(fin)
    print("  gagnant :", fin.gagnant() or "nul")
    print("\nPour jouer contre l'IA : python main.py jouer")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "jouer":
        jeu_humain()
    elif arg == "carte":
        import matplotlib.pyplot as plt
        creer_medina(P, Q, G, K_PASSAGES).afficher()
        plt.show()
    else:
        journee()
