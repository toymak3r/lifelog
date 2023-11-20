#  LifeLog
#  https://github.com/toymak3r/lifelog

"""Configure module for Lifelog

This module loads configure file from json file.
"""

__version__ = '0.1'
__author__ = 'Edward Facundo'

import json
import logging
import os
from pathlib import Path


class Config:
    # user directory to hold the files
    user_dir = os.path.join(Path.home(), '.lifelog')
    template_config_file = 'templates/config.template.json'  # template of configuration
    # content of configuration
    config = ''
    # default configuration file
    config_file = 'config.json'
    # complete path for config file
    config_file_path = os.path.join(user_dir, config_file)
    config_file_handle = ''                                  # config file handle

    def __init__(self, user_dir=None):

        if (user_dir is not None):
            self.user_dir = user_dir

        if not os.path.exists(self.user_dir):
            logging.warning(
                'Loglife user directory do not exit, creating: %s!' % self.user_dir)
            os.makedirs(self.user_dir)

        if os.path.exists(self.config_file_path):
            self.open_file('r')
            self.load_file()
            self.close_file()
        else:
            self.open_file('w')
            template_content = open(self.template_config_file, 'r')
            self.config = json.loads(template_content.read())
            template_content.close()
            self.save_file()
            self.config_file_handle.close()

    def open_file(self, mode):
        self.config_file_handle = open(os.path.join(
            self.user_dir, self.config_file), mode)

    def close_file(self):
        self.config_file_handle.close()

    def load_file(self):
        try:
            self.config = json.loads(self.config_file_handle.read())
        except:
            logging.error(f'config file problematic, please check it: {self.config_file_path}')
            exit(-1)

    def save_file(self):
        self.config_file_handle.write(json.dumps(self.config))
