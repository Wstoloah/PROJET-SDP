"""
SDP Project - Trade-off Explanation Solver
Supports (1-1), (1-m), (m-1), and hybrid explanations
"""

from gurobipy import Model, GRB, quicksum
from typing import Union, List, Dict, Tuple

# Global weights for the 7 features
WEIGHTS = [0.021, 0.188, 0.038, 0.322, 16.124, 67.183, 16.124]
FEATURES = ["A", "B", "C", "D", "E", "F", "G"]
EPSILON = 0.01
BIG_M = 10000


def compute_pros_and_cons(record1: List[float], record2: List[float]) -> Tuple[Dict[int, float], Dict[int, float]]:
    """
    Compute pros(record1, record2) and cons(record1, record2).
    
    Returns:
        pros: dict mapping feature index -> positive weighted contribution
        cons: dict mapping feature index -> negative weighted contribution
    """
    assert len(record1) == len(record2) == len(WEIGHTS), "Records must have 7 features"
    
    pros = {
        i: (record1[i] - record2[i]) * WEIGHTS[i]
        for i in range(len(record1))
        if (record1[i] - record2[i]) > 0
    }
    
    cons = {
        i: (record1[i] - record2[i]) * WEIGHTS[i]
        for i in range(len(record1))
        if (record1[i] - record2[i]) < 0
    }
    
    return pros, cons


def print_contribution_table(record1: List[float], record2: List[float]) -> None:
    """
    Print a table showing weighted differences between two records.
    """
    print("\n" + "=" * 80)
    print("WEIGHTED CONTRIBUTION TABLE (Record 1 - Record 2)")
    print("=" * 80)
    
    # Header
    header = "|"
    separator = "|"
    for feature in FEATURES:
        header += f"   {feature}    |"
        separator += "---------|"
    print(header)
    print(separator)
    
    # Values
    values = "|"
    for i in range(len(WEIGHTS)):
        diff = (record1[i] - record2[i]) * WEIGHTS[i]
        values += f" {diff:+7.3f} |"
    print(values)
    
    # Summary
    total = sum((record1[i] - record2[i]) * WEIGHTS[i] for i in range(len(WEIGHTS)))
    print(separator)
    print(f"\nTotal weighted difference: {total:+.3f}")
    
    if total > 0:
        print("[✓] Record 1 is preferred to Record 2 (positive total)")
    elif total < 0:
        print("[✗] Record 2 is preferred to Record 1 (negative total)")
    else:
        print("[=] Records are equivalent (zero total)")
    print()


def solve_1m_explanation(pros: Dict[int, float], cons: Dict[int, float], verbose: bool = True) -> dict:
    """
    Solve for (1-m) explanation: one pro covers multiple cons.
    Each pro can be a pivot covering multiple cons, and each con must be assigned to exactly one pro.
    """
    if not pros or not cons:
        return {"status": "trivial", "message": "No pros or cons to explain"}
    
    m = Model("1-m_Explanation")
    m.setParam('OutputFlag', 0)
    
    # Variables
    # x[p,c] = 1 if con c is assigned to pro p
    VarX = {(p, c): m.addVar(vtype=GRB.BINARY, name=f'x_{p}_{c}')
            for p in pros for c in cons}
    
    # y[p] = 1 if pro p is used as a pivot
    VarY = {p: m.addVar(vtype=GRB.BINARY, name=f'y_{p}')
            for p in pros}
    
    # Constraints
    # 1. Every con must be assigned to exactly one pro
    for c in cons:
        m.addConstr(quicksum(VarX[(p, c)] for p in pros) == 1, name=f"con_coverage_{c}")
    
    # 2. If a con is assigned to a pro, that pro must be used
    for p in pros:
        for c in cons:
            m.addConstr(VarX[(p, c)] <= VarY[p], name=f"link_{p}_{c}")
    
    # 3. Trade-off validity: pro contribution + sum of assigned cons >= epsilon (if pro is used)
    for p in pros:
        m.addConstr(
            pros[p] + quicksum(VarX[(p, c)] * cons[c] for c in cons) >= VarY[p] * EPSILON,
            name=f"validity_{p}"
        )
    
    # Objective: minimize number of trade-offs (pros used)
    m.setObjective(quicksum(VarY[p] for p in pros), GRB.MINIMIZE)
    
    m.optimize()
    
    result = {"type": "1-m", "status": None, "tradeoffs": [], "num_tradeoffs": 0}
    
    if m.status == GRB.OPTIMAL:
        result["status"] = "optimal"
        result["num_tradeoffs"] = int(m.objVal)
        
        for p in pros:
            if VarY[p].X > 0.5:
                associated_cons = [c for c in cons if VarX[(p, c)].X > 0.5]
                total = pros[p] + sum(cons[c] for c in associated_cons)
                result["tradeoffs"].append({
                    "pro": p,
                    "cons": associated_cons,
                    "pro_contribution": pros[p],
                    "cons_contributions": {c: cons[c] for c in associated_cons},
                    "total": total
                })
        
        if verbose:
            print_1m_results(result)
    
    elif m.status == GRB.INFEASIBLE:
        result["status"] = "infeasible"
        if verbose:
            print("\n[!] No (1-m) explanation exists for this comparison.")
    
    return result


def solve_m1_explanation(pros: Dict[int, float], cons: Dict[int, float], verbose: bool = True) -> dict:
    """
    Solve for (m-1) explanation: multiple pros cover one con.
    Each con is a pivot, and multiple pros can be assigned to cover it.
    """
    if not pros or not cons:
        return {"status": "trivial", "message": "No pros or cons to explain"}
    
    m = Model("m-1_Explanation")
    m.setParam('OutputFlag', 0)
    
    # Variables
    # x[p,c] = 1 if pro p is assigned to con c
    VarX = {(p, c): m.addVar(vtype=GRB.BINARY, name=f'x_{p}_{c}')
            for p in pros for c in cons}
    
    # Constraints
    # 1. Each pro can be assigned to at most one con
    for p in pros:
        m.addConstr(quicksum(VarX[(p, c)] for c in cons) <= 1, name=f"pro_usage_{p}")
    
    # 2. Each con must have at least one pro assigned
    for c in cons:
        m.addConstr(quicksum(VarX[(p, c)] for p in pros) >= 1, name=f"con_coverage_{c}")
    
    # 3. Trade-off validity: sum of assigned pros + con contribution >= epsilon
    for c in cons:
        m.addConstr(
            quicksum(VarX[(p, c)] * pros[p] for p in pros) + cons[c] >= EPSILON,
            name=f"validity_{c}"
        )
    
    # Objective: minimize total number of pros used
    m.setObjective(quicksum(VarX[(p, c)] for p in pros for c in cons), GRB.MINIMIZE)
    
    m.optimize()
    
    result = {"type": "m-1", "status": None, "tradeoffs": [], "num_pros_used": 0}
    
    if m.status == GRB.OPTIMAL:
        result["status"] = "optimal"
        result["num_pros_used"] = int(m.objVal)
        
        for c in cons:
            associated_pros = [p for p in pros if VarX[(p, c)].X > 0.5]
            if associated_pros:
                total = sum(pros[p] for p in associated_pros) + cons[c]
                result["tradeoffs"].append({
                    "con": c,
                    "pros": associated_pros,
                    "pros_contributions": {p: pros[p] for p in associated_pros},
                    "con_contribution": cons[c],
                    "total": total
                })
        
        if verbose:
            print_m1_results(result)
    
    elif m.status == GRB.INFEASIBLE:
        result["status"] = "infeasible"
        if verbose:
            print("\n[!] No (m-1) explanation exists for this comparison.")
    
    return result


def solve_hybrid_explanation(pros: Dict[int, float], cons: Dict[int, float], verbose: bool = True) -> dict:
    """
    Solve for hybrid explanation: combination of (1-m) and (m-1) trade-offs.
    """
    if not pros or not cons:
        return {"status": "trivial", "message": "No pros or cons to explain"}
    
    m = Model("Hybrid_Explanation")
    m.setParam('OutputFlag', 0)
    
    # Variables
    # Assignment variables
    VarAssignPro = {(p, c): m.addVar(vtype=GRB.BINARY, name=f'atp_{p}_{c}')
                    for p in pros for c in cons}
    VarAssignCon = {(p, c): m.addVar(vtype=GRB.BINARY, name=f'atc_{p}_{c}')
                    for p in pros for c in cons}
    
    # Pivot variables
    VarPivotPro = {p: m.addVar(vtype=GRB.BINARY, name=f'piv_p_{p}') for p in pros}
    VarPivotCon = {c: m.addVar(vtype=GRB.BINARY, name=f'piv_c_{c}') for c in cons}
    
    # Constraints
    # 1. Every con must be covered exactly once (either as m-1 pivot or assigned to 1-m pivot)
    for c in cons:
        m.addConstr(
            VarPivotCon[c] + quicksum(VarAssignPro[(p, c)] for p in pros) == 1,
            name=f"con_coverage_{c}"
        )
    
    # 2. Every pro can be used at most once (either as 1-m pivot or assigned to m-1 pivot)
    for p in pros:
        m.addConstr(
            VarPivotPro[p] + quicksum(VarAssignCon[(p, c)] for c in cons) <= 1,
            name=f"pro_usage_{p}"
        )
    
    # 3. Linking constraints
    for p in pros:
        for c in cons:
            m.addConstr(VarAssignPro[(p, c)] <= VarPivotPro[p], name=f"link_atp_{p}_{c}")
            m.addConstr(VarAssignCon[(p, c)] <= VarPivotCon[c], name=f"link_atc_{p}_{c}")
    
    # 4. Trade-off validity with Big-M
    for p in pros:
        m.addConstr(
            pros[p] + quicksum(VarAssignPro[(p, c)] * cons[c] for c in cons)
            >= VarPivotPro[p] * EPSILON - (1 - VarPivotPro[p]) * BIG_M,
            name=f"validity_1m_{p}"
        )
    
    for c in cons:
        m.addConstr(
            cons[c] + quicksum(VarAssignCon[(p, c)] * pros[p] for p in pros)
            >= VarPivotCon[c] * EPSILON - (1 - VarPivotCon[c]) * BIG_M,
            name=f"validity_m1_{c}"
        )
    
    # Objective: minimize total number of pivots
    m.setObjective(
        quicksum(VarPivotPro[p] for p in pros) + quicksum(VarPivotCon[c] for c in cons),
        GRB.MINIMIZE
    )
    
    m.optimize()
    
    result = {
        "type": "hybrid",
        "status": None,
        "tradeoffs_1m": [],
        "tradeoffs_m1": [],
        "num_pivots": 0
    }
    
    if m.status == GRB.OPTIMAL:
        result["status"] = "optimal"
        result["num_pivots"] = int(m.objVal)
        
        # Extract (1-m) trade-offs
        for p in pros:
            if VarPivotPro[p].X > 0.5:
                associated_cons = [c for c in cons if VarAssignPro[(p, c)].X > 0.5]
                total = pros[p] + sum(cons[c] for c in associated_cons)
                result["tradeoffs_1m"].append({
                    "pro": p,
                    "cons": associated_cons,
                    "pro_contribution": pros[p],
                    "cons_contributions": {c: cons[c] for c in associated_cons},
                    "total": total
                })
        
        # Extract (m-1) trade-offs
        for c in cons:
            if VarPivotCon[c].X > 0.5:
                associated_pros = [p for p in pros if VarAssignCon[(p, c)].X > 0.5]
                total = sum(pros[p] for p in associated_pros) + cons[c]
                result["tradeoffs_m1"].append({
                    "con": c,
                    "pros": associated_pros,
                    "pros_contributions": {p: pros[p] for p in associated_pros},
                    "con_contribution": cons[c],
                    "total": total
                })
        
        if verbose:
            print_hybrid_results(result)
    
    elif m.status == GRB.INFEASIBLE:
        result["status"] = "infeasible"
        if verbose:
            print("\n[!] No hybrid explanation exists for this comparison.")
            print("    Certificate of non-existence established.")
    
    return result


def print_1m_results(result: dict) -> None:
    """Pretty print (1-m) explanation results."""
    print("\n" + "=" * 80)
    print("OPTIMAL (1-m) EXPLANATION FOUND!")
    print("=" * 80)
    print(f"\nMinimum number of trade-offs: {result['num_tradeoffs']}")
    print("\n" + "-" * 80)
    print("TRADE-OFFS:")
    print("-" * 80)
    
    for to in result["tradeoffs"]:
        pro_name = FEATURES[to["pro"]]
        cons_names = [FEATURES[c] for c in to["cons"]]
        
        print(f"\n  Trade-off: ({pro_name}, {{{', '.join(cons_names)}}})")
        print(f"    - Pro contribution [{pro_name}]: {to['pro_contribution']:+.3f}")
        for c in to["cons"]:
            print(f"    - Con contribution [{FEATURES[c]}]: {to['cons_contributions'][c]:+.3f}")
        print(f"    - Total: {to['total']:+.3f}")
        print(f"    - Valid: {to['total'] > 0}")


def print_m1_results(result: dict) -> None:
    """Pretty print (m-1) explanation results."""
    print("\n" + "=" * 80)
    print("OPTIMAL (m-1) EXPLANATION FOUND!")
    print("=" * 80)
    print(f"\nTotal pros used: {result['num_pros_used']}")
    print("\n" + "-" * 80)
    print("TRADE-OFFS:")
    print("-" * 80)
    
    for to in result["tradeoffs"]:
        con_name = FEATURES[to["con"]]
        pros_names = [FEATURES[p] for p in to["pros"]]
        
        print(f"\n  Trade-off: ({{{', '.join(pros_names)}}}, {con_name})")
        for p in to["pros"]:
            print(f"    - Pro contribution [{FEATURES[p]}]: {to['pros_contributions'][p]:+.3f}")
        print(f"    - Con contribution [{con_name}]: {to['con_contribution']:+.3f}")
        print(f"    - Total: {to['total']:+.3f}")
        print(f"    - Valid: {to['total'] > 0}")


def print_hybrid_results(result: dict) -> None:
    """Pretty print hybrid explanation results."""
    print("\n" + "=" * 80)
    print("OPTIMAL HYBRID EXPLANATION FOUND!")
    print("=" * 80)
    print(f"\nMinimum number of pivots: {result['num_pivots']}")
    
    if result["tradeoffs_1m"]:
        print("\n" + "-" * 80)
        print("(1-m) TRADE-OFFS:")
        print("-" * 80)
        for to in result["tradeoffs_1m"]:
            pro_name = FEATURES[to["pro"]]
            cons_names = [FEATURES[c] for c in to["cons"]]
            
            print(f"\n  Trade-off: ({pro_name}, {{{', '.join(cons_names)}}})")
            print(f"    - Pro contribution [{pro_name}]: {to['pro_contribution']:+.3f}")
            for c in to["cons"]:
                print(f"    - Con contribution [{FEATURES[c]}]: {to['cons_contributions'][c]:+.3f}")
            print(f"    - Total: {to['total']:+.3f}")
    
    if result["tradeoffs_m1"]:
        print("\n" + "-" * 80)
        print("(m-1) TRADE-OFFS:")
        print("-" * 80)
        for to in result["tradeoffs_m1"]:
            con_name = FEATURES[to["con"]]
            pros_names = [FEATURES[p] for p in to["pros"]]
            
            print(f"\n  Trade-off: ({{{', '.join(pros_names)}}}, {con_name})")
            for p in to["pros"]:
                print(f"    - Pro contribution [{FEATURES[p]}]: {to['pros_contributions'][p]:+.3f}")
            print(f"    - Con contribution [{con_name}]: {to['con_contribution']:+.3f}")
            print(f"    - Total: {to['total']:+.3f}")


def find_explanation(
    record1: List[float],
    record2: List[float],
    explanation_type: Union[str, List[str]] = "1-m",
    verbose: bool = True
) -> dict:
    """
    Find an explanation for why record1 is preferred to record2.
    
    Args:
        record1: First record (list of 7 feature values)
        record2: Second record (list of 7 feature values)
        explanation_type: Type of explanation to find:
            - "1-m": One pro covers multiple cons
            - "m-1": Multiple pros cover one con
            - ["1-m", "m-1"]: Hybrid (combination of both)
        verbose: Whether to print detailed output
    
    Returns:
        Dictionary containing the explanation result
    """
    assert len(record1) == len(record2) == 7, "Records must have exactly 7 features"
    
    # Print contribution table
    if verbose:
        print_contribution_table(record1, record2)
    
    # Compute pros and cons
    pros, cons = compute_pros_and_cons(record1, record2)
    
    if verbose:
        print("=" * 80)
        print("PROS AND CONS ANALYSIS")
        print("=" * 80)
        print(f"\nPros (positive contributions):")
        for idx, val in pros.items():
            print(f"  {FEATURES[idx]}: {val:+.3f}")
        print(f"\nCons (negative contributions):")
        for idx, val in cons.items():
            print(f"  {FEATURES[idx]}: {val:+.3f}")
    
    # Check if comparison is valid
    total = sum(pros.values()) + sum(cons.values())
    if total <= 0:
        if verbose:
            print(f"\n[!] Record 1 is NOT preferred to Record 2 (total: {total:+.3f})")
            print("    No explanation needed/possible.")
        return {"status": "not_preferred", "message": "Record 1 is not preferred to Record 2"}
    
    if not cons:
        if verbose:
            print("\n[✓] Trivial explanation: Record 1 dominates Record 2 in all features where they differ.")
        return {"status": "trivial", "message": "Record 1 dominates Record 2"}
    
    # Determine which solver to use
    if isinstance(explanation_type, list):
        # Hybrid explanation
        if verbose:
            print("\n" + "=" * 80)
            print("SOLVING FOR HYBRID EXPLANATION (1-m + m-1)")
            print("=" * 80)
        return solve_hybrid_explanation(pros, cons, verbose)
    
    elif explanation_type == "1-m":
        if verbose:
            print("\n" + "=" * 80)
            print("SOLVING FOR (1-m) EXPLANATION")
            print("=" * 80)
        return solve_1m_explanation(pros, cons, verbose)
    
    elif explanation_type == "m-1":
        if verbose:
            print("\n" + "=" * 80)
            print("SOLVING FOR (m-1) EXPLANATION")
            print("=" * 80)
        return solve_m1_explanation(pros, cons, verbose)
    
    else:
        raise ValueError(f"Unknown explanation type: {explanation_type}")


# Example usage
if __name__ == "__main__":
    # Example records
    record1 = [85, 81, 71, 69, 75, 81, 88]
    record2 = [81, 81, 75, 63, 67, 88, 95]
    
    print("\n" + "#" * 80)
    print("# EXAMPLE: Testing (1-m) explanation")
    print("#" * 80)
    result = find_explanation(record1, record2, explanation_type="1-m")
    
    print("\n" + "#" * 80)
    print("# EXAMPLE: Testing (m-1) explanation")
    print("#" * 80)
    result = find_explanation(record1, record2, explanation_type="m-1")
    
    print("\n" + "#" * 80)
    print("# EXAMPLE: Testing hybrid explanation")
    print("#" * 80)
    result = find_explanation(record1, record2, explanation_type=["1-m", "m-1"])
