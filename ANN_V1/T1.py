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
from datetime import date


run_type = 'Exp'
task_name= 'T1'
config_name = 'config_T1'
torun_jsons = ['T1']
 

@hydra.main(version_base=None, config_path=f"conf/{run_type}", config_name=config_name)
def my_app(cfg : DictConfig) -> None:
    ############# DFP specific block
    operand1 = cfg.operand1
    operand2 = cfg.operand2
    creation_did = cfg.creation_did
    today = date.today().strftime("%Y-%m-%d")
    exp_logging = f"{today}_{cfg.custom.exp_title}"

    print(operand1)
    print(operand2)


    mlflow_dir = f"/Users/chirag.lodaya@zebra.com/{exp_logging}"
    base_path = "dbfs:/mnt/qa1datamartstdsandbox/qa1datamartstdsandbox-ds-store-std-sandbox-rw"
    git_root = '/Workspace/Repos/chirag.lodaya@zebra.com/MLO_test'
    
    runtime_oppath = HydraConfig.get().runtime.output_dir
    runtime_oppath = runtime_oppath.replace("/dbfs","dbfs:")
    op_dir = f"{task_name}/Output"
    

    fe_model_output = f'{runtime_oppath}/{op_dir}/fe/fe_model_output.parquet'
    model_data_path = f'{runtime_oppath}/{op_dir}/fe/'
    # dataset_path = f'{runtime_oppath}/fe/'
    # predict_input_path = f'{runtime_oppath}/fe/prediction.parquet'


    input_df_path = f'{base_path}/ML_Ops_Exp/Input/ANN_Input.parquet'
    


    # # model stuff
    # model_path = f'{runtime_oppath}/model/'
    # tensor_board_log_dir =f'{runtime_oppath}/model/tensorboard_logs/'
    # predict_model_path =f'{runtime_oppath}/model/'
    # forecast_path = f'{runtime_oppath}/predict/forecast_out.parquet'

    


    

    format_params = {
        "input_df_path":input_df_path,
        "fe_model_output": fe_model_output,
        "model_data_path": model_data_path,
        # "dataset_path": dataset_path,
        # "predict_input_path": predict_input_path,
        "operand1":operand1, 
        "operand2" : operand2,
        "creation_did": creation_did,
        "runtime_oppath": runtime_oppath,
        "mlflow_dir ": mlflow_dir ,
        "git_root": git_root,
        "base_path": base_path
            }

    #############################################################################################
    try:
        experiment_id = mlflow.create_experiment(mlflow_dir)
        mlflow.set_experiment(mlflow_dir)
        print('===============')
        print('Try block')
    except:
        mlflow.set_experiment(mlflow_dir)
        print('===============')
        print('except block')

    if run_type == 'Exp':
        with mlflow.start_run(run_name=str(HydraConfig.get().job.num)):
            mlflow.log_params(cfg)
            mlflow.log_param(f"Task_{task_name}_Output_Path",model_data_path)
            mlflow.end_run()
    else:
        with mlflow.start_run(run_name=str(0)):
            mlflow.log_params(cfg)
            mlflow.log_param(f"Task_{task_name}_Output_Path",model_data_path)
            mlflow.end_run()

    for temp_json in torun_jsons:
        t0 = time.time()
        json_name = f"{git_root}/ANN_V1/{temp_json}.json"

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