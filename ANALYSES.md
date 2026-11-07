# Réponses aux questions « Analyse »

> Les chiffres cités viennent de `journal_experiences.md` pour **G = 1234**. Avec votre graine G,
> relancez `experiences.py` et **remplacez les chiffres** par les vôtres : le raisonnement reste valable.

## Partie 1
**Q2 — `defiler()` amorti O(1).** Un défilage qui trouve la pile de sortie vide transfère toute la pile
d'entrée (O(n)). Mais chaque élément n'est transféré qu'une fois dans sa vie : au total 4 opérations
élémentaires par élément (empiler, dépiler-pour-transfert, empiler en sortie, dépiler). Sur n opérations
le coût total est O(n) → O(1) amorti.

**Q3 — pas de boucle.** Le graphe a P×Q sommets, est connexe (le DFS atteint toutes les cases) et possède
P×Q−1 arêtes (passages). Un graphe connexe à n sommets et n−1 arêtes est un arbre, donc sans cycle.

**Q4 — chemins.** Labyrinthe parfait : exactement **un** chemin sans détour entre deux cases. Après
l'ouverture de k murs, chaque mur abattu crée un cycle (nombre cyclomatique = k) : il existe plusieurs
chemins. Indispensable pour la Partie 2 : sinon BFS, DFS, coût uniforme et A* renvoient tous le même
chemin et la comparaison n'a aucun sens.

## Partie 2
**Q6a.** La file traite les cases par distance croissante (en nombre de pas) : toutes les cases à d pas sont
défilées avant celles à d+1, donc la première fois qu'on atteint l'arrivée, c'est par un chemin le plus court
en pas. **Q6b.** Non : BFS ignore les coûts. Sur notre carte, 0→1 : BFS 36 pas / coût 46, alors que le coût
minimal est 43 (40 pas) ; 35 paires de points sur 132 sont dans ce cas (BFS traverse des souks à coût 3).

**Q7.** Labyrinthe parfait (k=0) : BFS et DFS donnent le même chemin (unique) : 96 pas pour 0→1. Médina
(k>0) : BFS 36 pas, DFS 86 pas : le DFS prend le premier chemin rencontré, souvent très long.

**Q8.** Dijkstra développe toujours la case de plus petit g : quand l'arrivée sort du tas, tout autre chemin
l'atteignant passerait par une case de g ≥ au sien, avec des coûts positifs → pas moins cher. (Vérifié par
les tests : coût UCS ≤ coût BFS/DFS.)

**Q9c — Manhattan admissible.** Chaque pas coûte ≥ 1 (ruelle 1, escalier 2, souk 3) et un pas change
l+c de exactement 1 : il faut au moins |Δl|+|Δc| pas, donc coût restant réel ≥ distance de Manhattan.
**Q9d.** De la moins à la plus informée : h_nulle < Tchebychev ≤ Euclide ≤ Manhattan (toutes ≤ Manhattan
car max ≤ √(a²+b²) ≤ a+b). A* avec h_nulle = coût uniforme (mêmes 370 cases explorées sur 0→1).

**Q10.** Glouton : non optimal (0→1 : 45 contre 43 ; 9→11 : 62 contre 38). A* pondéré (w=2) : non garanti
optimal, coût ≤ 2× l'optimum (9→11 : 46 contre 38), mais bien moins de cases (93 contre 185). Acceptable
quand la rapidité prime (temps réel, mobile/batterie, très grande carte) et qu'un détour de quelques pour cent
est toléré.

**Q11.** Recommandation : **A\* avec Manhattan** : optimal, 185 cases contre 463 pour Dijkstra (9→11),
~1-3 ms ≪ 1 s. Si la carte grandit, passer à A* pondéré.

## Partie 3
**Q12.** 12×11 = **132** appels (66 suffiraient avec la relation ci-dessous). La matrice n'est pas symétrique :
on paie le coût de la case **où l'on entre**. Le même chemin dans l'autre sens remplace le coût de l'arrivée
par celui du départ, donc `M[i][j] − M[j][i] = cout(j) − cout(i)` (vérifié sur les 66 paires) : symétrique
seulement si les deux cases ont le même coût (27 paires asymétriques ici).

**Q14.** États = (n−1)·2^(n−2) = 11·2¹⁰ = **11 264** pour n = 12. Pour 60 monuments : 59·2⁵⁸ ≈ 1,7·10¹⁹ états
(mémoire impossible) et temps O(n²·2ⁿ).

**Q15.** Non : 5/10 départs atteignent l'optimum 234 (les autres s'arrêtent à 236 ou 256). **Optimum local** :
solution sans voisin meilleur, mais pas forcément meilleure que toutes les autres ; la descente n'accepte jamais
de dégrader, donc elle ne peut pas en sortir.

**Q16.** Accepter parfois pire permet de **sortir des optima locaux** : T élevée = exploration quasi aléatoire ;
T basse = descente. Refroidissement lent (α=0,995) : meilleurs résultats mais ×10 en itérations
(85 001 contre 1 951). Le voisinage 2-opt est nettement meilleur que l'échange (moyenne 234,0 contre 247-250 pour
α=0,95/0,8 à l'échange), car il conserve les arêtes consécutives et modifie 2 arcs seulement.

**Q17.** Quand la diversité s'effondre (p_mut=0,01 : 2 individus distincts à la fin) la population est faite de
clones : le croisement OX de deux clones redonne le même enfant, seule la mutation peut innover → **convergence
prématurée** vers un optimum local (coût moyen 248,4). p_mut=0,1 donne le meilleur compromis (243,6) ; 0,3
conserve la diversité mais perturbe les bons individus.

**Q18.** Pour 60 monuments Held-Karp est exclu (2⁶⁰). On choisirait **2-opt + recuit simulé** (démarrage
au plus proche voisin, éventuellement Or-opt) : écart ~0 % ici pour quelques dizaines de ms, complexité
polynomiale par itération. L'AG est plus lent et plus sensible aux réglages.

## Partie 4
**Q19.** 10⁸ affectations brutes (8 variables à 10 valeurs), 10!/2! = 1 814 400 si l'on impose « tous différents ».
**Q20/Q21.** 82 solutions. Résultat honnête sur notre instance : pour la **première** solution, aucune variante
ne change grand-chose (9-10 nœuds) car l'ordre statique (PA, PB, CH, DI…) met déjà les variables les plus
contraintes en tête. Pour **toutes** les solutions, le forward checking aide (260 → 187 nœuds) ; MRV+degré
coûte ici *plus* de nœuds (344) car il s'écarte d'un ordre déjà bon et ne sert pas quand il faut parcourir
tout l'arbre. Les heuristiques paient surtout sur des instances plus grosses, mal ordonnées ou insatisfiables.

**Q22.** PA et PB : 3 → 2 valeurs {1,3} ; DI : 7 → 3 ({5,6,7}) ; PT perd la valeur 6 ; les autres inchangés.
**PA = 2** disparaît : PB ∈ {1,2,3} et il faut |PA−PB| ≥ 2 → pour PA=2 il faudrait PB ≤ 0 ou ≥ 4 : aucun
soutien dans D(PB), donc 2 est retiré.

**Q23.** AC-3 renvoie `True` : chaque contrainte prise **deux à deux** a un soutien (CH=4 est compatible avec
BI=5 et TI=5…). Mais BI, TI, CH sont trois valeurs différentes dans {4,5} : impossible (principe des tiroirs),
propriété **globale** que la cohérence d'arc, locale, ne voit pas. Le backtracking le prouve (0 solution, 18
nœuds). Il faudrait une cohérence plus forte (all-different global, cohérence de chemin) ou la recherche.

## Partie 5
**Q24b.** `jouer` renvoie un nouvel état : Minimax/alpha-bêta explorent plusieurs branches depuis le même état ;
modifier l'état exigerait un « défaire » fragile, et on évite les effets de bord/aliasing (et on garde l'historique).

**Q27.** Alpha-bêta coupe quand un coup réfute le précédent ; si le meilleur coup est examiné en premier, alpha
(ou bêta) devient tôt très serré et la plupart des frères sont coupés immédiatement. Dans le meilleur cas :
O(b^(d/2)) au lieu de O(b^d). Mesuré (eval_1, profondeur 5) : 13 950 nœuds Minimax → 482 alpha-bêta → 420
avec tri des captures.

**Q28.** Dans notre tournoi (G = 1234) : 10 nulles sur 10 (score 5-5). Raisons : jeu déterministe à faible
profondeur, plateau 5×5 très encombré, chaque IA voit la recapture à profondeur 3 et évite d'offrir des
captures ; la règle des 60 demi-coups sans prise force alors la nulle. Pistes : profondeurs différentes,
évaluation plus agressive, départage aléatoire des coups équivalents.

## Bonus
Held-Karp : mémoire en O(n·2ⁿ) (71 Mo à n=16, ×4,3 par +2 sur n) → « mur de la **mémoire** ».
Branch and Bound : mémoire négligeable (profondeur de pile ≤ n) mais temps pas borné polynomialement
(factoriel au pire, dépend de la qualité de la borne) → « mur du **temps** ». Sur nos matrices aléatoires
B&B reste plus rapide jusqu'à n=16 (488 ms contre 3,9 s).
