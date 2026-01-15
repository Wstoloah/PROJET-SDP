# Project SDP - CentraleSupélec 2025/2026


## Question 2

cf. [Notebook](Question2.ipynb) pour l'implémentation complète.

### Partie 1 : Démonstration de la non-existence d'une explication (1-1) pour $w \succ w'$

#### Argument simple

Pour la comparaison $w \succ w'$, calculons les ensembles $\texttt{pros}(w, w')$ et $\texttt{cons}(w, w')$ :

- **Scores** :
  - $w$ : [79, 69, 78, 76, 67, 84, 79]
  - $w'$ : [57, 76, 81, 76, 82, 86, 77]

- **Contributions** :
  - $\texttt{pros}(w, w') = \{A: +176, G: +12\}$ (2 cours)
  - $\texttt{cons}(w, w') = \{B: -49, C: -21, E: -90, F: -10\}$ (4 cours)

**Conclusion** : $|\texttt{pros}(w, w')| = 2 < 4 = |\texttt{cons}(w, w')|$

Pour qu'une explication de type (1-1) existe, il faut associer chaque cours dans $\texttt{cons}(w, w')$ à un cours distinct dans $\texttt{pros}(w, w')$. Or, nous avons seulement 2 cours disponibles dans les pros mais 4 cours à couvrir dans les cons. 

**Par le principe des tiroirs**, il est impossible d'établir une telle bijection. Par conséquent, **il n'existe pas d'explication de type (1-1)** pour $w \succ w'$.

---

### Partie 2 : Programme d'optimisation linéaire pour les explications de type (1-m)

#### Rappel de la définition

Un trade-off de type (1-m) est défini par une paire $(P, \{C_1, \ldots, C_m\})$ où :
- $P \in \texttt{pros}(x, y)$
- $C_1, \ldots, C_m \in \texttt{cons}(x, y)$
- La somme des contributions de $P, C_1, \ldots, C_m$ est strictement positive

Une explication de type (1-m) est un ensemble $E = \{(P_1, \mathcal{C}_1), \ldots, (P_\ell, \mathcal{C}_\ell)\}$ de trade-offs disjoints tel que :
$$\bigcup_{i=1}^{\ell} \mathcal{{C}}_i = \texttt{cons}(x, y)$$

#### Formulation mathématique

Soit $P = |\texttt{pros}(x, y)|$ et $C = |\texttt{cons}(x, y)|$.

**Variables de décision** :

- $x_{i,j} \in \{0, 1\}$ : vaut 1 si le cours $C_j \in \texttt{cons}(x, y)$ est associé au cours $P_i \in \texttt{pros}(x, y)$ dans un trade-off
- $y_i \in \{0, 1\}$ : vaut 1 si le cours $P_i \in \texttt{pros}(x, y)$ est utilisé dans l'explication (i.e., fait partie d'un trade-off)

On définit également $w_{i,j} = p_i + c_j$ avec $p_i > 0$ et $c_j < 0$ les contributions respectives des cours $P_i$ et $C_j$.

**Fonction objectif** :

Minimiser le nombre de trade-offs (longueur de l'explication) :
$$\min \sum_{i=1}^{P} y_i$$

**Contraintes** :

1. **Couverture complète des cons** : Chaque cours dans $\texttt{cons}(x,y)$ doit être associé à exactement un cours pro
   $$\forall j \in [1, C], \quad \sum_{i=1}^{P} x_{i,j} = 1$$

2. **Lien entre variables** : Si $x_{i,j} = 1$ pour un certain $j$, alors le cours pro $P_i$ doit être utilisé ($y_i = 1$)
   $$\forall i \in [1, P], \forall j \in [1, C], \quad x_{i,j} \leq y_i$$

3. **Validité des trade-offs (1-m)** : Pour chaque cours pro $P_i$ utilisé, la somme des contributions du pro et de tous les cons qui lui sont associés doit être strictement positive
   $$\forall i \in [1, P], \quad p_i + \sum_{j=1}^{C} x_{i,j} \cdot c_j \geq y_i \cdot \epsilon$$
   
   où $\epsilon > 0$ est une petite constante (par exemple $\epsilon = 0.01$) pour garantir la stricte positivité lorsque $y_i = 1$.

**Certificat de non-existence** :

Si le problème d'optimisation est **infaisable** (INFEASIBLE), alors il n'existe aucune explication de type (1-m) pour la comparaison $x \succ y$. Le certificat est fourni par le solveur d'optimisation qui détecte l'infaisabilité du système de contraintes.

#### Résultats pour $w \succ w'$

L'implémentation trouve une explication de type (1-m) avec un seul trade-off :
$$(A, \{B, C, E, F\}) : 176 + (-170) = 6 > 0$$

Ce trade-off est valide car la somme des contributions est positive, et il couvre tous les cours dans $\texttt{cons}(w, w')$.
