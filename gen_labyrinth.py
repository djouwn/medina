DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]       # nord, sud, est, ouest (ordre imposé)

POINTS_INTERET = [
    (10, 29), (10, 15), (8, 15), (9, 9), (11, 17), (15, 18),
    (16, 13), (5, 8), (10, 1), (1, 14), (3, 17), (19, 12),
]   # 0 Bab Bhar, 1 Zitouna, 2 Souk el Attarine, 3 Souk ech-Chaouachia, 4 Médersa, 5 Dar Ben Abdallah,
    # 6 Tourbet el Bey, 7 Dar Lasram, 8 Kasbah, 9 Bab Souika, 10 Sidi Mahrez, 11 Bab Jedid

class Medina:
    def __init__(self, P, Q, graine):
        self.P, self.Q, self.graine = P, Q, graine
        self.rng = random.Random(graine)                    # générateur n°1 (DFS puis ouvrir_passages)
        self.mur_est = [[True] * Q for _ in range(P)]       # au départ : tout est muré
        self.mur_sud = [[True] * Q for _ in range(P)]
        self.points = list(POINTS_INTERET)
        self._couts_prets = False                           # (utilisé à la question 5)

    # ---- outils internes ----
    def _dans_grille(self, l, c):
        return 0 <= l < self.P and 0 <= c < self.Q

    def _mur_entre(self, a, b):
        (l1, c1), (l2, c2) = a, b
        if l1 == l2:
            return self.mur_est[l1][min(c1, c2)]
        return self.mur_sud[min(l1, l2)][c1]

    def _abattre(self, a, b):
        (l1, c1), (l2, c2) = a, b
        if l1 == l2:                                        # voisines est-ouest
            self.mur_est[l1][min(c1, c2)] = False
        else:                                               # voisines nord-sud
            self.mur_sud[min(l1, l2)][c1] = False

    # ---- Question 3 : DFS avec NOTRE Pile ----
    def generer_dfs(self):
        rng = self.rng
        depart = (rng.randrange(self.P), rng.randrange(self.Q))   # a. case de départ au hasard
        visitees = {depart}
        pile = Pile()
        pile.empiler(depart)
        while not pile.est_vide():                                # b. tant que la pile n'est pas vide
            l, c = pile.sommet()
            non_visitees = []
            for dl, dc in DIRECTIONS:                             #    voisines dans l'ordre N, S, E, O
                v = (l + dl, c + dc)
                if self._dans_grille(*v) and v not in visitees:
                    non_visitees.append(v)
            if non_visitees:
                v = rng.choice(non_visitees)
                self._abattre((l, c), v)                          #    abattre le mur
                visitees.add(v)
                pile.empiler(v)                                   #    avancer
            else:
                pile.depiler()                                    #    retour arrière

    # ---- voisins accessibles (sans mur) : utilisée par TOUTES les parties suivantes ----
    def voisins(self, case):
        l, c = case
        res = []
        for dl, dc in DIRECTIONS:
            v = (l + dl, c + dc)
            if self._dans_grille(*v) and not self._mur_entre(case, v):
                res.append(v)
        return res

    def nb_passages(self):
        n = 0
        for l in range(self.P):
            for c in range(self.Q):
                if c < self.Q - 1 and not self.mur_est[l][c]: n += 1
                if l < self.P - 1 and not self.mur_sud[l][c]: n += 1
        return n

    def texte(self):
        """Dessin ASCII (pratique pour les petites grilles)."""
        lignes = ["+" + "--+" * self.Q]
        for l in range(self.P):
            row, sep = "|", "+"
            for c in range(self.Q):
                row += "  " + ("|" if (c == self.Q - 1 or self.mur_est[l][c]) else " ")
                sep += ("--" if (l == self.P - 1 or self.mur_sud[l][c]) else "  ") + "+"
            lignes += [row, sep]
        return "\n".join(lignes)