import os
# from tkinter.tix import Tree
from typing import Sequence
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
import time
import ai_core.tools
import ai_core.api
import json
import sys
import datetime as dt



 
# ai_core.api.register_local_library("antuit", "/root/antuit-esp-adf-dev")

 
ARGO = False

if "FORMAT_PARAMS" in os.environ.keys():
    print('\n Running in Argo ... \n')
    ARGO = True
    run_params = eval(os.environ['FORMAT_PARAMS'])
    forecast_creation_date = int(run_params['forecast_creation_date'])
    is_gpu = True if run_params['forecast_creation_date'] == 'true' else False

    # Cluster Config
    if 'executor_instances' in run_params:
        executor_instances = int(run_params['executor_instances'])
    if 'executor_cores' in run_params:
        executor_cores = int(run_params['executor_cores'])
    if 'executor_profile' in run_params:
        executor_profile = run_params['executor_profile']

else:
    print('\n Running maually ... \n')
    # Cluster Config
    # executor_instances = 4
    # executor_cores = 16
    # forecast_creation_date = 180
    is_gpu = False
    if is_gpu:
        executor_profile = "GPU1C6M96_NC6s_v3"
    else:
        executor_profile = "C8M54_E8ds_v5" #"C4M3_F4s_v2"# "C2M1_F2s_v2#"C15M25_F16s_v2"#"C8M54_E8ds_v5"#"C15M25_F16s_v2"


#######################
creation_did = 48
batch_size = 128
run_dt = dt.datetime.strftime(dt.datetime.today(), '%Y%m%d')

print(creation_did)

# base_path = "wasbs://qa1datamartstdsandbox@qa1datamartstdsandbox-ds-store-std-sandbox-rw.blob.core.windows.net"
base_path = "dbfs:/mnt/qa1datamartstdsandbox/qa1datamartstdsandbox-ds-store-std-sandbox-rw"
s_dir =  "/var/content/qa1datamartstdsandbox-ds-store-std-sandbox-rw"


# change the input path before executing


input_df_path = f'{base_path}/ML_Ops_Exp/Input/ANN_Input.parquet'


fe_model_output = f'{base_path}/ML_Ops_Exp/Output/fe/fe_model_output.parquet'

model_data_path = f'{base_path}/ML_Ops_Exp/Output/fe/'

dataset_path =f"{base_path}/ML_Ops_Exp/Output/fe/"
model_path = f"{base_path}//ML_Ops_Exp/Output/model/"
tensor_board_log_dir =f"{base_path}/ML_Ops_Exp/Output/model/tensorboard_logs/"

predict_model_path =f'{base_path}/ML_Ops_Exp/Output/model/'
predict_input_path = f'{base_path}/ML_Ops_Exp/Output/fe/prediction.parquet'
forecast_path = f'{base_path}/ML_Ops_Exp/Output/predict/forecast_out.parquet'




format_params = {
    "input_df_path":input_df_path,
    "fe_model_output":fe_model_output,
    "model_data_path":model_data_path,
    
    "model_path":model_path,
    "dataset_path": dataset_path,
    "tensor_board_log_dir":tensor_board_log_dir,

    "predict_model_path":predict_model_path,
    "predict_input_path":predict_input_path,
    "forecast_path":forecast_path,
    "creation_did" : creation_did,
    "batch_size": batch_size
        }

#############################################################################################


json_path = '/Workspace/Repos/chirag.lodaya@zebra.com/MLO_test/ANN_Testing'

t0 = time.time() 
json_list = ['fe','model','predict']

for looping_json in json_list:
    json_name = f"{json_path}/{looping_json}.json"

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
        print('Loading API Stages')    
        ai_core.api.run(platform=platform, spark=spark, stages_list=stages['DFP']['stages'])

    elapsed_time = time.time() - t0
    print(f"----- Total time for {job_json}----")
    print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))