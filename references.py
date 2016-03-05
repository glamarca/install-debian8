# Commandes d'installation
import os

install_cmd = 'sudo /usr/bin/apt-get -y install {}'
chown_cmd = 'sudo chown -Rf {}:{} {}'
wget_cmd = 'sudo wget --no-check-certificate --no-cookies'
wget_app_cmd = ''.join([wget_cmd,' {}'])
execute_as_user = 'su -c {} -s /bin/sh {}'
add_user_to_grp = 'sudo usermod -a -G {} {}'
oracle_jdk_wget_cmd = ''.join([wget_cmd,' --header "Cookie: oraclelicense=accept-securebackup-cookie" '])
add_repo_cmd='echo \'\n\n###debian {}\n{}\n\' >> /etc/apt/sources.list'


APPS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apps.properties")

# Fichier de configuration de l'utilisateur
USER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user.properties")


# Dossier contenant les outils à installer
# Par défaut , dossier tools à la racine
TOOLS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")


PHASES = {
    'install' : {
        'fct' : 'l\'installation',
        'title' : 'Installation',
    },
    'download' : {
        'fct' : 'le téléchargement',
        'title' : 'Téléchargement'
    }
}


MESSAGES = {
    'error' : '\n!!!! Erreur pendant {} de {} !!!!\n',
    'phase_title' : '\n*** {} de {} ***\n',
    'section_title' : '\n\n\n**** [ {} ] ****\n',
    'app_lists' : '-- {} --\n',
}
