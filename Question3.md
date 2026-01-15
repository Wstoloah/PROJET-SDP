# Project SDP - CentraleSupélec 2025/2026


## Question 3

cf. [Notebook](Question3.ipynb) pour l'implémentation complète.

### Partie 1 : Démonstration de la non-existence d'une explication (1-m) pour $u \succ v$

#### Analyse des contributions

Pour la comparaison $u \succ v$, calculons les ensembles $\texttt{pros}(u, v)$ et $\texttt{cons}(u, v)$ :

- **Scores** :
  - $u$ : [72, 75, 66, 85, 88, 66, 93]
  - $v$ : [71, 73, 63, 92, 76, 79, 93]

- **Contributions** :
  - $\texttt{pros}(u, v) = \{A: +8, B: +14, C: +21, E: +72\}$ (4 cours)
  - $\texttt{cons}(u, v) = \{D: -42, F: -65\}$ (2 cours)

#### Démonstration de non-existence

Pour qu'une explication de type (1-m) existe, chaque cours pro doit former un trade-off valide avec un sous-ensemble de cons. Autrement dit, pour chaque cours pro $P_i$ utilisé :

$$p_i + \sum_{C_j \in \mathcal{C}_i} c_j > 0$$

où $\mathcal{C}_i \subseteq \texttt{cons}(u, v)$ est l'ensemble des cons associés à $P_i$.

**Vérification exhaustive** :

1. **Cours pro A (+8)** :
   - Avec D : $8 + (-42) = -34 < 0$ 
   - Avec F : $8 + (-65) = -57 < 0$ 
   - Avec D et F : $8 + (-42) + (-65) = -99 < 0$ 

2. **Cours pro B (+14)** :
   - Avec D : $14 + (-42) = -28 < 0$ 
   - Avec F : $14 + (-65) = -51 < 0$ 
   - Avec D et F : $14 + (-42) + (-65) = -93 < 0$ 

3. **Cours pro C (+21)** :
   - Avec D : $21 + (-42) = -21 < 0$ 
   - Avec F : $21 + (-65) = -44 < 0$ 
   - Avec D et F : $21 + (-42) + (-65) = -86 < 0$ 

4. **Cours pro E (+72)** :
   - Avec D : $72 + (-42) = +30 > 0$ 
   - Avec F : $72 + (-65) = +7 > 0$ 
   - Avec D et F : $72 + (-42) + (-65) = -35 < 0$

**Analyse** : Le cours E peut former un trade-off valide avec D **ou** avec F, mais pas avec les deux simultanément. Or, pour qu'une explication (1-m) existe, tous les cons doivent être couverts. Il est impossible de couvrir à la fois D et F avec les pros disponibles en utilisant des trade-offs (1-m) valides.

**Conclusion** : **Il n'existe pas d'explication de type (1-m)** pour $u \succ v$.

---

### Partie 2 : Trade-offs de type (m-1)

#### Définition

Un trade-off de type (m-1) est défini par une paire $(\{P_1, \ldots, P_m\}, C)$ où :
- $P_1, \ldots, P_m \in \texttt{pros}(x, y)$
- $C \in \texttt{cons}(x, y)$
- La somme des contributions de $P_1, \ldots, P_m$ et $C$ est strictement positive

Par exemple, $(\{A, B, C\}, D)$ est un trade-off de type (3-1) dans $u \succ v$.

Une explication de type (m-1) de l'affirmation $x \succ y$ est définie par l'ensemble $E = \{(\mathcal{P}_1, C_1), \ldots, (\mathcal{P}_\ell, C_\ell)\}$ de trade-offs (m-1) disjoints tel que :
$$\bigcup_{i=1}^{\ell} \{C_i\} = \texttt{cons}(x, y)$$

Autrement dit, **tous les cons doivent être couverts**.

---

### Partie 3 : Programme d'optimisation linéaire pour les explications de type (m-1)

#### Formulation mathématique

Soit $P = |\texttt{pros}(x, y)|$ et $C = |\texttt{cons}(x, y)|$.

**Variables de décision** :

- $x_{p,c} \in \{0, 1\}$ : vaut 1 si le cours $P_p \in \texttt{pros}(x, y)$ est associé au cours $C_c \in \texttt{cons}(x, y)$ dans un trade-off

On définit également $p_i > 0$ et $c_j < 0$ les contributions respectives des cours $P_i$ et $C_j$.

**Fonction objectif** :

Minimiser le nombre total de pros utilisés dans l'explication :
$$\min \sum_{p=1}^{P} \sum_{c=1}^{C} x_{p,c}$$

**Contraintes** :

1. **Participation optionnelle des pros** : Chaque cours pros peut être associé à au plus un cours cons
   $$\forall p \in [1, P], \quad \sum_{c=1}^{C} x_{p,c} \leq 1$$

2. **Couverture complète des cons** : Chaque cours cons doit avoir au moins un pros associé
   $$\forall c \in [1, C], \quad \sum_{p=1}^{P} x_{p,c} \geq 1$$

3. **Validité des trade-offs (m-1)** : Pour chaque cours cons $C_c$, la somme des contributions de tous les pros qui lui sont associés et du cons lui-même doit être strictement positive
   $$\forall c \in [1, C], \quad \sum_{p=1}^{P} x_{p,c} \cdot p_p + c_c \geq \epsilon$$
   
   où $\epsilon > 0$ est une petite constante (par exemple $\epsilon = 0.01$) pour garantir la stricte positivité.

**Certificat de non-existence** :

Si le problème d'optimisation est **infaisable** (INFEASIBLE), alors il n'existe aucune explication de type (m-1) pour la comparaison $x \succ y$. Le certificat est fourni par le solveur d'optimisation qui détecte l'infaisabilité du système de contraintes.

---

### Partie 4 : Explication de type (m-1) pour $y \succ z$

Pour la comparaison $y \succ z$ :

- **Scores** :
  - $y$ : [81, 81, 75, 63, 67, 88, 95]
  - $z$ : [74, 89, 74, 81, 68, 84, 79]

- **Contributions** :
  - $\texttt{pros}(y, z) = \{A: +56, C: +7, G: +96\}$ (3 cours)
  - $\texttt{cons}(y, z) = \{B: -56, D: -108, E: -6, F: +20\}$ (4 cours, mais F est positif donc sera dans pros)

L'implémentation du programme linéaire trouve une explication de type (m-1) pour cette comparaison.
