# ---------------------------------------------------------------------------- #
#                                    IMPORTS                                   #
# ---------------------------------------------------------------------------- #

import os
import sys
import time
import json


# ---------------------------------------------------------------------------- #
#                                    PARAMS                                    #
# ---------------------------------------------------------------------------- #

import argparse

parser = argparse.ArgumentParser(add_help=False)

args, unknown = parser.parse_known_args()


task_values = dbutils.jobs.taskValues.get(
                            taskKey = "T0",
                            key   = "task_values")


# task_values = task_values[1:len(task_values)-1]
print(task_values)
task_values = task_values.replace("'",'"')
print(task_values)
task_values_json = json.loads(task_values)
print(task_values_json)

all_tags = {}

for tag in json.loads(spark.conf.get("spark.databricks.clusterUsageTags.clusterAllTags")):

  all_tags[tag['key']] = tag['value']

task_name = all_tags.get('task')

 

# Print the task name

print(json.loads(spark.conf.get("spark.databricks.clusterUsageTags.clusterAllTags")))
