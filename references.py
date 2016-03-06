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
clear_list_repo_file=' > /etc/apt/sources.list'
add_package_key='wget -q -O - {} | sudo apt-key add -'
install_testing_cmd='sudo /usr/bin/apt-get install -y -t testing {}'
install_backports_cmd='sudo /usr/bin/apt-get install -y -t jessie-backports {}'
dpkg_install='sudo dpkg -i {}'
picking_prefs="""
Package: *
Pin: release a=jessie-backports
Pin-Priority: -10

Package: *
Pin: release a=testing
Pin-Priority: -10
"""

desktop_entry="""
#!/usr/bin/env xdg-open
[Desktop Entry]
Encoding=UTF-8
Name={name}
Exec={exe}
Icon={icon}
Categories=Application;Development;IDE
Version=1.0
Type=Application
Terminal=0
"""
add_pinning_cmd='echo \'{}\' >> /etc/apt/preferences.d/pinning'.format(picking_prefs)

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
    'error' : '\n!!!! Erreur pendant {} de {} !!!!\nErreur = {}',
    'phase_title' : '\n*** {} de {} ***\n',
    'section_title' : '\n\n\n**** [ {} ] ****\n',
    'app_lists' : '-- {} --\n',
}
