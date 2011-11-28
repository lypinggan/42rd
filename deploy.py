# UWSGI configuration

#import uwsgi
#import production_settings

from iapp import create_app

app = create_app()
#uwsgi.applications = {"/":application}








