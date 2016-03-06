from references import MESSAGES, PHASES


def make_message(type,*args):
    if type == 'error' :
        print(MESSAGES['error'].format(args[0],args[1],args[2]))
    if type == 'phase_title' :
        print(MESSAGES['phase_title'].format(args[0],args[1]))
    if type == 'section_title' :
        print (MESSAGES['section_title'].format(args[0]))
    if type == 'app_lists' :
        [print (MESSAGES['app_lists'].format(app)) for app in args[0]]

