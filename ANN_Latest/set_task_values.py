# ---------------------------------------------------------------------------- #
#                                    IMPORTS                                   #
# ---------------------------------------------------------------------------- #

import os
import sys
import time
import datetime
# ---------------------------------------------------------------------------- #
#                                    PARAMS                                    #
# ---------------------------------------------------------------------------- #


import argparse

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--task_values", type=str, required=True)

args, unknown = parser.parse_known_args()
print("Task Values", "->", args.task_values)



dbutils.jobs.taskValues.set(key   = "task_values", \
                            value = args.task_values)