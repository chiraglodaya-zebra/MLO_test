import hydra
from omegaconf import DictConfig

@hydra.main(config_path='config.yaml')
def main(cfg: DictConfig) -> None:
  print(cfg.model.node1) # 128
  print(cfg.optimizer.lr) # 0.001
