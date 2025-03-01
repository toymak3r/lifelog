import json
import logging
import os
from pathlib import Path
from typing import Dict, Optional
from .module import LifeLogModule

#  LifeLog
#  https://github.com/toymak3r/lifelog

"""Configure module for Lifelog

This module loads configure file from json file.
"""

__version__ = json.load(open('__version__.json'))['version']
__author__ = 'Edward Facundo'


class Config:
    # user directory to hold the files
    user_dir = os.path.join(Path.home(), '.loglife')
    template_config_file = 'templates/config.template.json'  # template of configuration
    # default configuration file
    config_file = 'config.json'
    # complete path for config file
    config_file_path = os.path.join(user_dir, config_file)

    def __init__(self, user_dir: Optional[str] = None):
        self.modules: Dict[str, LifeLogModule] = {}
        
        if user_dir:
            self.user_dir = user_dir

        self._ensure_user_directory()
        self._load_configuration()

    def _ensure_user_directory(self):
        if not os.path.exists(self.user_dir):
            logging.warning(
                'Lifelog user directory does not exist, creating: %s!', self.user_dir)
            os.makedirs(self.user_dir)

    def _load_configuration(self):
        if os.path.exists(self.config_file_path):
            self.load_file()
        else:
            self.create_default_config()

    def load_file(self):
        try:
            with open(self.config_file_path, 'r') as file:
                self.config = json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            logging.error('Error loading config file: %s', e)
            exit(-1)

    def create_default_config(self):
        try:
            with open(self.template_config_file, 'r') as template_file:
                self.config = json.load(template_file)
            self.save_file()
        except (json.JSONDecodeError, IOError) as e:
            logging.error('Error creating default config file: %s', e)
            exit(-1)

    def save_file(self):
        try:
            with open(self.config_file_path, 'w') as file:
                json.dump(self.config, file, indent=4)
        except IOError as e:
            logging.error('Error saving config file: %s', e)
            exit(-1)