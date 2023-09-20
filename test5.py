import mlflow
import hydra
from hydra import utils
from hydra.core.hydra_config import HydraConfig
import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
from pathlib import Path


# import hydra
# c = []
# hydra.main(config_name="config.yaml")(lambda x:c.append(x))()
# cfg = c[0]
# print(cfg)

# @hydra.main(version_base=None, config_path="conf", config_name='config_test.yaml')
# def main(cfg):
#     print('==================')
#     print(cfg)
#     print('==================')
#     # mlflow.set_tracking_uri('file://' + utils.get_original_cwd() + '/mlruns')


# if __name__ == '__main__':
#     main()

import hydra
from omegaconf import DictConfig, OmegaConf

# config_path = Path().cwd().joinpath("conf")

@hydra.main(version_base= None, config_path="conf", config_name="config_test2")
def main(cfg : DictConfig) -> None:
    print(cfg)
    # runtime_oppath = HydraConfig.get().runtime.output_dir
    # print(runtime_oppath)


if __name__ == '__main__':
    main()