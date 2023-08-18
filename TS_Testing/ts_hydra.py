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

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg : DictConfig) -> None:
    print(HydraConfig.get().runtime.output_dir)
    # hydra.job.override_dirname('Latest')

    ############# DFP specific block
    creation_did = cfg.creation_did
    window_size = int(cfg.window_size)
    runtime_oppath = HydraConfig.get().runtime.output_dir
    print(creation_did)
    print(window_size)

    base_path = "dbfs:/FileStore/MLO_Test_Temp"


    # change the input path before executing

    input_df_path = f'{base_path}/Input_data/Model_Table_ForecastCreation_July23.parquet'
    forecast_out_time_series = f'{runtime_oppath}/Output_data/TS_Output.parquet'
    ts_model_path = f'{runtime_oppath}/Output_data/model'

    git_root = '/Workspace/Repos/chirag.lodaya@zebra.com/MLO_test'
    print(input_df_path)
    print(forecast_out_time_series)

    format_params = {
        "input_df_path":input_df_path,
        "forecast_out_time_series": forecast_out_time_series, 
        "ts_model_path": ts_model_path,
        "creation_did" : creation_did,
        "window_size": window_size,
        "runtime_oppath": runtime_oppath,
        "git_root": git_root,
        "base_path": base_path
            }

    #############################################################################################
    t0 = time.time()
    json_name = f"{git_root}/TS_Testing/ts.json"

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
    print("----- Total time ----")
    print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    
if __name__ == "__main__":
    my_app()