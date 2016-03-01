#!/usr/bin/env python3
import fileinput
import os,sys,subprocess,configparser

# Script d'installation de l'environnement de devéloppement OSIS - SIPS
#
# OS : Debian 8
# Languages de développement : Python3, Java, Clojure
# Outils : Atom, Netbeans, Pycharm, SqlDevelopper, Visual Paradigm
#

# Fichier contenant les applications et dépendances à installer
import pwd
import re

APPS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apps.properties")

# Fichier de configuration de l'utilisateur
USER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user.properties")


# Dossier contenant les outils à installer
# Par défaut , dossier tools à la racine
TOOLS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")


def base_tests(config,user_config):
    # Test si l'utilisateur à les droits admin
    if os.geteuid() != 0:
        print('')
        print ('Utilisateur doit avoir les droits administrateur')
        print ('Lancez le script en root')
        exit(1)

    ## Validation du fichier de propriétés
    # Test les données obligatoiure du fichier user.properties
    if not user_config['BASE']['os_user']:
        print('')
        print ('Le paramètre os_user doit être défini dans le fichier user.properties')
        exit(1)
    if not user_config['GIT']['name'] \
            or not user_config['GIT']['email'] \
            or not user_config['GIT']['username'] :
        print('')
        print ('Les paramètres GIT doivent être définis dans le fichier user.properties')
        exit(1)
    #Test si l'utilisateur spécifié dans le fichier user.properties existe bien sur l'OS
    try :
        pwd.getpwnam(user_config['BASE']['os_user'])
    except :
        print('')
        print (''.join(['L\'utilisateur ',user_config['BASE']['os_user'],' n\'existe pas sur le système']))
        exit(1)
    #Test si sqldeveloper doit être installé et si les données de connexion oracle existent
    # if config['DEV-TOOLS']['sql-developer'] and \
    #     not ( user_config['ORACLE']['oracle_user'] or user_config['ORACLE']['oracle_password']) :
    #     print('')
    #     print('Vous avez spécifié l\'installation de sqldeveloper sans forunir les données de connexion Oracle')
    #     print('Supprimez sqldevelopeur des DEV-TOOLS à installer dans apps.properties ou complétez les données de connexion Oracle dans user.properties')
    #     exit(1)
    # Test si sqldeveloper doit être installé et si l'archive est présente dans le dossier tools
    if 'sql-developer' in config['DEV-TOOLS'] and not os.path.isfile(os.path.join(TOOLS_FOLDER,config['DEV-TOOLS']['sql-developer'])):
        print('')
        print('Vous avez spécifié l\'installation de sqldeveloper sans founir l\'archive nécéssaire')
        exit(0)
    # Le script ne fonctionne que si python3 est présent sur le système
    try :
        subprocess.check_output('which python3',shell=True,universal_newlines=True)
    except :
        print('')
        print('!! Python3 doit être présent sur le système et accèssible dans le $PATH')
        exit(1)


def sudo_install(config,user_config) :
    ### Installation de sudo
    print('*** Installation de sudo ***')
    subprocess.check_call('sudo apt-get install sudo',shell=True)
    print('')
    ## Ajout de l'utilisateur dans sudo
    print('**Ajout de l\'utilisateur dans groupe sudo')
    add_user_to_group_sudo_cmd = ''.join(['sudo usermod -a -G sudo ',user_config['BASE']['os_user']])
    subprocess.check_call(add_user_to_group_sudo_cmd,shell=True)
    print('')


def java_install(config,wget_cmd) :
    java_apps = config['JAVA']
    print('*** Installation des dépendance java7 et 8 ***')
    print('\n'.join(java_apps.keys()))
    print('')
    os.chdir('/opt')
    oracle_jdk_wget_cmd = ''.join([wget_cmd,' --header "Cookie: oraclelicense=accept-securebackup-cookie" '])

    #Téléchargement de la version de java7 spécifiée dans le fichier de propriétés
    java7_link = config['JAVA']['java7']
    match = re.search('.+\/(.+\.gz$)',java7_link)
    java7_version = match.group(1)
    if not java7_version :
        print ('!! Erreur dans ee chemin de téléchargement de jdk7')
        print('')
        exit(1)
    try:
        print(''.join(['** Téléchargement de ',java7_version]))
        java7_wget_cmd = ''.join([oracle_jdk_wget_cmd,java7_link])
        subprocess.check_call(java7_wget_cmd,shell=True)
        # Decompression dans /opt
        print('** Installation jdk7 dans /opt/jdk7')
        subprocess.check_call('sudo mkdir jdk7',shell=True)
        tar_cmd = ''.join(['sudo tar -xzf ', java7_version, ' -C jdk7 --strip-components 1'])
        subprocess.check_call(tar_cmd,shell=True)
        subprocess.check_call('sudo chown -Rf root:root jdk7',shell=True)
        rm_jdk7_gz_cmd = ''.join(['sudo rm -f ',java7_version])
        subprocess.check_call(rm_jdk7_gz_cmd,shell=True)
        # Ajout de java7 oracle dans alternatives java
        print('** Ajout de java7 dans alternatives')
        subprocess.check_call('sudo update-alternatives --install /usr/bin/java java /opt/jdk7/bin/java 1',shell=True)
        subprocess.check_call('sudo update-alternatives --install /usr/bin/javac javac /opt/jdk7/bin/javac 1',shell=True)
        subprocess.check_call('sudo update-alternatives --install /usr/bin/javaws javaws /opt/jdk7/bin/javaws 1',shell=True)
    except :
        print ('!! Erreur dans l\'installation de jdk7')
        print('')
        exit(1)

    #Téléchargement de la version de java8 spécifiée dans le fichier de propriétés
    java8_link = config['JAVA']['java8']
    match = re.search('.+\/(.+\.gz$)',java8_link)
    java8_version = match.group(1)
    if not java8_version :
        print ('!! Erreur dans le chemin de téléchargement de jdk8')
        print('')
        exit(1)
    try :
        print(''.join(['** Téléchargement de ',java8_version]))
        java8_wget_cmd = ''.join([oracle_jdk_wget_cmd,java8_link])
        subprocess.check_call(java8_wget_cmd,shell=True)
        # Decompression dans /opt
        print('** Installation jdk8 dans /opt/jdk8')
        subprocess.check_call('sudo mkdir jdk8',shell=True)
        tar_cmd = ''.join(['tar -xzf ',java8_version,' -C jdk8 --strip-components 1'])
        subprocess.check_call(tar_cmd,shell=True)
        subprocess.check_call('sudo chown -Rf root:root jdk8',shell=True)
        rm_jdk8_gz_cmd = ''.join(['sudo rm -f ',java8_version])
        subprocess.check_call(rm_jdk8_gz_cmd,shell=True)
        # Ajout de java8 oracle dans alternatives java
        print('** Ajout de java8 dans alternatives')
        subprocess.check_call('sudo update-alternatives --install /usr/bin/java java /opt/jdk8/bin/java 2',shell=True)
        subprocess.check_call('sudo update-alternatives --install /usr/bin/javac javac /opt/jdk8/bin/javac 2',shell=True)
        subprocess.check_call('sudo update-alternatives --install /usr/bin/javaws javaws /opt/jdk8/bin/javaws 2',shell=True)
    except :
        print ('!! Erreur dans l\'installation de jdk8')
        print('')
        exit(1)
    # version de java par default
    try :
        print('** Configuration de java7 comme alternative par defaut')
        subprocess.check_call('sudo update-alternatives --set java /opt/jdk7/bin/java',shell=True)
        subprocess.check_call('sudo update-alternatives --set javac /opt/jdk7/bin/javac',shell=True)
        subprocess.check_call('sudo update-alternatives --set javaws /opt/jdk7/bin/javaws',shell=True)
        subprocess.check_call('java -version',shell=True)
    except :
        print ('!! Erreur dans l\'installation de java')
        print('')
        exit(1)


def base_install(config,install_cmd) :
    base_apps = config['BASE']
    print('*** Installation des dépendances de base ***')
    print('\n'.join(base_apps.keys()))
    print('')
    try :
        base_apps_cmd = ' '.join([install_cmd] + list(base_apps.values()))
        subprocess.check_call(base_apps_cmd,shell=True)
    except :
        print ('!! Erreur dans l\'installation des dépendences de base')
        print('')
        exit(1)


def python_install(config,install_cmd) :
    python_apps = config['PYTHON']
    print('*** Installation des dépendances python3 ***')
    print('\n'.join(python_apps.keys()))
    print('')
    try :
        python_apps_cmd = ' '.join([install_cmd] + list(python_apps.values()))
        subprocess.check_call(python_apps_cmd,shell=True)
    except :
        print ('!! Erreur dans l\'installation des dépendences python')
        print('')
        exit(1)


def postgresql_install(config,install_cmd):
    postgres_apps = config['POSTGRES']
    print('*** Installation des dépendances postgres ***')
    print('\n'.join(postgres_apps.keys()))
    print('')
    try :
        postgres_apps_cmd = ' '.join([install_cmd] + list(postgres_apps.values()))
        subprocess.check_call(postgres_apps_cmd,shell=True)
    except :
        print ('!! Erreur dans l\'installation des dépendences postgres')
        print('')
        exit(1)


def install_media(config,install_cmd):
    media_apps = config['MEDIA']
    print('*** Installation des applications media ***')
    print('\n'.join(media_apps.keys()))
    print('')
    try :
        media_apps_cmd = ' '.join([install_cmd] + list(media_apps.values()))
        subprocess.check_call(media_apps_cmd,shell=True)
    except :
        print ('!! Erreur dans l\'installation des application media')
        print('')
        return 1
    return 0


def install_mozilla(config):
    retval = 0
    ret = []
    mozilla_apps = config['MOZILLA']
    print('*** Installation des applications mozilla ***')
    print('\n'.join(mozilla_apps.keys()))
    print('')
    try :
        subprocess.check_call('echo \'deb http://downloads.sourceforge.net/project/ubuntuzilla/mozilla/apt all main\' > /etc/apt/sources.list.d/ubuntuzilla.list',shell=True)
        subprocess.check_call('sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com C1289A29',shell=True)
        subprocess.check_call('sudo apt-get update')
    except :
        retval = 1
        print ('!! Erreur dans l\'installation des applications mozilla')
        ret = ['firefox','thunderbird']
        print('')
    if retval == 0 :
        if 'firefox' in config['MOZILLA'] :
            try :
                subprocess.check_call('sudo apt-get remove iceweasel',shell=True)
                subprocess.check_call('sudo apt-get install firefox')
            except :
                print ('!! Erreur dans l\'installation de firefox')
                ret.append('firefox')
                print('')
        if 'thunderbird' in config['MOZILLA'] :
            try :
                subprocess.check_call('sudo apt-get remove icedove',shell=True)
                subprocess.check_call('sudo apt-get install thunderbird')
            except :
                print ('!! Erreur dans l\'installation de thunderbird')
                ret.append('thunderbird')
                print('')
    return ret

def install_dev_tools(config,user_config,wget_cmd,install_cmd,chown_cmd) :

    retval = 0
    failled_install = []

    dev_apps = config['DEV-TOOLS']
    print('*** Installation des outils de développement ***')
    print('\n'.join(dev_apps.keys()))
    print('')
    os.chdir('/opt')

    if 'atom' in config['DEV-TOOLS'] :
        print(''.join(['** Atom ',]))
        ## Installation atom
        atom_link = config['DEV-TOOLS']['atom']
        match = re.search('.+\/(.+\.deb$)',atom_link)
        atom_version = match.group(1)
        if not atom_version :
            print ('!! Erreur dans le chemin de téléchargement de atom')
            print('')
            failled_install.append(atom_version)
            retval = 1
        if retval == 0 :
            atom_wget_cmd = ' '.join([wget_cmd,atom_link])
            #Telechargement atom
            print(''.join(['** Telechargement ',atom_version]))
            try :
                subprocess.check_call(atom_wget_cmd,shell=True)
            except :
                retval = 1
                failled_install.append(atom_version)
                print(''.join(['!! Echec téléchargement ',atom_version]))
                print('')
                pass
        # TO-DO creation de l'entrée dans le menu
        if retval == 0 :
            #Instalation atom
            try :
                print(''.join(['** Installation ',atom_version]))
                subprocess.check_call('sudo apt-get install gvfs-bin',shell=True)
                atom_install_cmd = ''.join(['sudo dpkg -i /opt/',atom_version])
                subprocess.check_call(atom_install_cmd,shell=True)
                rm_atom_cmd = ''.join(['sudo rm -f ',atom_version])
                subprocess.check_call(rm_atom_cmd,shell=True)
            except :
                failled_install.append(atom_version)
                print(''.join(['!! Echec installation ',atom_version]))
                print('')
                pass
    retval = 0

    if 'netbeans' in config['DEV-TOOLS'] :
        # Téléchargement de netbeans
        netbeans_link = config['DEV-TOOLS']['netbeans']
        match = re.search('.+\/(netbeans.+\.sh$)',netbeans_link)
        netbeans_version = match.group(1)
        if not netbeans_version :
            print ('!! Erreur dans le chemin de téléchargement de netbeans')
            print('')
            failled_install.append(netbeans_version)
            retval = 1
        if retval == 0 :
            netbeans_wget_cmd=' '.join([wget_cmd,netbeans_link])
            print(''.join(['* Téléchargement ',netbeans_version]))
            try :
                subprocess.check_call(netbeans_wget_cmd,shell=True)
            except :
                retval = 1
                failled_install.append(netbeans_version)
                print(''.join(['!! Echec téléchargement ',netbeans_version]))
                print('')
                pass
            # TO-DO creation de l'entrée dans le menu
            if retval == 0 :
                ## Installation de netbeans
                print(''.join(['** Installation ',netbeans_version]))
                try :
                    subprocess.check_call('sudo mkdir /opt/netbeans',shell=True)
                    netbeans_path = ''.join(['/opt/',netbeans_version])
                    netbeans_args = ' --silent -J-Dnb-base.installation.location=/opt/netbeans -J-Djdk.installation.location=/opt/jdk7 J-Dnb-base.jdk.location=/opt/jdk7'
                    netbean_install_cmd=''.join(['sudo /bin/sh ',netbeans_path,netbeans_args])
                    subprocess.check_call(netbean_install_cmd,shell=True)
                    netbeans_chown_cmd = ''.join([chown_cmd,' /opt/netbeans'])
                    subprocess.check_call(netbeans_chown_cmd,shell=True)
                    rm_netbeans_cmd = ''.join(['sudo rm -f ',netbeans_path])
                    subprocess.check_call(rm_netbeans_cmd,shell=True)
                except :
                    failled_install.append(netbeans_version)
                    print(''.join(['!! Echec installation ',netbeans_version]))
                    print('')
                    pass
    retval = 0

    if 'pycharm' in config['DEV-TOOLS'] :
        ##Télécharger pycharm
        pycharm_link = config['DEV-TOOLS']['pycharm']
        match = re.search('.+\/(pycharm.+\.gz$)',pycharm_link)
        pycharm_version = match.group(1)
        if not pycharm_version :
            print('')
            print ('!! Erreur dans le chemin de téléchargement de pycharm')
            print('')
            failled_install.append(pycharm_version)
            retval = 1
        if retval == 0 :
            pycharm_wget_cmd=' '.join([wget_cmd,pycharm_link])
            print(''.join(['* Téléchargement ',pycharm_version]))
            try :
                subprocess.check_call(pycharm_wget_cmd,shell=True)
            except :
                retval = 1
                failled_install.append(pycharm_version)
                print('')
                print(''.join(['!! Echec téléchargement ',pycharm_version]))
                print('')
                pass
            if retval == 0 :
                ## Installation de pycharm
                print(''.join(['** Installation ',pycharm_version]))
                try :
                    subprocess.check_call('sudo mkdir /opt/pycharm',shell=True)
                    pycharm_path=''.join(['/opt/',pycharm_version])
                    tar_cmd = ''.join(['sudo tar -xzf ',pycharm_path,' -C /opt/pycharm --strip-components 1'])
                    subprocess.check_call(tar_cmd,shell=True)
                    pycharm_chown_cmd=''.join([chown_cmd,' /opt/pycharm'])
                    subprocess.check_call(pycharm_chown_cmd,shell=True)
                    rm_pycharm_cmd = ''.join(['sudo rm -f ',pycharm_path])
                    subprocess.check_call(rm_pycharm_cmd,shell=True)
                except :
                    failled_install.append(pycharm_version)
                    print('')
                    print(''.join(['!! Echec installation ',pycharm_version]))
                    print('')
                    pass
                make_desktop_entry(user_config=user_config,
                                   app_short_name='pycharm',
                                   app_name='PyCharm',
                                   exec_path='/bin/sh /opt/pycharm/bin/pycharm.sh',
                                   icon_path='/opt/pycharm/bin/pycharm.png')
        print('')
    retval=0

    if 'sql-developer' in config['DEV-TOOLS'] :
        ## Telechargement de sqldevelopper
        # sqldeveloper_link = config['DEV-TOOLS']['sql-developer']
        # match = re.search('.+\/(sqldeveloper.+\.zip$)',sqldeveloper_link)
        # sqldeveloper_version = match.group(1)
        sqldeveloper_version = config['DEV-TOOLS']['sql-developer']
        if not sqldeveloper_version :
            print('')
            print ('!! Erreur dans le chemin de téléchargement de sqldeveloper')
            print('')
            failled_install.append(sqldeveloper_version)
            retval = 1
        if retval == 0 :
            # oracle_sql_wget_cmd = ''.join([wget_cmd,' --header "Cookie: oraclelicense=accept-securebackup-cookie" --http-user=',
            #                                user_config['ORACLE']['oracle_user'],
            #                                ' --http-password=',
            #                                user_config['ORACLE']['oracle_password']])
            # sqldeveloper_wget_cmd=' '.join([oracle_sql_wget_cmd,sqldeveloper_link])
            # print(''.join(['* Téléchargement ',sqldeveloper_version]))
            sql_dev = os.path.join(TOOLS_FOLDER,sqldeveloper_version)
            cp_cmd = ''.join(['sudo cp ',sql_dev,' ./'])
            try :
                subprocess.check_call(cp_cmd,shell=True)
            except :
                retval = 1
                failled_install.append(sqldeveloper_version)
                print('')
                print(''.join(['!! Echec téléchargement ',sqldeveloper_version]))
                print('')
                pass
            if retval == 0 :
                ## Installation sql-developer
                print(''.join(['** Installation ',sqldeveloper_version]))
                try :
                    sqldev_path=''.join(['/opt/',sqldeveloper_version])
                    unzip_cmd = ''.join(['sudo unzip -q ',sqldev_path])
                    subprocess.check_call(unzip_cmd,shell=True)
                    sqldev_chown_cmd=''.join([chown_cmd,' /opt/sqldeveloper'])
                    subprocess.check_call(sqldev_chown_cmd,shell=True)
                    rm_sqldev_cmd = ''.join(['sudo rm -f ',sqldev_path])
                    subprocess.check_call(rm_sqldev_cmd,shell=True)
                    #configuration du jdk
                    for line in fileinput.input('/opt/sqldeveloper/sqldeveloper/bin/sqldeveloper.conf',inplace=1) :
                        match = re.search('(SetJavaHome.+)',line)
                        if match.group(1) :
                            line.replace(match.group(1),'SetJavaHome /opt/jdk8')
                        sys.stdout.write(line)
                except :
                    failled_install.append(sqldeveloper_version)
                    print('')
                    print(''.join(['!! Echec installation ',sqldeveloper_version]))
                    print('')
                    pass
                make_desktop_entry(user_config,app_short_name='sqldeveloper',
                                   app_name='SqlDeveloper',
                                   exec_path='/bin/sh /opt/sqldeveloper/sqldeveloper.sh',
                                   icon_path='/opt/sqldeveloper/sqldeveloper/bin/splash.png')
    retval = 0

    if 'visual-paradigm' in config['DEV-TOOLS'] :
        ## Telechargement de vp
        vp_link = config['DEV-TOOLS']['visual-paradigm']
        match = re.search('.+\/(Visual_Paradigm.+\.sh$)',vp_link)
        vp_version = match.group(1)
        if not vp_version :
            print('')
            print ('!! Erreur dans le chemin de téléchargement de visual-paradigm')
            print('')
            failled_install.append(vp_version)
            retval = 1
        if retval == 0 :
            vp_wget_cmd=' '.join([wget_cmd,vp_link])
            print(''.join(['* Téléchargement ',vp_version]))
            try :
                subprocess.check_call(vp_wget_cmd,shell=True)
            except :
                retval = 1
                failled_install.append(vp_version)
                print('')
                print(''.join(['!! Echec téléchargement ',vp_version]))
                print('')
                pass
            if retval == 0 :
                try :
                    ## Installation Visual Paradigm
                    subprocess.check_call('sudo mkdir /opt/visual-paradigm',shell=True)
                    vp_path=''.join(['/opt/',vp_version])
                    vp_args = ' -q -dir /opt/visual-paradigm'
                    vp_install_cmd=''.join(['sudo /bin/sh ',vp_path,vp_args])
                    subprocess.check_call(vp_install_cmd,shell=True)
                    vp_chown_cmd=''.join([chown_cmd,' /opt/visual-paradigm'])
                    subprocess.check_call(vp_chown_cmd,shell=True)
                    rm_vp_cmd = ''.join(['sudo rm -f ',vp_path])
                    subprocess.check_call(rm_vp_cmd,shell=True)
                except :
                    failled_install.append(vp_version)
                    print('')
                    print(''.join(['!! Echec installation ',vp_version]))
                    print('')
                    pass

    if 'intellij' in config['DEV-TOOLS'] :
        ##Télécharger intellij
        intellij_link = config['DEV-TOOLS']['intellij']
        match = re.search('.+\/(ideaIC.+\.gz$)',intellij_link)
        intellij_version = match.group(1)
        if not intellij_version :
            print('')
            print ('!! Erreur dans le chemin de téléchargement de intellij')
            print('')
            failled_install.append(intellij_version)
            retval = 1
        if retval == 0 :
            intellij_wget_cmd=' '.join([wget_cmd,intellij_link])
            print(''.join(['* Téléchargement ',intellij_version]))
            try :
                subprocess.check_call(intellij_wget_cmd,shell=True)
            except :
                retval = 1
                failled_install.append(intellij_version)
                print('')
                print(''.join(['!! Echec téléchargement ',intellij_version]))
                print('')
                pass
            if retval == 0 :
                ## Installation de intellij
                print(''.join(['** Installation ',intellij_version]))
                try :
                    subprocess.check_call('sudo mkdir /opt/intellij',shell=True)
                    intellij_path=''.join(['/opt/',intellij_version])
                    tar_cmd = ''.join(['sudo tar -xzf ',intellij_path,' -C /opt/intellij --strip-components 1'])
                    subprocess.check_call(tar_cmd,shell=True)
                    intellij_chown_cmd=''.join([chown_cmd,' /opt/intellij'])
                    subprocess.check_call(intellij_chown_cmd,shell=True)
                    rm_intellij_cmd = ''.join(['sudo rm -f ',intellij_path])
                    subprocess.check_call(rm_intellij_cmd,shell=True)
                except :
                    failled_install.append(intellij_version)
                    print('')
                    print(''.join(['!! Echec installation ',intellij_version]))
                    print('')
                    pass
                make_desktop_entry(user_config=user_config,
                                   app_short_name='intellij',
                                   app_name='IntelliJ',
                                   exec_path='/bin/sh /opt/intellij/bin/idea.sh',
                                   icon_path='/opt/intellij/bin/idea.png')
        print('')
    if 'android-studio' in config['DEV-TOOLS'] :
        ##Télécharger android-studio
        android_studio_link = config['DEV-TOOLS']['android-studio']
        match = re.search('.+\/(android-studio-ide.+\.zip$)',android_studio_link)
        android_studio_version = match.group(1)
        if not android_studio_version :
            print('')
            print ('!! Erreur dans le chemin de téléchargement de android-studio')
            print('')
            failled_install.append(android_studio_version)
            retval = 1
        if retval == 0 :
            android_studio_wget_cmd=' '.join([wget_cmd,android_studio_link])
            print(''.join(['* Téléchargement ',android_studio_version]))
            try :
                subprocess.check_call(android_studio_wget_cmd,shell=True)
            except :
                retval = 1
                failled_install.append(android_studio_version)
                print('')
                print(''.join(['!! Echec téléchargement ',android_studio_version]))
                print('')
                pass
            if retval == 0 :
                ## Installation de android_studio
                print(''.join(['** Installation ',android_studio_version]))
                try :
                    unzip_cmd = ''.join(['sudo unzip -q /opt/',android_studio_version])
                    subprocess.check_call(unzip_cmd,shell=True)
                    android_studio_chown_cmd=''.join([chown_cmd,' /opt/android-studio'])
                    subprocess.check_call(android_studio_chown_cmd,shell=True)
                    rm_android_studio_cmd = ''.join(['sudo rm -f /opt/',android_studio_version])
                    subprocess.check_call(rm_android_studio_cmd,shell=True)
                except :
                    failled_install.append(android_studio_version)
                    print('')
                    print(''.join(['!! Echec installation ',android_studio_version]))
                    print('')
                    pass
                make_desktop_entry(user_config=user_config,
                                   app_short_name='android-studio',
                                   app_name='Android Studio',
                                   exec_path='/bin/sh /opt/android-studio/bin/studio.sh',
                                   icon_path='/opt/android-studio/bin/studio.png')
        print('')
    retval=0

    if'lein' in config['DEV-TOOLS'] :
        ##Télécharger lein
        lein_link = config['DEV-TOOLS']['lein']
        lein_wget_cmd=' '.join([wget_cmd,lein_link])
        print('* Téléchargemlent lein')
        try :
            subprocess.check_call(lein_wget_cmd,shell=True)
        except :
            retval = 1
            failled_install.append('lein')
            print('')
            print('!! Echec téléchargement lein')
            print('')
            pass
        if retval == 0 :
            ## Installation de lein
            print('** Installation lein')
            try :
                subprocess.check_call('sudo mkdir /opt/clojure',shell=True)
                subprocess.check_call('sudo mkdir /opt/clojure/bin',shell=True)
                subprocess.check_call('sudo mv /opt/lein /opt/clojure/bin/lein',shell=True)
                subprocess.check_call('sudo ln -s /opt/clojure/bin/lein /usr/bin/lein',shell=True)
                lein_chown_cmd=''.join([chown_cmd,' /opt/lein'])
                subprocess.check_call(lein_chown_cmd,shell=True)
            except :
                failled_install.append('lein')
                print('')
                print('!! Echec installation lein')
                print('')
                pass
    retval = 0

    if 'omyzsh' in config['DEV-TOOLS'] :
        omyzsh_link =  config['DEV-TOOLS']['omyzsh']
        print('** Installation oh-my-zsh')
        try :
            subprocess.check_call('sudo sh -c \"$(curl -fsSL )\"')
            subprocess.check_call('git clone https://github.com/powerline/fonts.git')
            subprocess.check_call('sudo /bin/sh /opt/fonts/install.sh')
        except :
            failled_install.append('oh-my-zsh')
            print('')
            print('!! Echec Installation lein')
            print('')
    print('')

    return failled_install

def make_desktop_entry(user_config,app_short_name,app_name,exec_path,icon_path):
    retval = 0
    application_desktop_dir = ''.join(['/home/',user_config['BASE']['os_user'],'/.local/share/applications'])
    if not os.path.isdir(application_desktop_dir) :
        mkdir_cmd = ''.join(['sudo mkdir ',application_desktop_dir])
        try :
            subprocess.check_call(mkdir_cmd,shell=True)
        except :
            print('')
            print(''.join(['!! Erreur lors de la création du dektop_enytry ',app_name]))
            print('')
            retval = 1
    if retval == 0 :
        try :
            app_desktop_path = ''.join([application_desktop_dir,'/',app_short_name,'.desktop'])
            desktop_content = """
            [Desktop Entry]
            Encoding=UTF-8
            Name={name}
            Exec={exe}
            Icon={icon}
            Categories=Application;Development;IDE
            Version=1.0
            Type=Application
            Terminal=0
            """.format(name=app_name,exe=exec_path,icon=icon_path)
            with open(app_desktop_path,"a+") as f:
                f.write(desktop_content)
        except :
            print('')
            print(''.join(['!! Erreur lors de la création du dektop_enytry ',app_name]))
            print('')
            retval = 1
    return retval


def main(argv):
    failed_install = None

    ### Initialisation de la lecture des fichier de propriétés
    config = configparser.ConfigParser()
    config.read(APPS_FILE)
    user_config = configparser.ConfigParser()
    user_config.read(USER_FILE)

    # Commandes d'installation
    install_cmd = 'sudo /usr/bin/apt-get -y install'
    chown_cmd = ''.join(['sudo chown -Rf ',user_config['BASE']['os_user'],':',user_config['BASE']['os_user']])
    wget_cmd = 'sudo wget --no-check-certificate --no-cookies'

    #Test validité propriété et utilisateur
    base_tests(config=config,user_config=user_config)
    #Installation sudo et ajout utilisateur au groupe sudo
    sudo_install(config=config,user_config=user_config)

    print('*** Liste des section d\'installation ***')
    print(config.sections())
    print('')

    ### Installation Java
    ## Les jdk spécifié dans le fichier app.properies vont être téléchargés et installés dans /opt
    if 'JAVA' in config.sections() :
        java_install(config=config,wget_cmd=wget_cmd)
        print('')

    ### Installation des dépendances de base
    if 'BASE' in config.sections() :
        base_install(config=config,install_cmd=install_cmd)
        print('')
    ### Installation Python
    ## Python3 ainsi que les dépendances nécéssaires
    if 'PYTHON' in config.sections() :
        python_install(config=config,install_cmd=install_cmd)
        print('')
    ### Installation PostgreSQL
    ## postgres9 et dépendences dev nécéssaires
    if 'POSTGRES' in config.sections():
        postgresql_install(config=config,install_cmd=install_cmd)
        print('')
    ### Installation des outils de développement

    if 'DEV-TOOLS' in config.sections() :
        failed_install = install_dev_tools(config=config,user_config=user_config,wget_cmd=wget_cmd,install_cmd=install_cmd,chown_cmd=chown_cmd)
        print('')

    if 'MEDIA' in config.sections():
        retval = install_media(config=config,install_cmd=install_cmd)
        if retval :
            failed_install.append('media')
        print('')

    if 'MOZILLA' in config.sections():
        retval = install_mozilla()
        if retval :
            failed_install.append('mozzilla')
        print('')

    if failed_install :
        print('**** Installation terminée avec des échecs ****')
        [print(''.join(['*',fail_app])) for fail_app in failed_install]
    else :
        print('**** Installation terminée avec succès ****')

    exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
