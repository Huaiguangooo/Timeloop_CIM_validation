import importlib.util
import os
import shutil
import timeloopfe.v4 as tl

def load_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} not found.")

    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    return {
        "rows": config.rows,
        "cols": config.cols,
        "datawidth": config.datawidth,
        "workload": config.workload,
        "num_thread": config.num_thread,
        "storage_compute_ratio": config.storage_compute_ratio,
    }

def create_yaml_files(config):
    """
    根据配置生成 YAML 文件
    :param config: 配置字典
    """
    yaml_dir = "yaml"
    os.makedirs(yaml_dir, exist_ok=True)

    # arch.yaml
    arch_yaml = f"""architecture:
  version: 0.4
  nodes:
  - !Container
    name: System
    attributes:
      technology: "40nm"
      global_cycle_seconds: 1e-9

  - !Component
    name: GlobalBuffer
    class: SRAM
    attributes:
      depth: 4096
      width: {config['datawidth']}
      datawidth: {config['datawidth']}
    constraints:
       temporal: {{factors: M=1}}

  - !Container
    name: PE
    spatial: {{meshX: {config['rows']}, meshY: {config['cols']}}}
    constraints:
      spatial: {{factors: K={config['rows']} N={config['cols']}, permutation: [K, N]}}

  - !Component
    name: RegisterFile
    class: regfile
    attributes:
      depth: 1
      width: {config['datawidth']}
      datawidth: {config['datawidth']}
    constraints:
      dataspace: {{keep: [Weights], bypass: [Inputs, Outputs]}}

  - !Component
    name: MACC
    class: intmac
    attributes:
      width: {config['datawidth']}
"""
    with open(os.path.join(yaml_dir, "arch.yaml"), "w") as f:
        f.write(arch_yaml)

    # mapper.yaml
    mapper_yaml = f"""mapper:
  version: 0.4
  optimization_metrics: [ delay, energy ]
  live_status: False
  num_threads: {config['num_thread']}
  timeout: 1000
  victory_condition: 1000
  algorithm: random_pruned
  max_permutations_per_if_visit: 16
"""
    with open(os.path.join(yaml_dir, "mapper.yaml"), "w") as f:
        f.write(mapper_yaml)

    # prob.yaml
    prob_yaml = f"""problem:
  version: 0.4
  shape:
    name: GEMM
    dimensions: [ M, N, K ]
    data_spaces:
    - name: Inputs   # Represents matrix A
      projection:
      - [ [M], [K] ]
    - name: Weights   # Represents matrix B
      projection:
      - [ [K], [N] ]
    - name: Outputs  # Represents matrix C
      projection:
      - [ [M], [N] ]
      read_write: True

  instance:
    M: {config['workload']['Inputs'][0]}
    N: {config['workload']['Weights'][1]}
    K: {config['workload']['Inputs'][1]}
"""
    with open(os.path.join(yaml_dir, "prob.yaml"), "w") as f:
        f.write(prob_yaml)

def main():
    config_path = "config.py"  # 配置文件路径

    for folder in ["yaml", "output"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    try:
        config = load_config(config_path)
        print("Configuration loaded successfully.")
        print(f"#CIM rows: {config['rows']}")
        print(f"#CIM cols: {config['cols']}")
        print(f"datawidth: {config['datawidth']}")
        print(f"GEMM Inputs (M, K): {config['workload']['Inputs']}")
        print(f"GEMM Weights (K, N): {config['workload']['Weights']}")
        print(f"num_thread: {config['num_thread']}")
        print(f"storage_compute_ratio: {config['storage_compute_ratio']}")
        
        create_yaml_files(config)
        print("Successfully created yaml files.")
    except Exception as e:
        print(f"Failed to create yaml files: {e}")

    out_dir = "output"

    THIS_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

    start_dir = os.path.join(THIS_SCRIPT_DIR, ".")
    spec = tl.Specification.from_yaml_files(
        os.path.join(start_dir, "yaml/*.yaml"),
    )
    tl.call_mapper(spec, output_dir=os.path.join(start_dir, f"{out_dir}"))

if __name__ == "__main__":
    main()