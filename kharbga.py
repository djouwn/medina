"""Partie 5.1 : moteur de la Kharbga simplifiée (règles de l'Annexe A).
L'état est IMMUABLE : jouer() renvoie un nouvel état."""

N = 5
DIRS = [(-1, 0), (1, 0), (0, 1), (0, -1)]
LIMITE_SANS_CAPTURE = 60   # 60 demi-coups consécutifs sans capture -> nul


def adversaire(j):
    return "N" if j == "B" else "B"


class Kharbga:
    def __init__(self, plateau=None, joueur="B", sans_capture=0):
        """plateau : tuple de 25 caractères 'B', 'N' ou '.' (ligne par ligne).
        Position de départ : Noirs lignes 0-1, Blancs lignes 3-4, Blancs jouent."""
        if plateau is None:
            plateau = tuple("N" * 10 + "." * 5 + "B" * 10)
        self.plateau = plateau
        self.joueur = joueur
        self.sans_capture = sans_capture
        self._coups = None

    # ---------------------------------------------------------- outils
    @classmethod
    def depuis_lignes(cls, lignes, joueur="B", sans_capture=0):
        return cls(tuple("".join(lignes)), joueur, sans_capture)

    def case(self, l, c):
        return self.plateau[l * N + c]

    def nb_pions(self, joueur):
        return self.plateau.count(joueur)

    def coups_pour(self, joueur):
        coups = []
        p = self.plateau
        for i, x in enumerate(p):
            if x != joueur:
                continue
            l, c = divmod(i, N)
            for dl, dc in DIRS:
                l2, c2 = l + dl, c + dc
                if 0 <= l2 < N and 0 <= c2 < N and p[l2 * N + c2] == ".":
                    coups.append(((l, c), (l2, c2)))
        return coups

    # ------------------------------------------------------------ API
    def coups_legaux(self):
        if self._coups is None:
            self._coups = self.coups_pour(self.joueur)
        return self._coups

    def jouer(self, coup):
        """Renvoie le NOUVEL état (captures faites, trait changé)."""
        (l1, c1), (l2, c2) = coup
        p = list(self.plateau)
        moi, adv = self.joueur, adversaire(self.joueur)
        p[l1 * N + c1] = "."
        p[l2 * N + c2] = moi
        captures = 0
        for dl, dc in DIRS:
            la, ca = l2 + dl, c2 + dc          # voisine
            lb, cb = l2 + 2 * dl, c2 + 2 * dc  # case suivante
            if (0 <= la < N and 0 <= ca < N and 0 <= lb < N and 0 <= cb < N
                    and p[la * N + ca] == adv and p[lb * N + cb] == moi):
                p[la * N + ca] = "."
                captures += 1
        return Kharbga(tuple(p), adv, 0 if captures else self.sans_capture + 1)

    def est_terminal(self):
        return (self.nb_pions("B") <= 1 or self.nb_pions("N") <= 1
                or self.sans_capture >= LIMITE_SANS_CAPTURE
                or not self.coups_legaux())

    def gagnant(self):
        """'B', 'N' ou None (nul, ou partie non terminée)."""
        if self.nb_pions("B") <= 1:
            return "N"
        if self.nb_pions("N") <= 1:
            return "B"
        if self.sans_capture >= LIMITE_SANS_CAPTURE:
            return None
        if not self.coups_legaux():
            return adversaire(self.joueur)       # le joueur bloqué perd
        return None

    def __str__(self):
        sym = {"B": "○", "N": "●", ".": "·"}
        lignes = ["   " + " ".join(str(c) for c in range(N))]
        for l in range(N):
            lignes.append(f"{l}  " + " ".join(sym[self.case(l, c)] for c in range(N)))
        return "\n".join(lignes)
