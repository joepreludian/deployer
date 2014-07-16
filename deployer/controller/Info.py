from deployer.Utils import run_silent

def check_if_present():

    app_list_result = []
    app_list = ['node',
                'git',
                'npm',
                'bower',
                'gunicorn',
                'supervisord',
                'virtualenv']

    validated = True

    for app_name in app_list:
        success = run_silent(['which', app_name])

        if not success:
            validated = False

        app_list_result.append((app_name, success))

    return validated, app_list_result