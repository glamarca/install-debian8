#!/usr/bin/env python3
import sys

import subprocess

from functions import clone_git_repo
from sips_config import SIPS_CONFIG, DEV_PATH, AS_PATH
from utils import make_message


def clone_sips_repos(config):
    retval = 0
    failed_install = []
    if 'EPC' in config.keys() :
        EPC_PATH = ''.join([config['GLOBAL']['ucl_java_path'],'/EPC'])
        try :
            create_epc_folder = ''.join(['mkdir ',EPC_PATH])
            subprocess.check_call(create_epc_folder,shell=True)
        except Exception as e :
            retval = 1
            failed_install.append('epc folder')
            make_message('error','install','EPC Folders',e)
        if retval == 0 :
            [clone_git_repo(''.join([EPC_PATH,'/',key]),value['repo_url']) for key,value in config['EPC'].items()]
    if 'OSIS' in config.keys() :
        OSIS_PATH = ''.join([config['GLOBAL']['ucl_python_path'],'/OSIS'])
        try :
            create_osis_folder = ''.join(['mkdir ',OSIS_PATH])
            subprocess.check_call(create_osis_folder,shell=True)
        except Exception as e :
            retval = 1
            failed_install.append('osis folder')
            make_message('error','install','OSIS Folders',e)
        if retval == 0 :
            [clone_git_repo(''.join([OSIS_PATH,'/',key]),value['repo_url']) for key,value in config['OSIS'].items()]


def init_osis_postgres_db(osis_config) :
    retval = 0
    try :
        create_db_cmd = ''.join(['createdb -O ',osis_config['osis']['db_user'],' ',osis_config['osis']['db_name']])
        create_user_cmd = ''.join(['createuser ',osis_config['osis']['db_user'],' -P'])
        subprocess.check_call(create_user_cmd,shell=True)
        subprocess.check_call(create_db_cmd,shell=True)
    except Exception as e:
        make_message('error','install','postgres init',e)
        retval = 1
    return retval


['osis']
def create_sips_folders(config):
    if 'GLOBAL' in config.keys() :
        dev_path_cmd = ''.join(['mkdir ',DEV_PATH])
        ucl_dev_cmd = ''.join(['mkdir ',config['GLOBAL']['ucl_dev_path']])
        ucl_java_dev_path = ''.join(['mkdir ',config['GLOBAL']['ucl_java_path']])
        ucl_python_dev_path = ''.join(['mkdir ',config['GLOBAL']['ucl_python_path']])
        as_path_cmd=''.join(['mkdir ',AS_PATH])
        try :
            subprocess.check_call(dev_path_cmd,shell=True)
            subprocess.check_call(ucl_dev_cmd,shell=True)
            subprocess.check_call(ucl_java_dev_path,shell=True)
            subprocess.check_call(ucl_python_dev_path,shell=True)
            subprocess.check_call(as_path_cmd,shell=True)
        except Exception as e :
            make_message('error','install','SIPS Folders',e)
            exit(1)

def main(argv):
    create_sips_folders(SIPS_CONFIG)
    clone_sips_repos(SIPS_CONFIG)
    init_osis_postgres_db(SIPS_CONFIG['OSIS'])

if __name__ == "__main__":
    main(sys.argv[1:])