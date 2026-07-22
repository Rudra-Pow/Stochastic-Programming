from solver import Solver, Scenario
import pandas as pd

# function to solve the farmers example in John R. Birge Introduction to Stochastic Programming
def farmer(c, A_ub, b_ub, q_base, W_base, h_base, scenarios_data, p, output_filename="farmer_results.xlsx"):
    scenarios = []

    # get the technology matrix
    for s in scenarios_data:
        T_s = [
            [s["yield_w"], 0.0, 0.0],
            [0.0, s["yield_c"], 0.0],
            [0.0, 0.0, s["yield_b"]],
            [0.0, 0.0, 0.0]
        ]
        scenarios.append(Scenario(prob=p, q=q_base, h=h_base, T=T_s, W=W_base))

    farmer_model = Solver(c=c, A_ub=A_ub, b_ub=b_ub, scenarios=scenarios)
    res = farmer_model.solve_deterministic_equivalent()

    # clean up small floating point numbers
    def fmt(val):
        if abs(val) < 0.001:
            return "-"
        return int(round(val))

    x = res['x']
    data = []

    # first stage variables
    data.append(["First Stage", "Area (acres)", fmt(x[0]), fmt(x[1]), fmt(x[2])])

    # loop through scenarios
    for i, s in enumerate(scenarios_data):
        y = res['y'][i]
        name = s.get("name", f"s={i + 1}")

        data.append([name, "Yield (T)", fmt(x[0] * s['yield_w']), fmt(x[1] * s['yield_c']), fmt(x[2] * s['yield_b'])])
        data.append(["", "Sales (T)", fmt(y[0]), fmt(y[2]), fmt(y[4])])
        data.append(["", "Purchase (T)", fmt(y[1]), fmt(y[3]), "-"])

    # append profit at the end
    data.append([f"Overall profit: ${-res['optimal_cost']:,.0f}", "", "", "", ""])

    df = pd.DataFrame(data, columns=["Stage/Scenario", "Metric", "Wheat", "Corn", "Sugar Beets"])

    # export
    df.to_excel(output_filename, index=False)

    return res