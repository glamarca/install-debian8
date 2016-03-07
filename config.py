USER = {
    'BASE': {
        # Obligatoire
        'os_user': '',
    },
    # Si utilisé , la configuration globale de git sera adaptée
    # 'GIT' : {
    #     'name' : '',
    #     'username' : '',
    #     'email' : '',
    # },
}

APPS = {
    'BASE': {
        'vim': 'vim',
        'gparted': 'gparted',
        'git': 'git',
        'svn': 'subversion',
        'unrar': 'unrar-free',
        'gettext': 'gettext',
        'build': 'build-essential',
        'jpeg': 'libjpeg62-turbo',
        'jpeg-dev': 'libjpeg62-turbo-dev',
        'png': 'libpng12-0',
        'png-dev': 'libpng12-dev',
        'maven': 'maven',
        'zsh': 'zsh',
        'ttf-ancient-fonts': 'ttf-ancient-fonts',
        'gvfs-bin': 'gvfs-bin',
        'openssl': 'openssl',
        'openconnect':'openconnect',
        'libpq-dev' : 'libpq-dev',
        'firmware' : 'firmware-linux-nonfree',
    },
    'DEBIAN_REPO': {
        'stable': 'deb http://httpredir.debian.org/debian jessie main contrib non-free',
        'jessie-update': 'deb http://httpredir.debian.org/debian jessie-updates main contrib non-free',
        'update': 'deb http://security.debian.org/ jessie/updates main contrib non-free',
        'backports': 'deb http://http.debian.net/debian jessie-backports main',
        'testing': 'deb http://httpredir.debian.org/debian testing main contrib non-free',
        'google-chrome': 'deb http://dl.google.com/linux/chrome/deb/ stable main',
    },
    'PACKAGE_KEY': {
        'google': 'https://dl.google.com/linux/linux_signing_key.pub',
    },
    'JAVA': {
        'java7': 'http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-linux-x64.tar.gz',
        'java8': 'http://download.oracle.com/otn-pub/java/jdk/8u73-b02/jdk-8u73-linux-x64.tar.gz',
    },
    'PYTHON': {
        'python3': 'python3-all',
        'python3-dev': 'python3-all-dev',
        'pip3': 'python3-pip',
    },
    'POSTGRES': {
        'postgres': 'postgresql',
        'postgres-client': 'postgresql-client',
        'postgres-dev' : 'postgresql-server-dev-all',
    },
    'COUCHBASE': {
        'couchbase':'http://packages.couchbase.com/releases/4.0.0/couchbase-server-community_4.0.0-debian7_amd64.deb',
    },
    'DEV-TOOLS': {
        'netbeans': 'http://download.netbeans.org/netbeans/8.1/final/bundles/netbeans-8.1-javaee-linux.sh',
        'pycharm': 'https://download.jetbrains.com/python/pycharm-community-5.0.4.tar.gz',

        # IntelliJ
        # Comunity 15
        'intellij': 'https://download.jetbrains.com/idea/ideaIC-15.0.4.tar.gz',
        # Ultimate 14
        # 'intellij':'https://download.jetbrains.com/idea/ideaIU-14.1.6.tar.gz',
        # Utltimate 13
        # 'intellij':'http://download.jetbrains.com/idea/ideaIU-13.1.6.tar.gz',

        'android-studio': 'https://dl.google.com/dl/android/studio/ide-zips/1.5.1.0/android-studio-ide-141.2456560-linux.zip',
        'atom': 'https://github.com/atom/atom/releases/download/v1.5.3/atom-amd64.deb',
        'sql-developer': 'sqldeveloper-4.1.3.20.78-no-jre.zip',
        'visual-paradigm': 'http://www.visual-paradigm.com/downloads/vp/Visual_Paradigm_Linux64.sh',
        'lein': 'https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein',
        'ohmyzsh': 'https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh',
    },
    'MEDIA': {
        'vlc': 'vlc',
        'goofle-chrome': 'google-chrome-stable',
        'gimp' : 'gimp',
        'flash-player' : 'flashplugin-nonfree',
    },
    'MOZILLA': {
        'firefox': 'firefox',
        'thunderbird': 'thunderbird',
    },
    'DRIVERS': {
        # 'intel-graphic':'xserver-xorg-video-intel'
        # 'intel-wifi':'firmware-iwlwifi'
        # 'nvidia-graphic' : 'nvidia-kernel-dkms',
        # 'ati-graphic' : 'libgl1-mesa-dri xserver-xorg-video-ati',
    },

}
