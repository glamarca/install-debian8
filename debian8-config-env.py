#!/usr/bin/env python3
import fileinput
import os, sys, subprocess, configparser

# Script d'installation d'un environnement de développement
#
# OS : Debian 8
# Languages de développement : Python3, Java7 et 8, Clojure
# DB : Postgres,Couchbase
# Outils : Atom, Netbeans, Pycharm, IntelliJ, Android-studio, SqlDevelopper, Visual Paradigm
#

# Fichier contenant les applications et dépendances à installer
import pwd

from config import APPS, USER
from functions import sudo_install, java_install, base_install, python_install, postgresql_install, install_dev_tools, \
    install_media, install_mozilla, add_debian_repo, install_drivers, install_couchbase, add_packages_keys, \
    configure_git
from references import TOOLS_FOLDER


def base_tests(config, user_config):
    # Test si l'utilisateur à les droits admin
    if os.geteuid() != 0:
        print('')
        print('!!!! Utilisateur doit avoir les droits administrateur !!!!')
        print('!!!! Lancez le script en root !!!!')
        exit(1)

    ## Validation du fichier de propriétés
    # Test les données obligatoiure du fichier user.properties
    if not user_config['BASE']['os_user']:
        print('')
        print('!!!! Le paramètre os_user doit être défini dans le fichier user.properties !!!!')
        exit(1)
    # Test si l'utilisateur spécifié dans le fichier user.properties existe bien sur l'OS
    try:
        pwd.getpwnam(user_config['BASE']['os_user'])
    except:
        print('')
        print(''.join(['!!!! L\'utilisateur ', user_config['BASE']['os_user'], ' n\'existe pas sur le système !!!!']))
        exit(1)
    # Test si sqldeveloper doit être installé et si l'archive est présente dans le dossier tools
    if 'DEV-TOOLS' in config.keys() and 'sql-developer' in config['DEV-TOOLS'] and not os.path.isfile(
            os.path.join(TOOLS_FOLDER, config['DEV-TOOLS']['sql-developer'])):
        print('')
        print('!!!! Vous avez spécifié l\'installation de sqldeveloper sans founir l\'archive nécéssaire !!!!')
        exit(0)
    # Le script ne fonctionne que si python3 est présent sur le système
    try:
        subprocess.check_output('which python3', shell=True, universal_newlines=True)
    except:
        print('')
        print('!!!! Python3 doit être présent sur le système et accèssible dans le $PATH !!!!')
        exit(1)
    # Vérifie données git si activé
    if 'GIT' in user_config.keys() and (
                'name' not in user_config['GIT'].keys() or 'username' not in user_config['GIT'].keys() or 'email' not in
        user_config['GIT'].keys()):
        print('')
        print('!!!! Les informations git doivent être fournie si vous activez la config git !!!!')
        exit(1)


def main(argv):
    failed_install = None

    ### Initialisation de la lecture des fichier de propriétés
    config = APPS
    user_config = USER

    # Test validité propriété et utilisateur
    base_tests(config=config, user_config=user_config)
    # Installation sudo et ajout utilisateur au groupe sudo
    sudo_install(os_user=user_config['BASE']['os_user'])

    print('*** Liste des section d\'installation ***')
    print(config.keys())
    print('')

    # ajout Dépôt
    if 'DEBIAN_REPO' in config.keys():
        add_debian_repo(config['DEBIAN_REPO'])

        # AJout clefs publiques dépôts
    if 'PACKAGE_KEY' in config.keys():
        add_packages_keys(config['PACKAGE_KEY'])

    ### Installation Java
    ## Les jdk spécifié dans le fichier app.properies vont être téléchargés et installés dans /opt
    if 'JAVA' in config.keys():
        java_install(config['JAVA'])

    ### Installation des dépendances de base
    if 'BASE' in config.keys():
        base_install(config['BASE'])

    ### Installation Python
    ## Python3 ainsi que les dépendances nécéssaires
    if 'PYTHON' in config.keys():
        python_install(config['PYTHON'])

    ### Installation PostgreSQL
    ## postgres9 et dépendences dev nécéssaires
    if 'POSTGRES' in config.keys():
        postgresql_install(config['POSTGRES'])

    ### Installation des outils de développement

    if 'DEV-TOOLS' in config.keys():
        failed_install = install_dev_tools(config['DEV-TOOLS'], user_config['BASE']['os_user'])

    if 'MEDIA' in config.keys():
        retval = install_media(config['MEDIA'])
        if retval:
            failed_install.append('media')

    if 'MOZILLA' in config.keys():
        retval = install_mozilla(config['MOZILLA'])
        if retval:
            failed_install.append('mozzilla')

    if 'COUCHBASE' in config.keys():
        retval = install_couchbase(config['COUCHBASE'])
        if retval:
            failed_install.append('couchbase')

    if 'DRIVERS' in config.keys():
        retval = install_drivers(config['DRIVERS'])
        failed_install += retval

    if 'GIT' in user_config.keys():
        retval = configure_git(user_config['GIT'], user_config['BASE']['os_user'])
        if retval:
            failed_install.append('GIT-CONFIG')

    if failed_install:
        print('**** Installation terminée avec des échecs ****')
        [print(''.join(['*', fail_app])) for fail_app in failed_install]
    else:
        print('**** Installation terminée avec succès ****')

    exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
