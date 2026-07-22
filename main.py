from farmer import farmer


if __name__ == "__main__":

    farmer(
        c=[150.0, 230.0, 260.0],
        A_ub=[[1.0, 1.0, 1.0]],
        b_ub=[500.0],
        q_base=[-170.0, 238.0, -150.0, 210.0, -36.0, -10.0, 0.0],
        W_base=[
            [-1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, -1.0, -1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, -1.0, 0.0, -1.0]
        ],
        h_base=[200.0, 240.0, 0.0, -6000.0],
        scenarios_data=[
            {"name": "Scenario 1 (Above Avg)", "yield_w": 3.0, "yield_c": 3.6, "yield_b": 24.0},
            {"name": "Scenario 2 (Average)", "yield_w": 2.5, "yield_c": 3.0, "yield_b": 20.0},
            {"name": "Scenario 3 (Below Avg)", "yield_w": 2.0, "yield_c": 2.4, "yield_b": 16.0},
        ],
        p=1.0 / 3.0
    )
