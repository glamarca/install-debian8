import os
import re
import subprocess

from references import install_cmd, add_user_to_grp, PHASES, oracle_jdk_wget_cmd, add_repo_cmd, wget_app_cmd, chown_cmd, \
    execute_as_user, \
    clear_list_repo_file, add_package_key, install_testing_cmd, install_backports_cmd, dpkg_install, TOOLS_FOLDER, \
    add_pinning_cmd, desktop_entry
from utils import make_message


def sudo_install(os_user):
    ### Installation de sudo
    print('**** Installation de sudo ****')
    try:
        subprocess.check_call('apt-get install sudo', shell=True)
        print('')
        ## Ajout de l'utilisateur dans sudo
        print('** Ajout de l\'utilisateur dans groupe sudo')
        subprocess.check_call(add_user_to_grp.format('sudo', os_user), shell=True)
    except Exception as e:
        make_message('error', 'sudo', 'install', e)
        exit(1)


def java_install(java_apps):
    make_message('section_title', 'JAVA')
    make_message('app_lists', java_apps.keys())
    os.chdir('/opt')
    # Téléchargement de la version de java7 spécifiée dans le fichier de propriétés
    java7_link = java_apps['java7']
    match = re.search('.+\/(.+\.gz$)', java7_link)
    java7_version = match.group(1)
    if not java7_version:
        print('!! Erreur dans le chemin de téléchargement de jdk7\n')
        print('')
        exit(1)
    try:
        make_message('phase_title', PHASES['download']['title'], java7_version)
        java7_wget_cmd = ''.join([oracle_jdk_wget_cmd, java7_link])
        subprocess.check_call(java7_wget_cmd, shell=True)
        # Decompression dans /opt
        make_message('phase_title', PHASES['install']['title'], 'jdk7 dans /opt/jdk7')
        subprocess.check_call('sudo mkdir jdk7', shell=True)
        tar_cmd = ''.join(['sudo tar -xzf ', java7_version, ' -C jdk7 --strip-components 1'])
        subprocess.check_call(tar_cmd, shell=True)
        subprocess.check_call('sudo chown -Rf root:root jdk7', shell=True)
        rm_jdk7_gz_cmd = ''.join(['sudo rm -f ', java7_version])
        subprocess.check_call(rm_jdk7_gz_cmd, shell=True)
        # Ajout de java7 oracle dans alternatives java
        print('** Ajout de java7 dans alternatives\n')
        subprocess.check_call('sudo update-alternatives --install /usr/bin/java java /opt/jdk7/bin/java 1', shell=True)
        subprocess.check_call('sudo update-alternatives --install /usr/bin/javac javac /opt/jdk7/bin/javac 1',
                              shell=True)
        subprocess.check_call('sudo update-alternatives --install /usr/bin/javaws javaws /opt/jdk7/bin/javaws 1',
                              shell=True)
    except Exception as e:
        make_message('error', PHASES['install']['fct'], 'jdk7', e)
        exit(1)

    # Téléchargement de la version de java8 spécifiée dans le fichier de propriétés
    java8_link = java_apps['java8']
    match = re.search('.+\/(.+\.gz$)', java8_link)
    java8_version = match.group(1)
    if not java8_version:
        print('!! Erreur dans le chemin de téléchargement de jdk8\n')
        print('')
        exit(1)
    try:
        make_message('phase_title', PHASES['download']['title'], java8_version)
        java8_wget_cmd = ''.join([oracle_jdk_wget_cmd, java8_link])
        subprocess.check_call(java8_wget_cmd, shell=True)
        # Decompression dans /opt
        make_message('phase_title', PHASES['install']['title'], 'jdk8 dans /opt/jdk8')
        subprocess.check_call('sudo mkdir jdk8', shell=True)
        tar_cmd = ''.join(['tar -xzf ', java8_version, ' -C jdk8 --strip-components 1'])
        subprocess.check_call(tar_cmd, shell=True)
        subprocess.check_call('sudo chown -Rf root:root jdk8', shell=True)
        rm_jdk8_gz_cmd = ''.join(['sudo rm -f ', java8_version])
        subprocess.check_call(rm_jdk8_gz_cmd, shell=True)
        # Ajout de java8 oracle dans alternatives java
        print('** Ajout de java8 dans alternatives\n')
        subprocess.check_call('sudo update-alternatives --install /usr/bin/java java /opt/jdk8/bin/java 2', shell=True)
        subprocess.check_call('sudo update-alternatives --install /usr/bin/javac javac /opt/jdk8/bin/javac 2',
                              shell=True)
        subprocess.check_call('sudo update-alternatives --install /usr/bin/javaws javaws /opt/jdk8/bin/javaws 2',
                              shell=True)
    except Exception as e:
        make_message('error', PHASES['install']['fct'], 'jdk8', e)
        exit(1)
    # version de java par default
    try:
        print('** Configuration de java7 comme alternative par defaut')
        subprocess.check_call('sudo update-alternatives --set java /opt/jdk7/bin/java', shell=True)
        subprocess.check_call('sudo update-alternatives --set javac /opt/jdk7/bin/javac', shell=True)
        subprocess.check_call('sudo update-alternatives --set javaws /opt/jdk7/bin/javaws', shell=True)
        subprocess.check_call('java -version', shell=True)
    except Exception as e:
        make_message('error', PHASES['install']['fct'], 'java', e)
        exit(1)


def base_install(base_apps):
    make_message('section_title', 'BASE')
    make_message('app_lists', base_apps.keys())
    cmd = install_cmd.format(' '.join(list(base_apps.values())))
    try:
        subprocess.check_call(cmd, shell=True)
    except Exception as e:
        make_message('error', PHASES['install']['fct'], 'des dépendences de base', e)
        exit(1)


def python_install(python_apps):
    make_message('section_title', 'PYTHON')
    make_message('app_lists', python_apps.keys())
    try:
        python_apps_cmd = install_cmd.format(' '.join(list(python_apps.values())))
        subprocess.check_call(python_apps_cmd, shell=True)
    except Exception as e:
        make_message('error', PHASES['install']['fct'], 'des dépendences python', e)
        exit(1)


def add_debian_repo(repos):
    make_message('section_title', 'DEBIAN_REPO')
    make_message('app_lists', repos.keys())
    try:
        subprocess.check_call(clear_list_repo_file, shell=True)
        for key, value in repos.items():
            subprocess.check_call(add_repo_cmd.format(key, value), shell=True)
        subprocess.check_call('touch /etc/apt/preferences.d/pinning', shell=True)
        subprocess.check_call(add_pinning_cmd, shell=True)

    except Exception as e:
        make_message('error', PHASES['install']['title'], 'DEBIAN_REPO', e)
        exit(1)


def add_packages_keys(keys_urls):
    make_message('section_title', 'PACKAGE-KEY')
    try:
        for key, value in keys_urls.items():
            subprocess.check_call(add_package_key.format(value), shell=True)
        subprocess.check_call('sudo apt-get update', shell=True)
    except Exception as e:
        make_message('error', PHASES['install']['title'], 'PACKAGE-KEY', e)
        exit(1)


def install_drivers(drivers):
    make_message('section_title', 'DRIVERS')
    make_message('app_lists', drivers.keys())
    ret = []
    if 'intel-graphic' in drivers.keys():
        try:
            subprocess.check_call(install_testing_cmd.format(drivers['intel-graphic']), shell=True)
        except Exception as e:
            make_message('error', PHASES['install']['fct'], 'intel-graphic', e)
            ret.append('intel-graphic')
    if 'intel-wifi' in drivers.keys():
        try:
            subprocess.check_call(install_backports_cmd.format(drivers['intel-wifi']), shell=True)
        except Exception as e:
            make_message('error', PHASES['install']['fct'], 'intel-wifi', e)
            ret.append('intel-wifi')
    return ret


def postgresql_install(postgres_apps):
    make_message('section_title', 'POSTGRES_REPO')
    make_message('app_lists', postgres_apps.keys())
    try:
        subprocess.check_call(install_cmd.format(' '.join(list(postgres_apps.values()))), shell=True)
    except Exception as e:
        make_message('error', PHASES['install']['title'], 'dépendences postgres', e)


def install_media(media_apps):
    make_message('section_title', 'MEDIA')
    make_message('app_lists', media_apps.keys())
    try:
        subprocess.check_call(install_cmd.format(' '.join(list(media_apps.values()))), shell=True)
    except Exception as e:
        make_message('error', PHASES['install']['title'], 'dépendences média', e)
        return 1
    return 0


def install_mozilla(mozilla_apps):
    retval = 0
    ret = []
    make_message('section_title', 'MOZILLA')
    make_message('app_lists', mozilla_apps.keys())
    try:
        subprocess.check_call(
            'echo \'deb http://downloads.sourceforge.net/project/ubuntuzilla/mozilla/apt all main\' > /etc/apt/sources.list.d/ubuntuzilla.list',
            shell=True)
        subprocess.check_call('sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com C1289A29', shell=True)
        subprocess.check_call('sudo apt-get update', shell=True)
    except Exception as e:
        retval = 1
        make_message('error', PHASES['install']['title'], 'applications mozilla', e)
        ret = ['firefox', 'thunderbird']
    if retval == 0:
        if 'firefox' in mozilla_apps.keys():
            try:
                subprocess.check_call('sudo apt-get -y remove iceweasel', shell=True)
                subprocess.check_call('sudo apt-get -y install firefox', shell=True)
            except Exception as e:
                make_message('error', PHASES['install']['title'], 'firefox', e)
                ret.append('firefox')
        if 'thunderbird' in mozilla_apps.keys():
            try:
                subprocess.check_call('sudo apt-get -y remove icedove', shell=True)
                subprocess.check_call('sudo apt-get -y install thunderbird', shell=True)
            except Exception as e:
                make_message('error', PHASES['install']['title'], 'thunderbird', e)
                ret.append('thunderbird')
    return ret


def install_couchbase(couchbase_apps):
    retval = 0
    make_message('section_title', 'COUCHBASE')
    os.chdir('/opt')

    cb_link = couchbase_apps['couchbase']
    match = re.search('.+\/(couchbase.*\.deb$)', cb_link)
    cb_version = match.group(1)
    if not cb_version:
        print('!! Erreur dans le chemin de téléchargement de couchbase')
        print('')
        retval = 1
    if retval == 0:
        # Telechargement couchbase
        make_message('phase_title', PHASES['download']['title'], 'couchbase')
        try:
            subprocess.check_call(wget_app_cmd.format(cb_link), shell=True)
        except Exception as e:
            retval = 1
            make_message('error', PHASES['download']['fct'], 'couchbase', e)
            pass
    if retval == 0:
        # Instalation couchbase
        try:
            make_message('phase_title', PHASES['install']['title'], 'couchbase')
            subprocess.check_call(dpkg_install.format(''.join(['/opt/', cb_version])), shell=True)
            rm_atom_cmd = ''.join(['sudo rm -f ', cb_version])
            subprocess.check_call(rm_atom_cmd, shell=True)
        except Exception as e:
            retval = 1
            make_message('error', PHASES['install']['fct'], 'couchbase', e)
            pass
    return retval


def configure_git(git_config, os_user):
    ret = 0
    make_message('section_title', 'GIT-CONFIG')
    try:
        subprocess.check_call(
            execute_as_user.format(''.join(['git config --global user.name \'', git_config['name'], '\'']), os_user),
            shell=True)
        subprocess.check_call(
            execute_as_user.format(''.join(['git config --global user.username ', git_config['username']]), os_user),
            shell=True)
        subprocess.check_call(
            execute_as_user.format(''.join(['git config --global user.email ', git_config['email']]), os_user),
            shell=True)
    except Exception as e:
        make_message('error', PHASES['install']['title'], 'GIT-CONFIG', e)
        ret = 1
    return ret


def install_dev_tools(dev_apps, os_user):
    retval = 0
    failled_install = []
    make_message('section_title', 'DEV-TOOLS')
    make_message('app_lists', dev_apps.keys())
    os.chdir('/opt')

    if 'atom' in dev_apps.keys():
        print(''.join(['** Atom ', ]))
        ## Installation atom
        atom_link = dev_apps['atom']
        match = re.search('.+\/(atom.*\.deb$)', atom_link)
        atom_version = match.group(1)
        if not atom_version:
            print('!! Erreur dans le chemin de téléchargement de atom')
            print('')
            failled_install.append(atom_version)
            retval = 1
        if retval == 0:
            # Telechargement atom
            make_message('phase_title', PHASES['download']['title'], 'atom')
            try:
                subprocess.check_call(wget_app_cmd.format(atom_link), shell=True)
            except Exception as e:
                retval = 1
                failled_install.append(atom_version)
                make_message('error', PHASES['download']['fct'], 'atom', e)
                pass
        # TO-DO creation de l'entrée dans le menu
        if retval == 0:
            # Instalation atom
            try:
                make_message('phase_title', PHASES['install']['title'], 'atom')
                subprocess.check_call(dpkg_install.format(''.join(['/opt/', atom_version])), shell=True)
                rm_atom_cmd = ''.join(['sudo rm -f ', atom_version])
                subprocess.check_call(rm_atom_cmd, shell=True)
            except Exception as e:
                failled_install.append(atom_version)
                make_message('error', PHASES['install']['fct'], 'atom', e)
                pass
    retval = 0

    if 'netbeans' in dev_apps.keys():
        # Téléchargement de netbeans
        netbeans_link = dev_apps['netbeans']
        match = re.search('.+\/(netbeans.+\.sh$)', netbeans_link)
        netbeans_version = match.group(1)
        if not netbeans_version:
            print('!! Erreur dans le chemin de téléchargement de netbeans')
            print('')
            failled_install.append(netbeans_version)
            retval = 1
        if retval == 0:
            make_message('phase_title', PHASES['download']['title'], 'netbeans')
            try:
                subprocess.check_call(wget_app_cmd.format(netbeans_link), shell=True)
            except Exception as e:
                retval = 1
                failled_install.append(netbeans_version)
                make_message('error', PHASES['download']['fct'], 'netbeans', e)
                pass
            # TO-DO creation de l'entrée dans le menu
            if retval == 0:
                ## Installation de netbeans
                make_message('phase_title', PHASES['install']['title'], netbeans_version)
                try:
                    subprocess.check_call('sudo mkdir /opt/netbeans', shell=True)
                    netbeans_path = ''.join(['/opt/', netbeans_version])
                    netbeans_args = ' --silent --javahome /opt/jdk7 -J-Dnb-base.installation.location=/opt/netbeans'
                    netbean_install_cmd = ''.join(['sudo /bin/sh ', netbeans_path, netbeans_args])
                    subprocess.check_call(netbean_install_cmd, shell=True)
                    subprocess.check_call(chown_cmd.format(os_user, os_user, '/opt/netbeans'), shell=True)
                    rm_netbeans_cmd = ''.join(['sudo rm -f ', netbeans_path])
                    subprocess.check_call(rm_netbeans_cmd, shell=True)
                except Exception as e:
                    failled_install.append(netbeans_version)
                    make_message('error', PHASES['install']['fct'], 'netbeans', e)
                    pass
    retval = 0

    if 'pycharm' in dev_apps.keys():
        ##Télécharger pycharm
        pycharm_link = dev_apps['pycharm']
        match = re.search('.+\/(pycharm.+\.gz$)', pycharm_link)
        pycharm_version = match.group(1)
        if not pycharm_version:
            print('')
            print('!! Erreur dans le chemin de téléchargement de pycharm')
            print('')
            failled_install.append(pycharm_version)
            retval = 1
        if retval == 0:
            make_message('phase_title', PHASES['download']['title'], 'pycharm')
            try:
                subprocess.check_call(wget_app_cmd.format(pycharm_link), shell=True)
            except Exception as e:
                retval = 1
                failled_install.append(pycharm_version)
                make_message('error', PHASES['download']['fct'], 'pycharm', e)
                pass
            if retval == 0:
                ## Installation de pycharm
                make_message('phase_title', PHASES['install']['title'], pycharm_version)
                try:
                    subprocess.check_call('sudo mkdir /opt/pycharm', shell=True)
                    pycharm_path = ''.join(['/opt/', pycharm_version])
                    tar_cmd = ''.join(['sudo tar -xzf ', pycharm_path, ' -C /opt/pycharm --strip-components 1'])
                    subprocess.check_call(tar_cmd, shell=True)
                    subprocess.check_call(chown_cmd.format(os_user, os_user, '/opt/pycharm'), shell=True)
                    rm_pycharm_cmd = ''.join(['sudo rm -f ', pycharm_path])
                    subprocess.check_call(rm_pycharm_cmd, shell=True)
                except Exception as e:
                    failled_install.append(pycharm_version)
                    make_message('error', PHASES['install']['fct'], 'pycharm', e)
                    pass
                make_desktop_entry(os_user=os_user,
                                   app_short_name='pycharm',
                                   app_name='PyCharm',
                                   exec_path='/bin/sh /opt/pycharm/bin/pycharm.sh',
                                   icon_path='/opt/pycharm/bin/pycharm.png')
        print('')
    retval = 0

    if 'sql-developer' in dev_apps.keys():
        ## Telechargement de sqldevelopper
        # sqldeveloper_link = config['DEV-TOOLS']['sql-developer']
        # match = re.search('.+\/(sqldeveloper.+\.zip$)',sqldeveloper_link)
        # sqldeveloper_version = match.group(1)
        sqldeveloper_version = dev_apps['sql-developer']
        if not sqldeveloper_version:
            print('')
            print('!! Erreur dans le chemin de téléchargement de sqldeveloper')
            print('')
            failled_install.append(sqldeveloper_version)
            retval = 1
        if retval == 0:
            # oracle_sql_wget_cmd = ''.join([wget_cmd,' --header "Cookie: oraclelicense=accept-securebackup-cookie" --http-user=',
            #                                user_config['ORACLE']['oracle_user'],
            #                                ' --http-password=',
            #                                user_config['ORACLE']['oracle_password']])
            # sqldeveloper_wget_cmd=' '.join([oracle_sql_wget_cmd,sqldeveloper_link])
            # print(''.join(['* Téléchargement ',sqldeveloper_version]))
            sql_dev = os.path.join(TOOLS_FOLDER, sqldeveloper_version)
            cp_cmd = ''.join(['sudo cp ', sql_dev, ' ./'])
            try:
                subprocess.check_call(cp_cmd, shell=True)
            except Exception as e:
                retval = 1
                failled_install.append(sqldeveloper_version)
                make_message('error', PHASES['download']['fct'], 'sql-developer', e)
                pass
            if retval == 0:
                ## Installation sql-developer
                make_message('phase_title', PHASES['install']['title'], sqldeveloper_version)
                try:
                    sqldev_path = ''.join(['/opt/', sqldeveloper_version])
                    unzip_cmd = ''.join(['sudo unzip -q ', sqldev_path])
                    subprocess.check_call(unzip_cmd, shell=True)
                    subprocess.check_call(chown_cmd.format(os_user, os_user, '/opt/sqldeveloper'), shell=True)
                    rm_sqldev_cmd = ''.join(['sudo rm -f ', sqldev_path])
                    subprocess.check_call(rm_sqldev_cmd, shell=True)
                    # configuration du jdk
                    subprocess.check_call(
                        'echo \'SetJavaHome /opt/jdk8\n\' >> /opt/sqldeveloper/sqldeveloper/bin/sqldeveloper.conf',
                        shell=True)
                except Exception as e:
                    failled_install.append(sqldeveloper_version)
                    make_message('error', PHASES['install']['fct'], 'sql-developer', e)
                    pass
                make_desktop_entry(os_user, app_short_name='sqldeveloper',
                                   app_name='SqlDeveloper',
                                   exec_path='/bin/sh /opt/sqldeveloper/sqldeveloper.sh',
                                   icon_path='/opt/sqldeveloper/icon.png')
    retval = 0
    if 'visual-paradigm' in dev_apps.keys():
        ## Telechargement de vp
        vp_link = dev_apps['visual-paradigm']
        match = re.search('.+\/(Visual_Paradigm.+\.sh$)', vp_link)
        vp_version = match.group(1)
        if not vp_version:
            print('')
            print('!! Erreur dans le chemin de téléchargement de visual-paradigm')
            print('')
            failled_install.append(vp_version)
            retval = 1
        if retval == 0:
            make_message('phase_title', PHASES['download']['title'], vp_version)
            try:
                subprocess.check_call(wget_app_cmd.format(vp_link), shell=True)
            except Exception as e:
                retval = 1
                failled_install.append(vp_version)
                make_message('error', PHASES['download']['fct'], 'visual-paradigm', e)
                pass
            if retval == 0:
                try:
                    ## Installation Visual Paradigm
                    make_message('phase_title', PHASES['install']['title'], vp_version)
                    subprocess.check_call('sudo mkdir /opt/visual-paradigm', shell=True)
                    vp_path = ''.join(['/opt/', vp_version])
                    vp_args = ' -q -dir /opt/visual-paradigm'
                    vp_install_cmd = ''.join(['sudo /bin/sh ', vp_path, vp_args])
                    subprocess.check_call(vp_install_cmd, shell=True)
                    subprocess.check_call(chown_cmd.format(os_user, os_user, '/opt/visual-paradigm'), shell=True)
                    rm_vp_cmd = ''.join(['sudo rm -f ', vp_path])
                    subprocess.check_call(rm_vp_cmd, shell=True)
                except Exception as e:
                    failled_install.append(vp_version)
                    make_message('error', PHASES['install']['fct'], 'visual-paradigm', e)
                    pass

    if 'intellij' in dev_apps.keys():
        ##Télécharger intellij
        intellij_link = dev_apps['intellij']
        match = re.search('.+\/(idea.+\.gz$)', intellij_link)
        intellij_version = match.group(1)
        if not intellij_version:
            print('')
            print('!! Erreur dans le chemin de téléchargement de intellij')
            print('')
            failled_install.append(intellij_version)
            retval = 1
        if retval == 0:
            make_message('phase_title', PHASES['download']['title'], intellij_version)
            try:
                subprocess.check_call(wget_app_cmd.format(intellij_link), shell=True)
            except Exception as e:
                retval = 1
                failled_install.append(intellij_version)
                make_message('error', PHASES['download']['fct'], 'intellij', e)
                pass
            if retval == 0:
                ## Installation de intellij
                make_message('phase_title', PHASES['install']['title'], intellij_version)
                try:
                    subprocess.check_call('sudo mkdir /opt/intellij', shell=True)
                    intellij_path = ''.join(['/opt/', intellij_version])
                    tar_cmd = ''.join(['sudo tar -xzf ', intellij_path, ' -C /opt/intellij --strip-components 1'])
                    subprocess.check_call(tar_cmd, shell=True)
                    subprocess.check_call(chown_cmd.format(os_user, os_user, '/opt/intellij'), shell=True)
                    rm_intellij_cmd = ''.join(['sudo rm -f ', intellij_path])
                    subprocess.check_call(rm_intellij_cmd, shell=True)
                except Exception as e:
                    failled_install.append(intellij_version)
                    make_message('error', PHASES['install']['fct'], 'intellij', e)
                    pass
                make_desktop_entry(os_user=os_user,
                                   app_short_name='intellij',
                                   app_name='IntelliJ',
                                   exec_path='/bin/sh /opt/intellij/bin/idea.sh',
                                   icon_path='/opt/intellij/bin/idea.png')
    if 'android-studio' in dev_apps.keys():
        ##Télécharger android-studio
        android_studio_link = dev_apps['android-studio']
        match = re.search('.+\/(android-studio-ide.+\.zip$)', android_studio_link)
        android_studio_version = match.group(1)
        if not android_studio_version:
            print('')
            print('!! Erreur dans le chemin de téléchargement de android-studio')
            print('')
            failled_install.append(android_studio_version)
            retval = 1
        if retval == 0:
            make_message('phase_title', PHASES['download']['title'], android_studio_link)
            try:
                subprocess.check_call(wget_app_cmd.format(android_studio_link), shell=True)
            except Exception as e:
                retval = 1
                failled_install.append(android_studio_version)
                make_message('error', PHASES['download']['fct'], 'android-studio', e)
                pass
            if retval == 0:
                ## Installation de android_studio
                make_message('phase_title', PHASES['install']['title'], android_studio_version)
                try:
                    unzip_cmd = ''.join(['sudo unzip -q /opt/', android_studio_version])
                    subprocess.check_call(unzip_cmd, shell=True)
                    subprocess.check_call(chown_cmd.format(os_user, os_user, '/opt/android-studio'), shell=True)
                    rm_android_studio_cmd = ''.join(['sudo rm -f /opt/', android_studio_version])
                    subprocess.check_call(rm_android_studio_cmd, shell=True)
                except Exception as e:
                    failled_install.append(android_studio_version)
                    make_message('error', PHASES['install']['fct'], 'android-studio', e)
                    pass
                make_desktop_entry(os_user=os_user,
                                   app_short_name='android-studio',
                                   app_name='Android Studio',
                                   exec_path='/bin/sh /opt/android-studio/bin/studio.sh',
                                   icon_path='/opt/android-studio/bin/studio.png')
        print('')
    retval = 0

    if 'lein' in dev_apps.keys():
        ##Télécharger lein
        lein_link = dev_apps['lein']
        make_message('phase_title', PHASES['download']['title'], lein_link)
        try:
            subprocess.check_call(wget_app_cmd.format(lein_link), shell=True)
        except Exception as e:
            retval = 1
            failled_install.append('lein')
            make_message('error', PHASES['download']['fct'], 'lein', e)
            pass
        if retval == 0:
            ## Installation de lein
            make_message('phase_title', PHASES['install']['title'], 'lein')
            try:
                subprocess.check_call('sudo mkdir /opt/clojure', shell=True)
                subprocess.check_call('sudo mkdir /opt/clojure/bin', shell=True)
                subprocess.check_call('sudo mv /opt/lein /opt/clojure/bin/lein', shell=True)
                subprocess.check_call('sudo chmod a+x /opt/clojure/bin/lein', shell=True)
                subprocess.check_call('ln -s /opt/clojure/bin/lein /usr/bin/lein', shell=True)
                subprocess.check_call(chown_cmd.format(os_user, os_user, '/opt/clojure/bin/lein'), shell=True)
            except Exception as e:
                failled_install.append('lein')
                make_message('error', PHASES['install']['fct'], 'android-studio', e)
                pass
    retval = 0

    if 'omyzsh' in dev_apps.keys():
        omyzsh_link = dev_apps['omyzsh']
        print('** Installation oh-my-zsh')
        try:
            subprocess.check_call(
                execute_as_user.format(''.join(['sh -c \"$(wget ',omyzsh_link, ' -O -)\"']), os_user))
            subprocess.check_call('git clone https://github.com/powerline/fonts.git')
            subprocess.check_call('sudo /bin/sh /opt/fonts/install.sh')
        except Exception as e:
            failled_install.append('oh-my-zsh')
            make_message('error', PHASES['install']['fct'], 'omyzsh', e)

    return failled_install


def make_desktop_entry(os_user, app_short_name, app_name, exec_path, icon_path):
    retval = 0
    application_desktop_dir = ''.join(['/home/', os_user, '/.local/share/applications'])
    if not os.path.isdir(application_desktop_dir):
        mkdir_cmd = ''.join(['sudo mkdir ', application_desktop_dir])
        try:
            subprocess.check_call(mkdir_cmd, shell=True)
        except Exception as e:
            print('')
            print(''.join(['!! Erreur lors de la création du dektop_enytry ', app_name]))
            print('')
            retval = 1
    if retval == 0:
        try:
            app_desktop_path = ''.join([application_desktop_dir, '/', app_short_name, '.desktop'])
            desktop_content = desktop_entry.format(name=app_name, exe=exec_path, icon=icon_path)
            with open(app_desktop_path, "a+") as f:
                f.write(desktop_content)
        except Exception as e:
            print('')
            print(''.join(['!! Erreur lors de la création du dektop_enytry ', app_name]))
            print('')
            retval = 1
    return retval


def clone_git_repo(dest_path,git_url) :
    ret = 0
    mkdir_dest_cmd = ''.join(['mkdir ',dest_path])
    git_clone_cmd = ''.join(['git clone ',git_url,' ',dest_path])
    make_message('clone_git_repo')
    try :
        subprocess.check_call(mkdir_dest_cmd,shell=True)
        subprocess.check_call(git_clone_cmd,shell=True)
    except Exception as e :
        ret = 1
        make_message('error', PHASES['install']['fct'], 'CLONE-GIT-REPO', e)
    return ret

