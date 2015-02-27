from fabric.api import cd, env, execute, hide, put, require, roles, run, sudo, task
from fabric.utils import fastprint

import os


## Memcached management
@task
@roles('admin')
def start():    
    """
    Start the webserver on the remote host.
    """
    with hide('stdout', 'running'):
        fastprint("Starting Memcached service..." % env, show_prefix=True)
        sudo('/etc/init.d/memcached start')
        fastprint(" done." % env, end='\n')  


@task
@roles('admin')
def stop():    
    """
    Stop the webserver on the remote host.
    """
    with hide('stdout', 'running'):
        fastprint("Stopping Memcached service..." % env, show_prefix=True)
        sudo('/etc/init.d/memcached stop')
        fastprint(" done." % env, end='\n')  


@task
@roles('admin')
def restart():    
    """
    Restart the webserver on the remote host.
    """
    with hide('stdout', 'running'):
        fastprint("Restarting Memcached service...", show_prefix=True)
        sudo('/etc/init.d/memcached restart')
        fastprint(" done." % env, end='\n')  


@task
@roles('admin')
def upload_conf():
    """
    Upload memcached configuration to the remote host
    """
    require('environment', provided_by=('staging','production'))
    fastprint("Uploading memcached configuration...", show_prefix=True)
    with hide('stdout', 'running'):
        source = os.path.join(env.local_repo_root, "system", 'memcached', 'memcached.conf' % env)
        with cd('/etc'):
            dest = 'memcached.conf'
            put(source, dest, use_sudo=True, mode=0644)
   
    fastprint(" done." % env, end='\n')

