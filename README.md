<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

# Projet de recherche Opérationnelle (one machine sequencing problem)

## Description du problème

Nous aurons un ensemble $ N = \{ 1,\dots,n \} $ de n tâche à affecter à une machine.

Pour chaque tâche $i \in N$, nous aurons une date $a_i$, tel que la tâche i ne pourra pas commencer avant cette date.

Pour chaque tâche i, nous aurons la durée $d_i$, qui est la durée passée sur la machine et la durée $q_i$, qui est la durée pendant laquelle l'objet reste dans le système, mais n'utilise pas la machine. la tâche i, se terminera au temps $t+d_i+q_i$, mais la machine sera utilisable à partir de $t+d_i$

Notre objectif est de minimiser le temps de travail, donc de minimiser le temps où la **dernière machine** aura fini de tourner.

## Travail sur le sujet

Le but est de mettre en place un algorithme de branch and bound. Nous aurons deux types d'algorithmes de branch and bound à coder.

* Le premier algorithme se basera sur la technique de **Schrage** pour trouver des bornes supérieures et inférieures à chaque noeud de branchement. Tout sera passée sur cette procédure de Schrage. A chaque noeuds nous aurons à faire cette procédure et un critère nous permettra de brancher.

* un second algorithme de branch and bound pourra se baser sur de la programmation mixte. C'est en fait la version classique de cet algorithme. A chaque noeuds on considère une relaxation linéaire, que l'on résoud (algorithme du simplexe/simplexe dual).





