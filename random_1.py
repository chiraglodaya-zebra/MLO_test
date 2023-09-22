import mlflow
import hydra
from hydra import utils
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, OmegaConf
import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
from pathlib import Path
import json
# config_path = Path().cwd().joinpath("conf")

@hydra.main(version_base= None, config_path="conf", config_name="config_test3")
def main(cfg : DictConfig) -> None:
    json_list = cfg.torun_jsons
    print(type(json_list))
    for i in json_list:
        print(i)

if __name__ == '__main__':
    main()