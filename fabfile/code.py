from fabric.api import cd, env, execute, hide, lcd, put, require, roles, run, sudo, task
from fabric.utils import abort, fastprint, puts
from fabric.contrib import files, console
from fabric.contrib.project import rsync_project

from webserver import touch_WSGI_script
from provision import setup_instance_user

import os

## Application code management
@task
@roles('web')
def make_website_skeleton():
    """
    Create a skeleton directory tree for the new web app.

    Include setup of suitable filesystem permissions.
    """
    require('web_root', 'app_domain', 'om_user', 
                provided_by=('staging', 'production'))
    puts("Setting up initial filesystem layout for this OpenOrdini instance..." % env)
    with hide('commands'):
        with cd(env.web_root):
            if not files.exists(env.app_domain):
                abort("Missing directory '%(app_domain)s'. Invoke 'code.make_website_skeleton' after 'provision.setup_instance_user'" % env)

##                confirmation_msg = "Directory `%(app_domain)s' already exists on the remote machine, but we need to recreate it: do you want to delete the old copy ?" % env                                  
##                if not console.confirm(confirmation_msg):
##                    abort("Deployment aborted by the user.")
##                else:
##                    sudo('rm -rf %(app_domain)s' % env)
##                    # re-create a SSH account for ``OM_USER``
##                    execute(setup_instance_user) # don't do it, it's already done in the initial deploy
            ## create filesystem skeleton
            sudo('chmod 2750 %(app_domain)s' % env)
            sudo('mkdir -p %(app_domain)s/backup' % env)
            sudo('mkdir -p %(app_domain)s/private/log' % env)
            sudo('mkdir -p %(app_domain)s/private/%(project)s' % env)
            sudo('mkdir -p %(app_domain)s/private/venv' % env)
            sudo('mkdir -p %(app_domain)s/private/apache' % env)
            sudo('mkdir -p %(app_domain)s/private/system' % env)
            sudo('mkdir -p %(app_domain)s/public/media' % env)
            sudo('mkdir -p %(app_domain)s/public/static' % env)
            ## setup permissions
            # create empty logfile with group-writing permission used by PermissionKeepingLogFileRotator
            sudo('touch %(app_domain)s/private/log/logfile' % env)
            sudo('chmod g+w %(app_domain)s/private/log/logfile' % env)           
            sudo('touch %(app_domain)s/private/log/webapp.log' % env)
            sudo('chmod g+w %(app_domain)s/private/log/webapp.log' % env)           

            # webserver user needs read access to (nearly) every file within its domain
            sudo('chown -R %(om_user)s:www-data %(app_domain)s' % env)           
            # webserver user needs RW access to the directory holding files uploaded by clients
            sudo('chmod g+w %(app_domain)s/public/media' % env)
    puts("Done setting up initial filesytem layout." % env)


@task
@roles('om')
def update_project():
    """
    Update Django project's files  on the remote host.
    
    It works by syncing contents of the project dir on the local machine
    with the corresponding one on the remote staging/production server(s).
    
    Therefore, to deploy a given version of the Django project, all you need 
    to do is to checkout the chosen version on the local machine before starting
    the deploy process.
    
    Notice that you can prevent some files from being synced to the server via the
    ``RSYNC_EXCLUDE`` config option.
    """
    require('project_root', provided_by=('staging', 'production'))
    if env.environment == 'production':
        if not console.confirm('Are you sure you want to deploy to the production server(s)?',
                               default=False):
            abort('Production deployment aborted.')
    with hide('commands'):         
        fastprint("Updating Django project files..." % env, show_prefix=True)
        # defaults rsync options:
        # -pthrvz
        # -p preserve permissions
        # -t preserve times
        # -h output numbers in a human-readable format
        # -r recurse into directories
        # -v increase verbosity
        # -z compress file data during the transfer
        extra_opts = '--omit-dir-times'
        rsync_project(
            remote_dir = env.project_root,
            local_dir = env.local_project_root + os.path.sep,
            exclude=env.rsync_exclude,
            delete=True,
            extra_opts=extra_opts,
        )
        fastprint(" done." % env, end='\n')
        fastprint("Updating settings & URLconfs modules..." % env, show_prefix=True)
        with lcd(os.path.join(env.local_project_root, env.project)):
            with cd(os.path.join(env.project_root, env.project)):
                # update Django settings module
                settings_file = 'settings_%(environment)s.py' % env
                put(settings_file, settings_file, mode=0644)
                # update Django main URLconf module
                urls_file = 'urls_%(environment)s.py' % env        
                put(urls_file, urls_file, mode=0644)
        fastprint(" done." % env, end='\n')
##        fastprint("Updating WSGI script..." % env, show_prefix=True)
##        with lcd(os.path.join(env.local_repo_root, env.project)):
##            with cd(os.path.join(env.domain_root, 'private')):
##                source = '%(environment)s.wsgi' % env
##                dest = 'django.wsgi'
##                put(source, dest, mode=0644)
        fastprint(" done." % env, end='\n')
    # trigger code reloading
    touch_WSGI_script()
