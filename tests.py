"""Tests du projet. Lancer :  python tests.py   (ou pytest tests.py)."""
import itertools
import math
import random

import config
from structures import Pile, File
from medina import Medina, creer_medina
from recherche import (bfs, dfs, cout_uniforme, a_star, glouton, h_nulle,
                       h_manhattan, h_euclide, h_tchebychev)
from tsp import (matrice_couts, cout_tournee, plus_proche_voisin, held_karp,
                 descente_2opt, recuit_simule, voisin_2opt, voisin_echange,
                 croisement_ox, algo_genetique, branch_and_bound, tournee_aleatoire)
from csp import creer_csp_souk, backtracking, ac3
from kharbga import Kharbga
from jeu_ia import minimax, alphabeta, eval_1, eval_2, ouverture_aleatoire

G, P, Q, K = config.G, config.P, config.Q, config.K_PASSAGES
_cache = {}


def medina():
    if "m" not in _cache:
        _cache["m"] = creer_medina(P, Q, G, K)
        _cache["parfaite"] = creer_medina(P, Q, G, 0)
    return _cache["m"]


# ------------------------------------------------------------ Partie 1
def test_pile_lifo():
    p = Pile()
    for x in (1, 2, 3):
        p.empiler(x)
    assert len(p) == 3 and p.sommet() == 3
    assert [p.depiler() for _ in range(3)] == [3, 2, 1] and p.est_vide()


def test_pile_vide_leve_indexerror():
    p = Pile()
    for f in (p.depiler, p.sommet):
        try:
            f()
            assert False
        except IndexError:
            pass


def test_pile_len_apres_operations():
    p = Pile(); p.empiler("a"); p.empiler("b"); p.depiler()
    assert len(p) == 1 and p.sommet() == "a"


def test_file_fifo_entrelace():
    f = File()
    f.enfiler(1); f.enfiler(2); assert f.defiler() == 1
    f.enfiler(3); f.enfiler(4)
    assert [f.defiler() for _ in range(3)] == [2, 3, 4] and f.est_vide()
    try:
        f.defiler(); assert False
    except IndexError:
        pass


def test_file_utilise_deux_piles():
    f = File()
    assert isinstance(f._entree, Pile) and isinstance(f._sortie, Pile)


def test_labyrinthe_parfait_nb_passages():
    m = creer_medina(P, Q, G)
    assert m.nb_passages() == P * Q - 1


def test_labyrinthe_connexe_arbre():
    m = creer_medina(P, Q, G)
    ch, _, _ = bfs(m, (0, 0), (P - 1, Q - 1))
    vus, pile = {(0, 0)}, [(0, 0)]
    while pile:
        for v in m.voisins(pile.pop()):
            if v not in vus:
                vus.add(v); pile.append(v)
    assert len(vus) == P * Q and ch is not None


def test_reproductibilite():
    a, b = creer_medina(P, Q, G, K), creer_medina(P, Q, G, K)
    assert a.mur_est == b.mur_est and a.mur_sud == b.mur_sud
    assert a.nb_passages() == P * Q - 1 + K


def test_voisins_symetriques():
    m = medina()
    for l in range(P):
        for c in range(Q):
            for v in m.voisins((l, c)):
                assert (l, c) in m.voisins(v)


def test_couts():
    m = medina()
    assert m.cout(config.POINTS[2]) == 3 and m.cout(config.POINTS[3]) == 3
    assert m.cout((8, 17)) == 3 and m.cout((8, 18)) != 3     # distance 2 / 3
    assert len(m.escaliers) == round(0.05 * (P * Q - len(
        [1 for l in range(P) for c in range(Q) if m._couts[l][c] == 3]) - 10))
    assert all(m.cout(c) == 2 for c in m.escaliers)
    assert not (m.escaliers & set(config.POINTS))


# ------------------------------------------------------------ Partie 2
def test_bfs_moins_de_pas_et_ucs_minimal():
    m = medina()
    for i, j in [(0, 1), (9, 11), (7, 5)]:
        a, b = config.POINTS[i], config.POINTS[j]
        cb, _, _ = bfs(m, a, b)
        cu, couc, _ = cout_uniforme(m, a, b)
        cd, _, _ = dfs(m, a, b)
        assert m.chemin_valide(cb) and m.chemin_valide(cd) and m.chemin_valide(cu)
        assert len(cb) <= len(cu) and len(cb) <= len(cd)
        assert couc <= m.cout_chemin(cb)


def test_astar_optimal_pour_heuristiques_admissibles():
    m = medina()
    a, b = config.POINTS[9], config.POINTS[11]
    ref = cout_uniforme(m, a, b)[1]
    for h in (h_nulle, h_manhattan, h_euclide, h_tchebychev):
        assert a_star(m, a, b, h)[1] == ref


def test_manhattan_admissible_partout():
    m = medina()
    b = config.POINTS[1]
    ucs = {}
    for l in range(0, P, 3):
        for c in range(0, Q, 3):
            cout = cout_uniforme(m, (l, c), b)[1]
            assert h_manhattan((l, c), b) <= cout


def test_glouton_et_astar_pondere_valides():
    m = medina()
    a, b = config.POINTS[0], config.POINTS[1]
    for ch, c, _ in (glouton(m, a, b, h_manhattan), a_star(m, a, b, h_manhattan, 2)):
        assert m.chemin_valide(ch) and ch[0] == a and ch[-1] == b
        assert c >= cout_uniforme(m, a, b)[1]


def test_dfs_bfs_meme_longueur_si_parfait():
    m = creer_medina(P, Q, G)
    a, b = config.POINTS[0], config.POINTS[1]
    assert len(dfs(m, a, b)[0]) == len(bfs(m, a, b)[0])   # chemin unique


# ------------------------------------------------------------ Partie 3
def _M():
    if "M" not in _cache:
        _cache["M"] = matrice_couts(medina(), config.POINTS)
    return _cache["M"]


def test_matrice_asymetrie_exacte():
    M, m = _M(), medina()
    assert matrice_couts.nb_appels == 132
    for i in range(12):
        for j in range(12):
            assert M[i][j] - M[j][i] == m.cout(config.POINTS[j]) - m.cout(config.POINTS[i])


def test_held_karp_vs_force_brute():
    rng = random.Random(5)
    n = 7
    M = [[0 if i == j else rng.randint(1, 50) for j in range(n)] for i in range(n)]
    brute = min(cout_tournee([0] + list(p), M) for p in itertools.permutations(range(1, n)))
    opt, t = held_karp(M)
    assert opt == brute == cout_tournee(t, M) and sorted(t) == list(range(n)) and t[0] == 0
    assert branch_and_bound(M)[0] == brute


def test_held_karp_nb_etats():
    held_karp(_M())
    assert held_karp.nb_etats == 11 * 2 ** 10


def test_heuristiques_tsp_valides_et_bornees():
    M = _M(); opt, _ = held_karp(M); rng = random.Random(1)
    nn = plus_proche_voisin(M)
    d, cd = descente_2opt(tournee_aleatoire(12, rng), M)
    for t in (nn, d):
        assert sorted(t) == list(range(12)) and t[0] == 0
    assert cout_tournee(nn, M) >= opt and cd >= opt
    for vois in (voisin_echange, voisin_2opt):
        b, hist = recuit_simule(M, 50, 0.9, 20, vois, rng)
        assert sorted(b) == list(range(12)) and cout_tournee(b, M) >= opt


def test_ox_exemple_annexe():
    assert croisement_ox([1, 2, 3, 4, 5, 6, 7, 8], [8, 6, 4, 2, 7, 5, 3, 1],
                         coupe=(3, 5)) == [8, 2, 7, 4, 5, 6, 3, 1]


def test_ag_valide():
    M = _M(); opt, _ = held_karp(M)
    t, c, hc, hd = algo_genetique(M, 30, 40, 0.1, 3, 2, random.Random(2))
    assert sorted(t) == list(range(12)) and c == cout_tournee(t, M) >= opt
    assert all(hc[i + 1] <= hc[i] for i in range(len(hc) - 1))   # élitisme


# ------------------------------------------------------------ Partie 4
def _verifie_souk(s, lumiere=False):
    PA, PB, CH, DI, BI, TI, LI, PT = (s[k] for k in ("PA", "PB", "CH", "DI", "BI", "TI", "LI", "PT"))
    assert len(set(s.values())) == 8
    assert PA <= 3 and PB <= 3 and abs(PA - PB) >= 2
    assert abs(DI - PA) >= 4 and abs(DI - PB) >= 4 and DI <= 7
    assert LI >= 8 and abs(BI - TI) == 1 and abs(CH - TI) <= 2 and abs(PT - DI) >= 2


def test_souk_solutions():
    csp = creer_csp_souk()
    r = backtracking(csp, toutes=True)
    assert r["nb_solutions"] > 0
    for s in r["solutions"]:
        _verifie_souk(s)
    for kw in ({"mrv": True}, {"fc": True}, {"mrv": True, "fc": True}):
        assert backtracking(csp, toutes=True, **kw)["nb_solutions"] == r["nb_solutions"]
        _verifie_souk(backtracking(csp, **kw)["solution"])


def test_ac3_retire_2_de_PA():
    csp = creer_csp_souk()
    assert 2 in csp.domaines["PA"]
    assert ac3(csp) and 2 not in csp.domaines["PA"] and csp.domaines["PA"] == [1, 3]


def test_contrainte_de_trop():
    csp = creer_csp_souk(lumiere=True)
    assert ac3(csp.copie()) is True            # AC-3 NE détecte PAS l'impossibilité
    assert backtracking(csp)["solution"] is None


# ------------------------------------------------------------ Partie 5
def test_kharbga_depart():
    e = Kharbga()
    assert e.nb_pions("B") == e.nb_pions("N") == 10 and e.joueur == "B"
    assert len(e.coups_legaux()) == 5            # seuls les pions de la ligne 3 avancent
    assert not e.est_terminal() and e.gagnant() is None


def test_kharbga_double_capture_figure2():
    e = Kharbga.depuis_lignes([".....", "N.B..", "...NB", "..N..", "..B.."])
    f = e.jouer(((1, 2), (2, 2)))
    assert f.nb_pions("N") == 1 and f.case(2, 3) == "." and f.case(3, 2) == "."
    assert e.nb_pions("N") == 3                  # l'ancien état n'a pas changé
    assert f.joueur == "N"


def test_kharbga_pas_de_suicide():
    e = Kharbga.depuis_lignes([".....", ".....", "B.B..", ".N...", "....."], joueur="N")
    f = e.jouer(((3, 1), (2, 1)))                # le Noir s'insère entre deux Blancs
    assert f.case(2, 1) == "N" and f.nb_pions("N") == 1


def test_kharbga_fin_de_partie():
    e = Kharbga.depuis_lignes(["B....", ".....", ".....", ".....", "....N"])
    assert e.est_terminal() and e.gagnant() == "N" or e.gagnant() == "B"
    bloque = Kharbga.depuis_lignes(["BN...", "NN...", "BB...", ".....", "....."], joueur="B")
    nul = Kharbga(Kharbga().plateau, "B", 60)
    assert nul.est_terminal() and nul.gagnant() is None


def test_alphabeta_egal_minimax():
    rng = random.Random(G)
    for _ in range(20):
        e = ouverture_aleatoire(rng, rng.randint(4, 14))
        for ev in (eval_1, eval_2):
            v1 = minimax(e, 3, ev)[0]
            v2 = alphabeta(e, 3, -math.inf, math.inf, ev)[0]
            v3 = alphabeta(e, 3, -math.inf, math.inf, ev, ordre=True)[0]
            assert v1 == v2 == v3


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    echecs = 0
    for nom, f in tests:
        try:
            f(); print("OK  ", nom)
        except Exception as e:        # noqa
            echecs += 1; print("ECHEC", nom, repr(e))
    print(f"\n{len(tests) - echecs}/{len(tests)} tests réussis")
    raise SystemExit(echecs)
