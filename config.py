# =============================================================================
#          File: config.py
#        Author: Andre Brener
#       Created: 27 May 2017
#   Description: Load logging configuration from config.yaml and expose the
#                project directory.
# =============================================================================
import os

import yaml

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(PROJECT_DIR, 'config.yaml'), 'r') as config_file:
    config = yaml.safe_load(config_file.read())
