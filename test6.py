from hydra import compose, initialize_config_dir
from omegaconf import OmegaConf
from pathlib import Path

def main() -> None:
    config_dirr = Path().cwd().joinpath("conf")
    print(config_dirr)
    with initialize_config_dir(version_base="1.3", config_dir=config_dirr):
        cfg = compose(
            config_name="config_test2.yaml", overrides=[]
            )
        # print(cfg)
        print(OmegaConf.to_yaml(cfg))
        
if  __name__ == "__main__":
    main()