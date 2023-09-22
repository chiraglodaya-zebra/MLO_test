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
config_name = 'config_T2'
torun_jsons = ['T2_1','T2_2']
prev_dir = 'Output/fe'

 



@hydra.main(version_base=None, config_path=f"conf/{run_type}", config_name=config_name)
def my_app(cfg : DictConfig) -> None:
    ############# DFP specific block

    # torun_jsons = cfg.torun_jsons

    total_runtime_oppath = HydraConfig.get().runtime.output_dir
    total_runtime_oppath = total_runtime_oppath.replace("/dbfs","dbfs:")

    

    if run_type == 'Exp':
        task_name = cfg.custom.task_name
        mlflow_run_name = f'{task_name}_'+str(HydraConfig.get().job.num)

        op_dir_model = f"Output/model"
        op_dir_predict = f"Output/predict"

        par_runtime_oppath = HydraConfig.get().sweep.dir
        par_runtime_oppath = par_runtime_oppath.replace("/dbfs","dbfs:")

        prev_sweep = cfg.prev_sweep 
        prev_sweep = prev_sweep.replace("_","=")

        if prev_sweep == 'Def':
            prior_op = f'{cfg.prev_task}/{prev_dir}'
        else:
            prior_op = f'{prev_sweep}/{prev_dir}'



    else:
        task_name = cfg.custom.task_name2
        mlflow_run_name = f'{task_name}'
        # op_dir = f"{task_name}/Output/fe"

        op_dir_model = f"{task_name}/Output/model"
        op_dir_predict = f"{task_name}/Output/predict"

        par_runtime_oppath = total_runtime_oppath
        prior_op = f'{cfg.custom.task_name1}/{prev_dir}'


    
    batch_size = cfg.batch_size
    learning_rate = cfg.learning_rate
    creation_did = cfg.creation_did

    today = date.today().strftime("%Y-%m-%d")
    exp_logging = f"{run_type}_{today}_{cfg.custom.exp_title}"



    print(batch_size)
    print(learning_rate)
    print(prior_op)


    mlflow_dir = f"/Users/chirag.lodaya@zebra.com/{exp_logging}"
    base_path = "dbfs:/mnt/qa1datamartstdsandbox/qa1datamartstdsandbox-ds-store-std-sandbox-rw"
    git_root = '/Workspace/Repos/chirag.lodaya@zebra.com/MLO_test'
    

    
    
    
    

    # fe_model_output = f'{runtime_oppath}/{op_dir}/fe/fe_model_output.parquet'
    # model_data_path = f'{runtime_oppath}/{op_dir}/fe/'

    dataset_path = f'{par_runtime_oppath}/{prior_op}/'
    predict_input_path = f'{par_runtime_oppath}/{prior_op}/prediction.parquet'


    # input_df_path = f'{base_path}/ML_Ops_Exp/Input/ANN_Input.parquet'
    


    # # model stuff
    model_path = f'{total_runtime_oppath}/{op_dir_model}/'
    tensor_board_log_dir =f'{total_runtime_oppath}/{op_dir_model}/tensorboard_logs/'
    predict_model_path =f'{total_runtime_oppath}/{op_dir_model}/'
    forecast_path = f'{total_runtime_oppath}/{op_dir_predict}/forecast_out.parquet'

    


    

    format_params = {
        # "input_df_path":input_df_path,
        # "fe_model_output": fe_model_output,
        # "model_data_path": model_data_path,
        # "predict_input_path": predict_input_path,
        # "operand1":operand1, 
        # "operand2" : operand2,
        # "creation_did": creation_did,
        "creation_did": creation_did,
        "learning_rate": learning_rate,
        "batch_size": batch_size,
        "dataset_path": dataset_path,
        "predict_input_path": predict_input_path,
        "model_path": model_path,
        "tensor_board_log_dir": tensor_board_log_dir,
        "predict_model_path": predict_model_path,
        "forecast_path": forecast_path,
        "total_runtime_oppath": total_runtime_oppath,
        "par_runtime_oppath": par_runtime_oppath,
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

    with mlflow.start_run(run_name=mlflow_run_name):
        mlflow.log_params(cfg)
        mlflow.log_param(f"Task_{task_name}_Model_Path",model_path)
        mlflow.log_param(f"Task_{task_name}_Output_Path",forecast_path)
        mlflow.end_run()
    

    for temp_json in torun_jsons:
        t0 = time.time()
        json_name = f"{git_root}/ANN_V1_Improved/{temp_json}.json"

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