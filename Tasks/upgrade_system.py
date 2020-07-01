#!/usr/bin/env python3
import sys
sys.path.append("..")
from Utilities import get_exec_permission, Logger

logger = Logger()


def main():
    task_name = __file__.split(".")[0]
    logger.log("Starting task " + task_name)
    permission = get_exec_permission(task_name)
    if not permission:
        logger.log("Task " + task_name + " is disabled.")
        logger.log("Exiting")


if __name__ == "__main__":
    main()