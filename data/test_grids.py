import numpy as np

grid_3bus = {
    "bus": [
        ["Bus1"],
        ["Bus2"],
        ["Bus3"]
    ],
    "branch": [
        ["Branch1-2", "Bus1", "Bus2", np.cdouble(0.0-1.0j)],
        ["Branch1-3", "Bus1", "Bus3", np.cdouble(0.0-1.0j)],
        ["Branch2-3", "Bus2", "Bus3", np.cdouble(0.0-0.5j)],
    ]
}

grid_5bus = {
    "bus": [
        ["Bus1"],
        ["Bus2"],
        ["Bus3"],
        ["Bus4"],
        ["Bus5"]
    ],
    "branch": [
        ["Branch1-2", "Bus1", "Bus2", np.cdouble(0.0-3.97j)],
        ["Branch1-3", "Bus1", "Bus3", np.cdouble(0.0-2.95j)],
        ["Branch1-4", "Bus1", "Bus4", np.cdouble(0.0-1.03j)],
        ["Branch1-5", "Bus1", "Bus5", np.cdouble(0.0-0.95j)],
        ["Branch2-3", "Bus2", "Bus3", np.cdouble(0.0-0.03j)],
        ["Branch3-4", "Bus3", "Bus4", np.cdouble(0.0-0.02j)],
        ["Branch4-5", "Bus4", "Bus5", np.cdouble(0.0-0.5j)],
    ]
}