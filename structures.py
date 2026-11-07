"""Partie 1.1 : Pile (LIFO) et File (FIFO) construite avec deux Piles."""


class Pile:
    """Pile LIFO basée sur une liste Python."""

    def __init__(self):
        self._data = []

    def empiler(self, x):
        self._data.append(x)

    def depiler(self):
        if not self._data:
            raise IndexError("depiler() sur une pile vide")
        return self._data.pop()

    def sommet(self):
        if not self._data:
            raise IndexError("sommet() sur une pile vide")
        return self._data[-1]

    def est_vide(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)


class File:
    def __init__(self):
        self._entree = Pile()
        self._sortie = Pile()

    def enfiler(self, x):
        self._entree.empiler(x)

    def defiler(self):
        if self._sortie.est_vide():
            while not self._entree.est_vide():
                self._sortie.empiler(self._entree.depiler())
        if self._sortie.est_vide():
            raise IndexError("defiler() sur une file vide")
        return self._sortie.depiler()

    def est_vide(self):
        return self._entree.est_vide() and self._sortie.est_vide()

    def __len__(self):
        return len(self._entree) + len(self._sortie)
