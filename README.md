# IA-PVC

## Mini-Rapport

Les différentes classes :
- City : représente une ville.
- Manager : permet de gérer un tableau de villes.
- Individual : gère les individus, qui sont des villes.
- Population : gère une population, qui est un tableau d'individus.
- GeneticalAlgorithm : implémente l'algorithme génétique (sélection, croisement, mutation, évolution)


La sélection : la sélection par tournois a été implémentée. Cette sélection forme des paires et sélectionne le meilleur individu de chaque paire.

L'opérateur de mutation : La mutation est en fait un échange de deux villes, celles-ci sont choisies aléatoirement.

L'opérateur de croisement : Le croisement en deux points est utilisé. Les deux points sont déterminés aléatoirement.


L'algorithme fonctionne bien. Cependant, pour plus de 50 villes, suivant le premier chemin choisi, aléatoirement, l'algorithme n'arrivera pas à défaire toutes les boucles. Des croisements subsisteront donc. De plus, dans le cas où il est possible d'éliminer tous les croisements, cela va prendre un temps assez long. Cela est dû au grand nombre d’évolution qu’il faudra effectuer afin d’arriver à une solution.
