from fabric.contrib.files import append, exists, sed
from fabric.api import env, run,settings, local, sudo
#from fabric import Connection
import random
import os

REPO_URL = 'https://github.com/Ro-Goncalves/Superlist.git'

env.key_filename = 'tddstudy.pem'    

def deploy(user):
    site_folder = f'/home/{user}/sites/{env.host}'   
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder, user)
    _get_latest_source(source_folder, user)
    _update_settings(source_folder, env.host, user)
    _update_virtualenv(source_folder, user)
    _update_static_files(source_folder, user)
    _update_database(source_folder, user)
    
def _create_directory_structure_if_necessary(site_folder, user):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        sudo(f'mkdir -p {site_folder}/{subfolder}', user=user)
        
def _get_latest_source(source_folder, user):    
    if exists(source_folder + '/.git'):
        sudo(f'cd {source_folder} && git fetch', user=user)
    else:
        sudo(f'git clone {REPO_URL} {source_folder}', user=user)
    #current_commit = local("git log -n 1 --pretty=format:'%H'", capture=True)
    #sudo(f'cd {source_folder} && git reset --hard {current_commit}', user=user)
    
def _update_settings(source_folder, site_name, user):
    #with settings(user=user):        
    settings_path = source_folder + '/superlist/settings.py'
    
    sed(settings_path, "DEBUG = True", "DEBUG = False", use_sudo=True)
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        f'ALLOWED_HOSTS = ["{site_name}"]', use_sudo=True)
    secret_key_file = source_folder + '/superlist/secret_key.py'
    if not exists(secret_key_file):
        chars = 'ntstlj-77fd6wy)nliy$8ysz_3t$54(b_w5e9fi%$8z!04v+f='
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"', use_sudo=True)
    append(settings_path, '\nfrom .secret_key import SECRET_KEY', use_sudo=True)
    
def _update_virtualenv(source_folder, user):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        sudo(f'python3.6 -m venv {virtualenv_folder}',user=user)
    sudo(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt',
          user=user)
    
def _update_static_files(source_folder, user):
    sudo(f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput', user=user)
    
def _update_database(source_folder, user):
    sudo(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput',user=user
    )