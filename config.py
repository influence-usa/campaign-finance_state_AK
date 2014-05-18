import os

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
DOWNLOAD_DIR = CURRENT_DIRECTORY + '/downloads'
TEXT_CONV_DIR = DOWNLOAD_DIR + '/text_conv'
DATA_DIR = CURRENT_DIRECTORY + '/data'
USE_ALTERNATE = False

import config_local
#
# FEEL FREE TO IMPORT A CONFIG.LOCAL IF YOU HAVE ONE AND
# OVERWRITE THE ABOVE DIRECTORIES
#
