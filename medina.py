"""Partie 1.2 : la carte de la Médina (grille P x Q, murs, coûts)."""
import random

from structures import Pile
from config import POINTS

# Ordre imposé : nord, sud, est, ouest
DIRS = [(-1, 0), (1, 0), (0, 1), (0, -1)]


class Medina:
    def __init__(self, P, Q, graine):
        self.P, self.Q, self.graine = P, Q, graine
        # rng UNIQUE partagé par generer_dfs() puis ouvrir_passages()
        self.rng = random.Random(graine)
        self.points = list(POINTS)
        # mur_est[l][c]  : mur entre (l,c) et (l,c+1)
        # mur_sud[l][c]  : mur entre (l,c) et (l+1,c)
        self.mur_est = [[True] * Q for _ in range(P)]
        self.mur_sud = [[True] * Q for _ in range(P)]
        self._couts = self._calculer_couts()

    # ------------------------------------------------------------ murs
    def dans_grille(self, l, c):
        return 0 <= l < self.P and 0 <= c < self.Q

    def a_mur(self, a, b):
        (l1, c1), (l2, c2) = a, b
        if l1 == l2:
            return self.mur_est[l1][min(c1, c2)]
        return self.mur_sud[min(l1, l2)][c1]

    def _abattre(self, a, b):
        (l1, c1), (l2, c2) = a, b
        if l1 == l2:
            self.mur_est[l1][min(c1, c2)] = False
        else:
            self.mur_sud[min(l1, l2)][c1] = False

    def nb_passages(self):
        """Nombre de murs intérieurs abattus."""
        total_int = self.P * (self.Q - 1) + (self.P - 1) * self.Q
        restants = len(self._murs_restants())
        return total_int - restants

    def _murs_restants(self):
        """Murs intérieurs restants : ligne par ligne, puis colonne par colonne,
        pour chaque case d'abord le mur est, puis le mur sud (ordre imposé)."""
        murs = []
        for l in range(self.P):
            for c in range(self.Q):
                if c < self.Q - 1 and self.mur_est[l][c]:
                    murs.append(((l, c), (l, c + 1)))
                if l < self.P - 1 and self.mur_sud[l][c]:
                    murs.append(((l, c), (l + 1, c)))
        return murs

    # ------------------------------------------------------ génération
    def generer_dfs(self):
        """Labyrinthe parfait par DFS itératif avec notre Pile."""
        rng = self.rng
        self.mur_est = [[True] * self.Q for _ in range(self.P)]
        self.mur_sud = [[True] * self.Q for _ in range(self.P)]
        visitee = [[False] * self.Q for _ in range(self.P)]
        depart = (rng.randrange(self.P), rng.randrange(self.Q))
        visitee[depart[0]][depart[1]] = True
        pile = Pile()
        pile.empiler(depart)
        while not pile.est_vide():
            l, c = pile.sommet()
            non_visitees = [(l + dl, c + dc) for dl, dc in DIRS
                            if self.dans_grille(l + dl, c + dc)
                            and not visitee[l + dl][c + dc]]
            if non_visitees:
                v = rng.choice(non_visitees)
                self._abattre((l, c), v)
                visitee[v[0]][v[1]] = True
                pile.empiler(v)
            else:
                pile.depiler()

    def ouvrir_passages(self, k):
        """Abat k murs intérieurs restants tirés avec rng.sample."""
        murs = self._murs_restants()
        if k > len(murs):
            raise ValueError("pas assez de murs à abattre")
        for a, b in self.rng.sample(murs, k):
            self._abattre(a, b)

    # ------------------------------------------------------- navigation
    def voisins(self, case):
        """Cases accessibles (sans mur), ordre N, S, E, O."""
        l, c = case
        res = []
        for dl, dc in DIRS:
            n = (l + dl, c + dc)
            if self.dans_grille(*n) and not self.a_mur(case, n):
                res.append(n)
        return res

    # ------------------------------------------------------------ coûts
    def _est_souk(self, l, c):
        for i in (2, 3):  # Souk el Attarine, Souk ech-Chaouachia
            pl, pc = self.points[i]
            if abs(l - pl) + abs(c - pc) <= 2:
                return True
        return False

    def _calculer_couts(self):
        couts = [[1] * self.Q for _ in range(self.P)]
        souk = set()
        for l in range(self.P):
            for c in range(self.Q):
                if self._est_souk(l, c):
                    couts[l][c] = 3
                    souk.add((l, c))
        poi = set(self.points)
        # second générateur, indépendant du premier (ordre imposé)
        rng2 = random.Random(self.graine)
        candidates = [(l, c) for l in range(self.P) for c in range(self.Q)
                      if (l, c) not in souk and (l, c) not in poi]
        self.escaliers = set(rng2.sample(candidates, round(0.05 * len(candidates))))
        for l, c in self.escaliers:
            couts[l][c] = 2
        return couts

    def cout(self, case):
        return self._couts[case[0]][case[1]]

    def cout_chemin(self, chemin):
        """Somme des coûts des cases où l'on entre (départ non compté)."""
        return sum(self.cout(c) for c in chemin[1:])

    def chemin_valide(self, chemin):
        return all(b in self.voisins(a) for a, b in zip(chemin, chemin[1:]))

    # -------------------------------------------------------- affichage
    def afficher(self, chemins=None, explores=None, titre=None, fichier=None):
        """Dessin matplotlib : coûts, murs, points d'intérêt.

        chemins  : dict {nom: chemin} ou liste de chemins
        explores : dict {nom: cases explorées} ou liste de listes de cases
        fichier  : si donné, sauvegarde la figure (PNG)
        """
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap

        fig, ax = plt.subplots(figsize=(12, 8))
        cmap = ListedColormap(["#f6f1e7", "#f4c24c", "#e07b5f"])
        grille = [[self._couts[l][c] - 1 for c in range(self.Q)] for l in range(self.P)]
        ax.imshow(grille, cmap=cmap, vmin=0, vmax=2, extent=(0, self.Q, self.P, 0))
        # murs
        kw = dict(color="#2b2d42", lw=1.6)
        ax.plot([0, self.Q, self.Q, 0, 0], [0, 0, self.P, self.P, 0], **kw)
        for l in range(self.P):
            for c in range(self.Q):
                if c < self.Q - 1 and self.mur_est[l][c]:
                    ax.plot([c + 1, c + 1], [l, l + 1], **kw)
                if l < self.P - 1 and self.mur_sud[l][c]:
                    ax.plot([c, c + 1], [l + 1, l + 1], **kw)
        couleurs = ["#2a9d8f", "#e63946", "#457b9d", "#6a4c93", "#ff7f0e"]
        if explores:
            items = explores.items() if isinstance(explores, dict) else enumerate(explores)
            for i, (nom, cases) in enumerate(items):
                xs = [c + 0.5 + 0.12 * (i - 0.5) for _, c in cases]
                ys = [l + 0.5 + 0.12 * (i - 0.5) for l, _ in cases]
                ax.scatter(xs, ys, s=10, color=couleurs[i % 5], alpha=0.45,
                           label=f"explorées : {nom}" if isinstance(explores, dict) else None)
        if chemins:
            items = chemins.items() if isinstance(chemins, dict) else enumerate(chemins)
            for i, (nom, ch) in enumerate(items):
                ax.plot([c + 0.5 for _, c in ch], [l + 0.5 for l, _ in ch],
                        color=couleurs[i % 5], lw=2.5, label=f"chemin : {nom}")
        for i, (l, c) in enumerate(self.points):
            ax.scatter(c + 0.5, l + 0.5, s=330, color="#1d3557", zorder=5)
            ax.text(c + 0.5, l + 0.5, str(i), color="white", ha="center",
                    va="center", fontsize=8, fontweight="bold", zorder=6)
        ax.set_xlim(0, self.Q); ax.set_ylim(self.P, 0)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(titre or f"Médina 2.0 — graine G = {self.graine} "
                     "(beige = 1, jaune = escaliers 2, orange = souk bondé 3)")
        if (chemins or explores):
            ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
        fig.tight_layout()
        if fichier:
            fig.savefig(fichier, dpi=110)
            plt.close(fig)
        return fig


def creer_medina(P, Q, G, k=None):
    """Raccourci : génère le labyrinthe parfait puis ouvre k passages."""
    m = Medina(P, Q, G)
    m.generer_dfs()
    if k:
        m.ouvrir_passages(k)
    return m
