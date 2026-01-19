# Project SDP - CentraleSupélec 2025/2026


## Question 4

cf. [Notebook](Question4.ipynb) pour l'implémentation complète.

### Partie 1 : Démonstration de la non-existence d'une explication (1-m) pour $z \succ t$

#### Analyse des contributions

Pour la comparaison $z \succ t$, calculons les ensembles $\texttt{pros}(z, t)$ et $\texttt{cons}(z, t)$ :

- **Scores** :
  - $z$ : [74, 89, 74, 81, 68, 84, 79]
  - $t$ : [74, 71, 84, 91, 77, 76, 73]

- **Contributions** :
  - $\texttt{pros}(z, t) = \{B: +126, F: +40, G: +36\}$ (3 cours)
  - $\texttt{cons}(z, t) = \{C: -70, D: -60, E: -54\}$ (3 cours)

#### Démonstration de non-existence

Pour qu'une explication de type (1-m) existe, chaque cours pro $P_i$ utilisé doit former un trade-off valide avec un sous-ensemble de cons $\mathcal{C}_i$ :

$$p_i + \sum_{C_j \in \mathcal{C}_i} c_j > 0$$

où les ensembles de cons associés à chaque pro doivent être **disjoints** et leur union doit couvrir l'intégralité de $\texttt{cons}(z, t)$.

**Vérification exhaustive** :

1. **Cours pros F (+40) et G (+36)** :
   - Avec E seul : $40 + (-54) = -14 < 0$ et $36 + (-54) = -18 < 0$
   - Avec D seul : $40 + (-60) = -20 < 0$ et $36 + (-60) = -24 < 0$
   - Avec C seul : $40 + (-70) = -30 < 0$ et $36 + (-70) = -34 < 0$
   - **Conclusion** : F et G ne peuvent former aucun trade-off (1-m) valide individuellement.

2. **Cours pro B (+126)** :
   - Avec $\{C, D, E\}$ : $126 + (-70 - 60 - 54) = -58 < 0$ [X]
   - Avec $\{C, D\}$ : $126 + (-70 - 60) = -4 < 0$ [X]
   - Avec $\{C, E\}$ : $126 + (-70 - 54) = +2 > 0$ (mais laisse D seul)
   - Avec $\{D, E\}$ : $126 + (-60 - 54) = +12 > 0$ (mais laisse C seul)
   - Avec $\{C\}$ seul : $126 + (-70) = +56 > 0$ (mais laisse D et E)
   - Avec $\{D\}$ seul : $126 + (-60) = +66 > 0$ (mais laisse C et E)
   - Avec $\{E\}$ seul : $126 + (-54) = +72 > 0$ (mais laisse C et D)

**Analyse** : Le cours B peut former des trade-offs valides, mais au maximum il peut couvrir 2 cons. Comme F et G ne peuvent former aucun trade-off valide, il est impossible de couvrir les 3 cons avec des trade-offs (1-m) disjoints.

**Conclusion** : **Il n'existe pas d'explication de type (1-m)** pour $z \succ t$.

---

### Partie 2 : Démonstration de la non-existence d'une explication (m-1) pour $z \succ t$

#### Rappel de la définition

Pour une explication de type (m-1), chaque cours con $C_j$ doit être le pivot d'un trade-off associé à un sous-ensemble de pros $\mathcal{P}_j$ :

$$c_j + \sum_{P_i \in \mathcal{P}_j} p_i > 0$$

Les ensembles de pros doivent être **disjoints** et tous les cons doivent être couverts.

#### Vérification des capacités de couverture

Pour couvrir les 3 cours cons ($C, D, E$), nous devons constituer **3 trade-offs (m-1) disjoints**.

**Capacité de couverture de chaque con** :

1. **Con C (-70)** :
   - Avec $\{B\}$ : $-70 + 126 = +56 > 0$ 
   - Avec $\{F, G\}$ : $-70 + 40 + 36 = +6 > 0$ 
   - Avec $\{F\}$ ou $\{G\}$ seul : Insuffisant

2. **Con D (-60)** :
   - Avec $\{B\}$ : $-60 + 126 = +66 > 0$ 
   - Avec $\{F, G\}$ : $-60 + 40 + 36 = +16 > 0$ 
   - Avec $\{F\}$ ou $\{G\}$ seul : Insuffisant

3. **Con E (-54)** :
   - Avec $\{B\}$ : $-54 + 126 = +72 > 0$ 
   - Avec $\{F, G\}$ : $-54 + 40 + 36 = +22 > 0$ 
   - Avec $\{F\}$ ou $\{G\}$ seul : Insuffisant

**Analyse de l'impossibilité** :

Nous avons essentiellement **deux ressources** pour couvrir les 3 cons :
- Le pro $\{B\}$ (fort, peut couvrir n'importe quel con)
- Le groupe $\{F, G\}$ (ensemble, peut couvrir n'importe quel con)

Même en utilisant ces deux ressources optimalement, nous pouvons couvrir au maximum **2 cons**, laissant le troisième con sans couverture valide.

**Conclusion** : **Il n'existe pas d'explication de type (m-1)** pour $z \succ t$.

---

### Partie 3 : Démonstration de l'existence d'une explication hybride pour $z \succ t$

Bien que ni une explication pure (1-m), ni une explication pure (m-1) n'existe, une **combinaison hybride** est possible.

**Construction d'une explication hybride valide** :

1. **Trade-off (1-m)** : $(B, \{C, E\})$
   - Somme : $126 + (-70) + (-54) = +2 > 0$ 
   - Couvre les cons C et E avec le pro B

2. **Trade-off (m-1)** : $(\{F, G\}, D)$
   - Somme : $40 + 36 + (-60) = +16 > 0$ 
   - Couvre le con D avec les pros F et G

**Vérification** :
- Tous les cons sont couverts : $\{C, E\} \cup \{D\} = \{C, D, E\}$ 
- Chaque pro est utilisé au plus une fois : B dans (1-m), F et G dans (m-1) 
- Les trade-offs sont disjoints 

**Conclusion** : L'ensemble $E = \{(B, \{C, E\}), (\{F, G\}, D)\}$ constitue une explication hybride valide pour $z \succ t$.

---

### Partie 4 : Programme d'optimisation linéaire pour des explications hybrides

L'objectif est de formuler un programme linéaire capable de trouver automatiquement une explication hybride de la comparaison $x \succ y$ combinant des trade-offs de types (1-m) et (m-1).

#### Formulation mathématique

Soient $P = |\texttt{pros}(x, y)|$ et $C = |\texttt{cons}(x, y)|$.

**Variables de décision** :

- $assign\_to\_pro_{p,c} \in \{0, 1\}$ : vaut 1 si le cours con $c$ est associé au cours pro $p$ dans un trade-off de type **(1-m)** (où $p$ est le pivot)
- $assign\_to\_con_{p,c} \in \{0, 1\}$ : vaut 1 si le cours pro $p$ est associé au cours con $c$ dans un trade-off de type **(m-1)** (où $c$ est le pivot)
- $pivot\_pro_p \in \{0, 1\}$ : vaut 1 si le cours pro $p$ est le pivot d'un trade-off (1-m)
- $pivot\_con_c \in \{0, 1\}$ : vaut 1 si le cours con $c$ est le pivot d'un trade-off (m-1)

On définit également $p_i > 0$ et $c_j < 0$ les contributions respectives des cours pros et cons.

**Fonction objectif** :

Minimiser le nombre total de trade-offs (complexité de l'explication) :
$$\min \sum_{p=1}^{P} pivot\_pro_p + \sum_{c=1}^{C} pivot\_con_c$$

**Contraintes** :

1. **Couverture complète des cons** : Chaque cours con $c$ doit être soit un pivot (m-1), soit être assigné à exactement un pivot pro (1-m)
   $$\forall c \in [1, C], \quad pivot\_con_c + \sum_{p=1}^{P} assign\_to\_pro_{p,c} = 1$$

2. **Utilisation unique des pros** : Chaque cours pro $p$ peut être soit un pivot (1-m), soit être assigné à au plus un pivot con (m-1)
   $$\forall p \in [1, P], \quad pivot\_pro_p + \sum_{c=1}^{C} assign\_to\_con_{p,c} \leq 1$$

3. **Lien entre pivots et assignations** : Les assignations ne peuvent exister que si les pivots correspondants sont actifs
   $$\forall p \in [1, P], \forall c \in [1, C], \quad assign\_to\_pro_{p,c} \leq pivot\_pro_p$$
   $$\forall p \in [1, P], \forall c \in [1, C], \quad assign\_to\_con_{p,c} \leq pivot\_con_c$$

4. **Participation minimale** : Un pivot doit avoir au moins un élément associé
   $$\forall p \in [1, P], \quad \sum_{c=1}^{C} assign\_to\_pro_{p,c} \geq pivot\_pro_p$$
   $$\forall c \in [1, C], \quad \sum_{p=1}^{P} assign\_to\_con_{p,c} \geq pivot\_con_c$$

5. **Validité des trade-offs (1-m)** : Pour chaque trade-off (1-m), la somme doit être strictement positive
   $$\forall p \in [1, P], \quad p_p + \sum_{c=1}^{C} assign\_to\_pro_{p,c} \cdot c_c \geq pivot\_pro_p \cdot \epsilon $$

6. **Validité des trade-offs (m-1)** : Pour chaque trade-off (m-1), la somme doit être strictement positive
   $$\forall c \in [1, C], \quad c_c + \sum_{p=1}^{P} assign\_to\_con_{p,c} \cdot p_p \geq pivot\_con_c \cdot \epsilon - (1 - pivot\_con_c) \cdot M$$

où $\epsilon = 0.01$ garantit la stricte positivité et $M$ est une grande constante (Big-M).

**Calcul dynamique de Big-M** :

Pour éviter les problèmes numériques, on calcule $M$ adapté aux données :
$$M = \sum_{c=1}^{C} |c_c| + 1$$

**Certificat de non-existence** :

Si le solveur retourne le statut `INFEASIBLE`, cela prouve mathématiquement qu'aucune combinaison de trade-offs de type (1-m) ou (m-1) ne peut couvrir l'ensemble des cours cons.

---

### Partie 5 : Application aux candidats a1 et a2

Pour la comparaison $a_1 \succ a_2$ :

- **Scores** :
  - $a_1$ : [89, 74, 81, 68, 84, 79, 77]
  - $a_2$ : [71, 84, 91, 79, 78, 73.5, 77]

- **Contributions** :
  - $\texttt{pros}(a_1, a_2) = \{A: +144, C: -70, E: +36, F: +27.5\}$
  - $\texttt{cons}(a_1, a_2) = \{B: -70, D: -66\}$

**Résultat de l'optimisation** :

Le programme linéaire hybride retourne le statut **INFEASIBLE**, ce qui constitue un certificat formel de non-existence.

**Interprétation** :

Bien que $a_1$ ait une moyenne pondérée supérieure à $a_2$, cette supériorité ne peut être expliquée par une combinaison de trade-offs (1-m) et (m-1). L'avantage de $a_1$ provient d'un équilibre global complexe qui dépasse la logique des explications structurées recherchées.

Plus précisément :
- Le fort avantage en Anatomie (A: +144) de $a_1$ est presque entièrement neutralisé en couvrant les deux désavantages en Biologie (B: -70) et Diagnostic (D: -66)
- Les avantages restants (E: +36, F: +27.5) sont insuffisants face aux contraintes de disjonction
- Il n'existe aucune partition des pros et cons permettant de former des trade-offs valides et disjoints

**Conclusion** : **Il n'existe pas d'explication hybride (1-m)/(m-1)** pour $a_1 \succ a_2$. 
