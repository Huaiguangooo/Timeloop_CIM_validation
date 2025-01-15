rows = 8                 # CIM structure rows
cols = 4                 # CIM structure columns
datawidth = 16            # Data bit width
workload = {             # Matrix multiplication dimensions
    "Inputs": [32, 8],     # [M, K]
    "Weights": [8, 4]      # [K, N]
}
# Note: Only support K = CIM rows and N = CIM cols for now.
num_thread = 8           # Number of mapper threads
storage_compute_ratio = 1