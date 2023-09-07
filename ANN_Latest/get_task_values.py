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
                            taskKey = "T1",
                            key   = "task_values")

print(task_values)
task_values_json = json.loads(task_values)

print(task_values_json)
