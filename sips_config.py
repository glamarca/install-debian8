DEV_PATH = '~/DEV'
AS_PATH = '~/AS'

SIPS_CONFIG = {
    'GLOBAL': {
        'ucl_dev_path' : ''.join([DEV_PATH,'/UCL']),
        'ucl_java_path' : ''.join([DEV_PATH,'/UCL/Java']),
        'ucl_python_path' : ''.join([DEV_PATH,'/UCL/Python'])
    },
    'EPC': {
        'epc': {
            'repo-url': 'git@github.com:uclouvain/epc.git',
        },
        "epcv2": {
            'repo-url': 'git@github.com:uclouvain/epc-v2.git',
        },
        "epc-batch": {
            'repo-url': 'git@github.com:uclouvain/epc-batch.git',
        }
    },
    "OSIS": {
        "osis": {
            'repo-url': 'git@github.com:uclouvain/osis.git',
        },
        "osis-portal": {
            'repo-url': 'git@github.com:uclouvain/osis-portal.git',
        },
        "osis-documentation": {
            'repo-url': 'git@github.com:uclouvain/osis-louvain-documentation.git',
        },
        "osis-legacy": {
            'repo-url': 'git@github.com:uclouvain/osis-legacy-sync.git',
        }

    },
    "CARTE": {

    },
    "ALUMNI": {

    }
}
