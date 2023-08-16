# import mlflow
# import hydra
import os
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

file__fullPath = "dbfs:/mnt/devdatamartstd/devdatamartstd-ds-store-rw/Amazon_EU_Test/12NC_lvl/ANN/JSON" #os.path.abspath(__file__)
file__baseName = "dbfs:/mnt/devdatamartstd/devdatamartstd-ds-store-rw/Amazon_EU_Test/12NC_lvl/ANN/JSON" #os.path.basename(file__fullPath)
file__parentDr = os.path.dirname(file__fullPath)
 
# ai_core.api.register_local_library("storeSplit", "/Workspace/Users/ritesh.gunjal@zebra.com/ANN/")

#######################
exp_id = "Exp_20230725_10"
input_path_date = "20230725"
re_run_flag = 1
creation_did = 60
segments = '5678' # 5678 234

run_dt = dt.datetime.strftime(dt.datetime.today(), '%Y%m%d')
exp_col = str(exp_id)
file_name = "predict"



print(exp_id)
print(creation_did)

base_job_json = f"/dbfs/mnt/devdatamartstd/devdatamartstd-ds-store-rw/Amazon_EU_Test/12NC_lvl/ANN/JSON/{segments}/"
base_path = "dbfs:/mnt/devdatamartstd/devdatamartstd-ds-store-rw"
s_dir = base_path # "/var/content/ds-store"

# change the input path before executing

if re_run_flag == 0:
    input_df_path = f'{base_path}/Amazon_EU_Test/12NC_lvl/ANN/model_input/{input_path_date}/ANN_Input_{segments}_{creation_did}.parquet'
else:
    input_df_path = f'{base_path}/Amazon_EU_Test/12NC_lvl/ANN/DB_Output/{exp_id}/model_input_Future_Frcs/ANN_Input_{segments}_{creation_did}.parquet'

print(input_df_path)
# change this path if requried
folder_path = f'Amazon_EU_Test/12NC_lvl/ANN/DB_Output/{exp_id}/{creation_did}/{segments}'
folder_path_2 = f'Amazon_EU_Test/12NC_lvl/ANN/DB_Output/{exp_id}/{creation_did}/{segments}'
fe_folder_path = f'Amazon_EU_Test/12NC_lvl/ANN/DB_Output/Whole_Data_FE/{creation_did}/fe'

fe_model_output = f'{base_path}/{folder_path}/fe/fe_model_output.parquet'

model_data_path = f'{base_path}/{folder_path}/fe/'
dataset_path =f"{s_dir}/{folder_path}/fe/"

model_path = f"{s_dir}/{folder_path_2}/model/"
tensor_board_log_dir =f"{s_dir}/{folder_path_2}/model/tensorboard_logs/"

predict_model_path =f'{base_path}/{folder_path_2}/model/'
predict_input_path = f'{base_path}/{folder_path}/fe/prediction.parquet'
forecast_path = f'{base_path}/{folder_path_2}/predict/forecast_out.parquet'


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
    "creation_did" : creation_did
        }

#############################################################################################
t0 = time.time()
# 'fe', 'model','predict'
for pipeline_name in ['fe']:
  json_name = f"{pipeline_name}.json"

  if True:
      # print format_params
      if isinstance(format_params, dict):
          print(json.dumps(format_params, sort_keys=False, indent=4))
      else:
          print(format_params)
      

      # Load stages
      key = json_name
      job_json = base_job_json + key
      # print(base_job_json, key)
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