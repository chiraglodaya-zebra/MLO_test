import mlflow
import hydra
from hydra import utils
from pathlib import Path
import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"


@hydra.main(config_path="conf", config_name='config_test2.yaml')
def main(cfg):
    # print(cfg)
    mlflow.set_tracking_uri('file://' + utils.get_original_cwd() + '/mlruns')
    # experiment = mlflow.get_experiment(experiment_id)
    try:
        experiment_id = mlflow.create_experiment(cfg.experiment_name)
        experiment = mlflow.get_experiment(experiment_id)
        mlflow.set_experiment(cfg.experiment_name)
        print('===============')
        print('Try block')
    except:
        mlflow.set_experiment(cfg.experiment_name)
        experiment = mlflow.get_experiment_by_name(cfg.experiment_name)
        print('===============')
        print('except block')
        # experiment = mlflow.get_experiment(experiment_id)
    with mlflow.start_run() as run:
        mlflow.set_tag("mlflow.runName",f"{cfg.experiment_name}_{run.info.run_id}")
        mode = 0o666
        output_dir = os.path.join(hydra.utils.get_original_cwd(),f"Final_Outputs\{cfg.experiment_name}\{run.info.run_id}\Whatever_output")
        print('=========================')
        print(output_dir)
        os.makedirs(output_dir, mode)
        # file_dict = cfg
        # print(file_dict)
        # with open(os.path.join(output_dir,'run_config.yaml'), 'w') as file:
        #     yaml.dump(file_dict, file)
        mlflow.log_params(cfg)
        mlflow.log_artifact(Path.cwd() / '.hydra/config.yaml')
        print('===========================')
        print(experiment)
        print('==========================')
        print(run.info.run_id) # just to show each run is different
        print("==========================")
        print(cfg.n)

        # mlflow.log_metric("changing param", cfg.n)
        mlflow.log_param("Directory", output_dir)
        mlflow.end_run()


if __name__ == '__main__':
    main()