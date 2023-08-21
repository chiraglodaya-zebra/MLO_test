import mlflow
import hydra
from hydra import utils
from pathlib import Path
import os
from hydra.core.hydra_config import HydraConfig
os.environ["GIT_PYTHON_REFRESH"] = "quiet"


@hydra.main(config_path="conf", config_name='config')
def main(cfg):
    print(cfg)
    sweep_params = ['window_size','creation_did']
    
    mlflow.set_tracking_uri('file://' + utils.get_original_cwd() + '/mlruns')
    try:
        experiment_id = mlflow.create_experiment(cfg.experiment_name)
        mlflow.set_experiment(cfg.experiment_name)
        print('===============')
        print('Try block')
    except:
        mlflow.set_experiment(cfg.experiment_name)
        print('===============')
        print('except block')

    with mlflow.start_run() as run:
        mlflow.set_tag("mlflow.runName",f"{cfg.experiment_name}_{str(HydraConfig.get().job.num)}")
        output_dir = HydraConfig.get().runtime.output_dir
        print('=========================')
        print(output_dir)
        print(Path.cwd())
        for changing_param in sweep_params:
            mlflow.log_param(changing_param,cfg[changing_param])
        mlflow.log_param("Directory", output_dir)
        mlflow.log_artifact(Path.cwd() / '.hydra/config.yaml')
        # print('===========================')
        # print(experiment)
        print('==========================')
        print(run.info.run_id) # just to show each run is different
        print("==========================")


        # mlflow.log_metric("changing param", cfg.n)
        
        mlflow.end_run()


if __name__ == '__main__':
    main()