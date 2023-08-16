import mlflow
import hydra
from hydra import utils
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

@hydra.main(version_base= None, config_path="conf", config_name="config_test2.yaml",)
def main(cfg : DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == '__main__':
    main()