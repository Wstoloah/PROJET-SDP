# Project SDP - CentraleSupélec 2025


## Question 1

cf. [Notebook](Question1.ipynb) pour l'implémentation complète.

### Modélisation

Soit $P = |\texttt{pros}(x, y)$| et $C = |\texttt{cons}(x, y)$| <br>

On définit $X \in \{0, 1\}^{P \times C}$ tel que :


$$ x_{i, j} = \begin{cases} 1 & \text{si } (P_i, C_j) \text{ appartient à l'explication E du type (1-1)} \\ 0 & \text{sinon} \end{cases} $$

On définit également la matrice constante $W \in \mathbb{Z}^{P \times C}$ telle que :

$$ w_{i, j} = p_i + c_j $$

avec $p_i > 0$ et $c_j < 0$ les contributions respectives des cours $P_i$ et $C_j$.

L'objectif est de minimiser la fonction suivante :
$$ \min \sum_{i=1}^{P} \sum_{j=1}^{C} x_{i, j} w_{i, j} $$

Contraintes :

1. Chaque cours $C_i \in \texttt{cons}(x, y)$ doit être associé à un et un seul trade-off du type (1-1) :
    $$ \forall j \in [1, C], \sum_{i=1}^{P} x_{i, j} = 1 $$

2. Chaque cours $P_i \in \texttt{pros}(x, y)$ doit être associé à au plus un trade-off du type (1-1) :
    $$ \forall i \in [1, P], \sum_{j=1}^{C} x_{i, j} \leq 1 $$

3. Un pair $(P_i, C_j)$ ne peut être sélectionné que si le trade-off $(P_i, C_j)$ est valide :
    $$ \forall i \in [1, P], \forall j \in [1, C], x_{i, j} w_{i, j} \geq 0 $$
