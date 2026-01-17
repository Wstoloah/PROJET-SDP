# Project SDP - CentraleSupélec 2025/2026


## Question 4

cf. [Notebook](Question4.ipynb) pour l'implémentation complète.

### Partie 1 : Démonstration de la non-existence d'une explication (1-m) ou une explication (m-1) pour $z \succ t$

#### Analyse des contributions

Pour la comparaison $z \succ t$, calculons les ensembles $\texttt{pros}(z, t)$ et $\texttt{cons}(z, t)$ :

- **Scores** :
  - $z$ : [74, 89, 74, 81, 68, 84, 79]
  - $t$ : [74, 71, 84, 91, 77, 76, 73]

- **Contributions** :
  - $\texttt{pros}(z, t) = \{B: +126, F: +40, G: +36\}$ (3 cours)
  - $\texttt{cons}(z, t) =  \{C: -70, D: -60, E: -54\}$ (3 cours)

##### 1.1 Non-existence d'une explication de type (1-m)

Pour qu'une explication de type (1-m) existe, chaque cours pro $P_i$ utilisé doit vérifier la condition de trade-off suivante :

$$p_i + \sum_{C_j \in \mathcal{C}_i} c_j > 0$$

où les ensembles de cons  associés à chaque pro doivent être disjoints et leur union doit couvrir l'intégralité de $\texttt{cons}(z, t)$.

**Vérification exhaustive :**

* **Cours pros F (+40) et G (+36)** :
* Aucun de ces cours ne peut compenser individuellement le plus petit con ($E: -54$)
*  $40 + (-54) = -14 < 0$ et $36 + (-54) = -18 < 0$.
* **Conclusion** :  et  ne peuvent participer à aucun trade-off (1-m) valide.

* **Cours pro B (+126)** :
* Avec  : $\{C, D, E\}$ : $126 + (-70 - 60 - 54) = 126 - 184 = -58 < 0$.
* Avec  : $\{C, D\}$ : $126 + (-70 - 60) = 126 - 130 = -4 < 0$.
* Avec  : $\{C, E\}$ : $126 + (-70 - 54) = 126 - 124 = +2 > 0$(Valide, mais laisse  seul).
* Avec  : $\{D, E\}$ : $126 + (-60 - 54) = 126 - 114 = +12 > 0$ (Valide, mais laisse  seul).



**Analyse** : Le cours  $B$ est le seul pro capable de former un trade-off. S'il couvre deux cons, il reste nécessairement un troisième  con ($C$ ou $D$) qui ne peut être couvert par $F$ ou $G$. Il est donc impossible de couvrir l'intégralité des cons.

**Conclusion** : **Il n'existe pas d'explication de type (1-m)** pour  $z \succ t$.

##### 1.2 Non-existence d'une explication de type (m-1)

Pour une explication de type (m-1), chaque cours con $C_j$ doit être associé à un sous-ensemble de pros $\mathcal{P}_j$ tel que :

$$c_j + \sum_{P_i \in \mathcal{P}_j} p_i > 0$$

**Vérification des capacités de couverture :**

* **Nombre d'arguments nécessaires** : Il y a 3 cours cons distincts ($C, D, E$). Pour une explication (m-1), il est impératif de constituer **3 trade-offs disjoints**.
* **Contrainte de ressources** :
* Pour couvrir **C (-70)**, il faut soit le pro , le pro $\{B\}$, soit le groupe $\{F, G\}$ ($40 + 36 = 76 > 70$).
* Pour couvrir **D (-60)**, il faut soit le pro $\{B\}$, soit le groupe $\{F, G\}$.
* Pour couvrir **E (-54)**, il faut soit le pro $\{B\}$, soit le groupe $\{F, G\}$.


* **Impossibilité de partition** :
* Si nous utilisons le groupe $\{F, G\}$ pour couvrir un con (par exemple $E$), il ne reste que le pro unique $\{B\}$ pour couvrir les deux cons restants ($C$ et $D$).
* Or, dans une explication (m-1), un cours pro ne peut pas être divisé pour servir plusieurs trade-offs disjoints. Le pro $B$ ne peut couvrir qu'un seul des deux cons restants, laissant l'autre orphelin.

**Conclusion** : **Il n'existe pas d'explication de type (m-1)** pour $z \succ t$.

### Partie 2 : Démonstration de l'existence d'une explication combinant des trade-offs de type (m-1) et (1-m)
Pour la comparaison $z \succ t$, nous avons établi précédemment l'absence d'explications pures (1-m) ou (m-1). Cependant, une combinaison est possible.

**Contributions c**:
- $\texttt{pros}(z, t) = \{B: +126, F: +40, G: +36\}$
- $\texttt{cons}(z, t) = \{C: -70, D: -60, E: -54\}$

**Construction d'une explication hybride valide** :

1. **Trade-off (1-m)** : $(B, \{C, E\})$
   - Somme : $126 + (-70) + (-54) = 126 - 124 = +2 > 0$.
   - Ce trade-off est valide et couvre les cours cons C et E en utilisant le pro B.

2. **Trade-off (m-1)** : $(\{F, G\}, D)$
   - Somme : $40 + 36 + (-60) = 76 - 60 = +16 > 0$.
   - Ce trade-off est valide et couvre le cours con restant D en utilisant les pros F et G.

**Conclusion** : L'ensemble $E = \{(B, \{C, E\}), (\{F, G\}, D)\}$ constitue une explication hybride valide. Tous les cours cons sont couverts et chaque cours pro est utilisé au plus une fois.

### Partie 3 : Programme d'optimisation linéaire pour des explications hybrides

L'objectif est de formuler un programme linéaire capable de trouver une explication de la comparaison $x \succ y$ en utilisant une collection de trade-offs disjoints, où chaque trade-off est soit de type (1-m), soit de type (m-1).

#### Formulation mathématique

Soient $P = \texttt{pros}(x, y)$ et $C = \texttt{cons}(x, y)$.

#### Variables de décision
- $assign\_to\_pro_{p,c} \in \{0, 1\}$ : vaut 1 si le cours con $c$ est associé au cours pro $p$ dans un trade-off de type **(1-m)** (où $p$ est le pivot).
- $assign\_to\_con_{p,c} \in \{0, 1\}$ : vaut 1 si le cours pro $p$ est associé au cours con $c$ dans un trade-off de type **(m-1)** (où $c$ est le pivot).
- $pivot\_pro_p \in \{0, 1\}$ : vaut 1 si le cours pro $p$ est le pivot d'un trade-off (1-m).
- $pivot\_con_c \in \{0, 1\}$ : vaut 1 si le cours con $c$ est le pivot d'un trade-off (m-1).

#### Contraintes

1. **Couverture complète des cons** : Chaque cours con $c$ doit être soit un pivot (m-1), soit être assigné à exactement un pivot pro (1-m).
   $$\forall c \in C, \quad pivot\_con_c + \sum_{p \in P} assign\_to\_pro_{p,c} = 1$$

2. **Utilisation unique des pros** : Chaque cours pro $p$ peut être soit un pivot (1-m), soit être assigné à au plus un pivot con (m-1).
   $$\forall p \in P, \quad pivot\_pro_p + \sum_{c \in C} assign\_to\_con_{p,c} \leq 1$$

3. **Lien entre pivots et assignations** :
   - Un pro $p$ ne peut recevoir des cons que s'il est déclaré pivot pro :
     $$\forall p \in P, \quad \sum_{c \in C} assign\_to\_pro_{p,c} \leq |C| \cdot pivot\_pro_p$$
   - Un con $c$ ne peut recevoir des pros que s'il est déclaré pivot con :
     $$\forall c \in C, \quad \sum_{p \in P} assign\_to\_con_{p,c} \leq |P| \cdot pivot\_con_c$$
   - Un pivot con doit avoir au moins un pro associé :
     $$\forall c \in C, \quad \sum_{p \in P} assign\_to\_con_{p,c} \geq pivot\_con_c$$

4. **Validité des trade-offs** :
   - Pour chaque trade-off (1-m) : $p_p + \sum_{c \in C} assign\_to\_pro_{p,c} \cdot c_c \geq \epsilon$
   - Pour chaque trade-off (m-1) : $c_c + \sum_{p \in P} assign\_to\_con_{p,c} \cdot p_p \geq \epsilon$
   (où $\epsilon = 0.01$ pour garantir la positivité stricte).

#### Fonction objectif
Minimiser la complexité de l'explication (nombre total de trade-offs) :
$$\min \sum_{p \in P} pivot\_pro_p + \sum_{c \in C} pivot\_con_c$$

#### Certificat de non-existence
Si le solveur retourne le statut `INFEASIBLE`, cela prouve mathématiquement qu'aucune combinaison de trade-offs de type (1-m) ou (m-1) ne peut couvrir l'ensemble des cours cons.

### Partie 4 : Explication hybride pour a1 et a2: 
