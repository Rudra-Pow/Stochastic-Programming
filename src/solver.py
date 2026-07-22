from scenario import Scenario
import numpy as np
import gurobipy as gp
from gurobipy import GRB


class Solver:
    def __init__(self, c, scenarios, A_ub=None, b_ub=None):
        self.c = np.asarray(c, dtype=float)
        self.scenarios = scenarios

        # inequality constraints
        self.A_ub = np.asarray(A_ub, dtype=float) if A_ub is not None and len(A_ub) > 0 else None
        self.b_ub = np.asarray(b_ub, dtype=float) if b_ub is not None and len(b_ub) > 0 else None

        # Sanity check on probabilities
        total_prob = sum(s.prob for s in self.scenarios)
        if not np.isclose(total_prob, 1.0):
            raise ValueError(f"Scenario probabilities sum to {total_prob:.4f}, expected 1.0")

    # Solves via deterministic equivalent form
    def solve_deterministic_equivalent(self):
        model = gp.Model("deterministic_equivalent")
        model.Params.OutputFlag = 0

        # First-stage decision variables
        x = model.addMVar(shape=len(self.c), lb=0.0, name="x")

        # First-stage constraints
        if self.A_ub is not None:
            model.addConstr(self.A_ub @ x <= self.b_ub, name="ub_constr")

        # Second-stage decision variables and constraints
        y_vars = []
        expected_recourse_cost = 0

        for i, s in enumerate(self.scenarios):
            y = model.addMVar(shape=len(s.q), lb=0.0, name=f"y_{i}")
            y_vars.append(y)

            # Constraint: W @ y >= h - T @ x  (Standardized to inequality)
            model.addConstr(s.W @ y >= s.h - s.T @ x, name=f"recourse_{i}")

            # Accumulate objective
            expected_recourse_cost += s.prob * (s.q @ y)

        model.setObjective(self.c @ x + expected_recourse_cost, GRB.MINIMIZE)
        model.optimize()

        if model.Status == GRB.OPTIMAL:
            return {
                "status": "optimal",
                "optimal_cost": model.ObjVal,
                "x": x.X,
                "y": [y_var.X for y_var in y_vars]
            }
        else:
            raise RuntimeError(f"Optimization failed. Gurobi status: {model.Status}")
    #Benders via multi cut
    def solve_benders(self):
        pass
