import hydra
import os
from omegaconf import DictConfig, OmegaConf
from hydra.core.hydra_config import HydraConfig
# from tkinter.tix import Tree
from typing import Sequence
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
import time
import ai_core
import ai_core.tools
import ai_core.api
import json
import sys
import datetime as dt
import mlflow

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg : DictConfig) -> None:
    ############# DFP specific block
    creation_did = cfg.creation_did
    batch_size = cfg.batch_size
    init_dir = "/Users/chirag.lodaya@zebra.com/experiment_ann_1"
    # init_dir = init_dir.replace("/dbfs","dbfs:")
    runtime_par_path = HydraConfig.get().sweep.dir
    runtime_par_path = runtime_par_path.replace("/dbfs","dbfs:")
    runtime_oppath = HydraConfig.get().runtime.output_dir
    runtime_oppath = runtime_oppath.replace("/dbfs","dbfs:")
    print(creation_did)
    print(batch_size)

    base_path = "dbfs:/mnt/qa1datamartstdsandbox/qa1datamartstdsandbox-ds-store-std-sandbox-rw"


    # change the input path before executing

    input_df_path = f'{base_path}/ML_Ops_Exp/Input/ANN_Input.parquet'


    fe_model_output = f'{runtime_par_path}/fe/fe_model_output.parquet'

    model_data_path = f'{runtime_par_path}/fe/'

    dataset_path = f'{runtime_par_path}/fe/'

    model_path = f'{runtime_oppath}/model/'
    tensor_board_log_dir =f'{runtime_oppath}/model/tensorboard_logs/'

    predict_model_path =f'{runtime_oppath}/model/'
    predict_input_path = f'{runtime_par_path}/fe/prediction.parquet'
    forecast_path = f'{runtime_oppath}/predict/forecast_out.parquet'

    


    git_root = '/Workspace/Repos/chirag.lodaya@zebra.com/MLO_test'
    print(input_df_path)

    format_params = {
        "input_df_path":input_df_path,
        "fe_model_output": fe_model_output,
        "model_data_path": model_data_path,
        "dataset_path": dataset_path,
        "model_path": model_path,
        "tensor_board_log_dir": tensor_board_log_dir,
        "predict_model_path": predict_model_path,
        "predict_input_path": predict_input_path,
        "forecast_path": forecast_path,
        "batch_size":batch_size, 
        "creation_did" : creation_did,
        "runtime_oppath": runtime_oppath,
        "runtime_par_path": runtime_par_path,
        "init_dir": init_dir,
        "git_root": git_root,
        "base_path": base_path
            }

    #############################################################################################
    try:
        experiment_id = mlflow.create_experiment(init_dir)
        mlflow.set_experiment(init_dir)
        print('===============')
        print('Try block')
    except:
        mlflow.set_experiment(init_dir)
        print('===============')
        print('except block')

    with mlflow.start_run(run_name=str(HydraConfig.get().job.num)):
        mlflow.log_params(cfg)
        mlflow.log_param("Output_Parquet_Path",forecast_path)
        mlflow.end_run()


    
    torun_jsons = ['fe']
    for temp_json in torun_jsons:
        t0 = time.time()
        json_name = f"{git_root}/ANN_Testing/{temp_json}.json"

        if True:
            # print format_params
            if isinstance(format_params, dict):
                print(json.dumps(format_params, sort_keys=False, indent=4))
            else:
                print(format_params)
            

            # Load stages
            job_json = json_name
            print(job_json)
            print(f"Running job_json: {job_json}")
            stages = ai_core.tools.load_stages(f"{job_json}", format_params, sequence='DFP')


        # Create Spark session

            spark = SparkSession.builder.getOrCreate()
            sparkConf = SparkConf()
            print("Spark session created")
            platform = ai_core.platforms.DatabricksPlatform()

            # Run pipeline
                
            ai_core.api.run(platform=platform, spark=spark, stages_list=stages['DFP']['stages'])

        elapsed_time = time.time() - t0
        print(f"----- Total time to run {json_name}----")
        print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    
if __name__ == "__main__":
    my_app()