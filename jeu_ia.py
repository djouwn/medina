"""Partie 5.2 - 5.3 : Minimax, alpha-bêta, évaluations, tournoi, jeu humain."""
import math
import random
import time

from kharbga import Kharbga, adversaire

GAIN = 1000


def valeur_terminale(etat, ia):
    g = etat.gagnant()
    return 0 if g is None else (GAIN if g == ia else -GAIN)


# ------------------------------------------------------------- évaluations
def eval_1(etat, ia):
    """(pions de l'IA) - (pions de l'adversaire)."""
    return etat.nb_pions(ia) - etat.nb_pions(adversaire(ia))


def menaces(etat, joueur):
    """Nombre de pions de `joueur` capturables au prochain coup adverse :
    pion T avec, sur un même axe, un pion adverse d'un côté et une case vide
    de l'autre côté qui touche un autre pion adverse (qui s'y déplacerait)."""
    adv = adversaire(joueur)
    n = 0
    for i, x in enumerate(etat.plateau):
        if x != joueur:
            continue
        l, c = divmod(i, 5)
        menace = False
        for dl, dc in ((1, 0), (0, 1)):
            for s in (1, -1):
                la, ca = l + s * dl, c + s * dc            # côté "ami adverse"
                lv, cv = l - s * dl, c - s * dc            # côté vide
                if not (0 <= la < 5 and 0 <= ca < 5 and 0 <= lv < 5 and 0 <= cv < 5):
                    continue
                if etat.case(la, ca) == adv and etat.case(lv, cv) == ".":
                    for ddl, ddc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        lw, cw = lv + ddl, cv + ddc
                        if (lw, cw) != (l, c) and 0 <= lw < 5 and 0 <= cw < 5 \
                                and etat.case(lw, cw) == adv:
                            menace = True
        n += menace
    return n


def eval_2(etat, ia):
    """Trois critères : matériel (poids 10), mobilité (1), menaces (3)."""
    adv = adversaire(ia)
    materiel = etat.nb_pions(ia) - etat.nb_pions(adv)
    mobilite = len(etat.coups_pour(ia)) - len(etat.coups_pour(adv))
    danger = menaces(etat, adv) - menaces(etat, ia)
    return 10 * materiel + 1 * mobilite + 3 * danger


# ----------------------------------------------------------------- minimax
def minimax(etat, profondeur, evaluation, ia=None, stats=None):
    """Renvoie (valeur du point de vue de l'IA, meilleur_coup).
    L'IA est le joueur au trait à la racine (sauf si `ia` est donné)."""
    ia = ia or etat.joueur
    if stats is None:
        stats = {"noeuds": 0}
    stats["noeuds"] += 1
    if etat.est_terminal():
        return valeur_terminale(etat, ia), None
    if profondeur == 0:
        return evaluation(etat, ia), None
    maxi = etat.joueur == ia
    meilleur, val = None, -math.inf if maxi else math.inf
    for coup in etat.coups_legaux():
        v, _ = minimax(etat.jouer(coup), profondeur - 1, evaluation, ia, stats)
        if (maxi and v > val) or (not maxi and v < val):
            val, meilleur = v, coup
    return val, meilleur


def alphabeta(etat, profondeur, alpha, beta, evaluation, ia=None, stats=None,
              ordre=False):
    """Même valeur que minimax. ordre=True : captures examinées d'abord."""
    ia = ia or etat.joueur
    if stats is None:
        stats = {"noeuds": 0}
    stats["noeuds"] += 1
    if etat.est_terminal():
        return valeur_terminale(etat, ia), None
    if profondeur == 0:
        return evaluation(etat, ia), None
    maxi = etat.joueur == ia
    enfants = [(c, etat.jouer(c)) for c in etat.coups_legaux()] if ordre else None
    if ordre:                       # moins de pions adverses = plus de captures
        adv = adversaire(etat.joueur)
        enfants.sort(key=lambda ce: ce[1].nb_pions(adv))
    suite = enfants if ordre else ((c, None) for c in etat.coups_legaux())
    meilleur, val = None, -math.inf if maxi else math.inf
    for coup, enfant in suite:
        if enfant is None:
            enfant = etat.jouer(coup)
        v, _ = alphabeta(enfant, profondeur - 1, alpha, beta, evaluation, ia,
                         stats, ordre)
        if maxi:
            if v > val:
                val, meilleur = v, coup
            alpha = max(alpha, val)
        else:
            if v < val:
                val, meilleur = v, coup
            beta = min(beta, val)
        if alpha >= beta:           # coupure
            break
    return val, meilleur


def coup_ia(etat, profondeur, evaluation):
    return alphabeta(etat, profondeur, -math.inf, math.inf, evaluation, ordre=True)[1]


# ------------------------------------------------------- parties / tournoi
def ouverture_aleatoire(rng, nb_demi_coups):
    etat = Kharbga()
    for _ in range(nb_demi_coups):
        if etat.est_terminal():
            break
        etat = etat.jouer(rng.choice(etat.coups_legaux()))
    return etat


def jouer_partie(joueur_B, joueur_N, etat=None, max_demi_coups=300):
    """joueur_X : fonction etat -> coup. Renvoie l'état final."""
    etat = etat or Kharbga()
    for _ in range(max_demi_coups):
        if etat.est_terminal():
            break
        f = joueur_B if etat.joueur == "B" else joueur_N
        etat = etat.jouer(f(etat))
    return etat


def tournoi(G, n_parties=10, profondeur=3):
    """eval_1 contre eval_2 ; on alterne qui commence (= qui joue Blancs).
    Chaque partie : 4 demi-coups aléatoires tirés avec random.Random(G)."""
    rng = random.Random(G)
    p1 = lambda e: coup_ia(e, profondeur, eval_1)
    p2 = lambda e: coup_ia(e, profondeur, eval_2)
    pts = {"eval_1": 0.0, "eval_2": 0.0}
    details = []
    for i in range(n_parties):
        debut = ouverture_aleatoire(rng, 4)
        e1_blanc = (i % 2 == 0)
        # l'ouverture a 4 demi-coups : les Blancs ont le trait de nouveau
        B, Nn = (p1, p2) if e1_blanc else (p2, p1)
        fin = jouer_partie(B, Nn, debut)
        g = fin.gagnant()
        c1, c2 = ("B", "N") if e1_blanc else ("N", "B")
        if g is None:
            pts["eval_1"] += .5; pts["eval_2"] += .5; res = "nul"
        elif g == c1:
            pts["eval_1"] += 1; res = "eval_1"
        else:
            pts["eval_2"] += 1; res = "eval_2"
        diff = fin.nb_pions(c2) - fin.nb_pions(c1)       # pions eval_2 - eval_1
        details.append((i + 1, "eval_1" if e1_blanc else "eval_2", res, diff))
    return pts, details


# -------------------------------------------------------------- humain
def jeu_humain(profondeur=4, humain="B"):
    """Boucle texte. Coup saisi : 'l1 c1 l2 c2' (ex. : 3 2 2 2). 'q' pour quitter."""
    etat = Kharbga()
    ia = adversaire(humain)
    print("Kharbga — vous jouez les", "Blancs (○)" if humain == "B" else "Noirs (●)")
    while not etat.est_terminal():
        print("\n" + str(etat))
        if etat.joueur == humain:
            legaux = etat.coups_legaux()
            while True:
                s = input("Votre coup (l1 c1 l2 c2) : ").strip()
                if s.lower() == "q":
                    return
                try:
                    a, b, c, d = map(int, s.split())
                    coup = ((a, b), (c, d))
                except ValueError:
                    print("Format invalide."); continue
                if coup in legaux:
                    break
                print("Coup illégal. Coups possibles :", legaux)
        else:
            t0 = time.perf_counter()
            coup = coup_ia(etat, profondeur, eval_2)
            print(f"Médina 2.0 joue {coup} ({time.perf_counter() - t0:.2f} s)")
        etat = etat.jouer(coup)
    print("\n" + str(etat))
    g = etat.gagnant()
    print("Partie nulle." if g is None else
          ("Vous avez gagné !" if g == humain else "Médina 2.0 a gagné."))
