# ---------------------------------------------------------------------------- #
#                                    IMPORTS                                   #
# ---------------------------------------------------------------------------- #

import os
import sys
import time


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
