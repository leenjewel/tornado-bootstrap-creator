
import os
import shutil
import hashlib
import stat
from jinja2 import Environment, PackageLoader
from tornado_bootstrap_creator.util import timestamp_to_string
try:
    input = raw_input
except NameError:
    pass

class ArgumentError(Exception):
    pass

class ProjectHasExists(Exception):
    pass

def new_project(args):
    now = timestamp_to_string()
    if not args.package:
        args.package = input('Your project package name:')
    if not args.package:
        raise ArgumentError('Project need package name')
    project_path = os.path.join(args.prefix, args.package)
    if os.path.exists(project_path) and args.force:
        shutil.rmtree(project_path)
    if os.path.exists(project_path):
        raise ProjectHasExists('%s has exists' % project_path)
    package_path = os.path.join(project_path, args.package)
    os.makedirs(package_path)
    with open(os.path.join(package_path, '__init__.py'), 'w') as fp:
        fp.write("'''%s\n\n%s\n\nby %s at %s\n'''" %(args.name, args.descript, args.author, now))
    
    file_dir = os.path.split(__file__)[0]
    resources_path = os.path.join(package_path, 'resources')
    os.makedirs(resources_path)
    shutil.copytree(os.path.join(file_dir, 'resources', 'css'), os.path.join(resources_path, 'css'))
    shutil.copytree(os.path.join(file_dir, 'resources', 'js'), os.path.join(resources_path, 'js'))
    shutil.copytree(os.path.join(file_dir, 'resources', 'fonts'), os.path.join(resources_path, 'fonts'))
    shutil.copytree(os.path.join(file_dir, 'resources', 'favicon'), os.path.join(resources_path, 'favicon'))
    if args.logo and os.path.isfile(args.logo):
        shutil.copy(args.logo, os.path.join(resources_path, 'css', 'images', 'logo.png'))

    templates_path = os.path.join(package_path, 'templates')
    os.makedirs(os.path.join(templates_path, 'ui'))
    os.makedirs(os.path.join(templates_path, 'layouts'))
    shutil.copy(os.path.join(file_dir, 'resources', 'templates', 'login.html'), os.path.join(templates_path, 'login.html'))

    locales_path = os.path.join(package_path, 'locales')
    os.makedirs(locales_path)
    locales = {
        args.name: args.name,
        args.descript: args.descript,
        'menu index': 'menu index',
    }

    routes = {}
    handlers = {}
    menu = {}
    if args.routes:
        for route in args.routes.split(';'):
            if not route:
                continue
            if ':' not in route or '.' not in route:
                continue
            r, h = route.split(':')
            c, n = h.split('.')
            routes[r] = c
            handlers[c] = n
            menu[r] = n
            locales['menu '+n] = 'menu '+n
            locales['panel '+n] = 'panel '+n

    admin_password = hashlib.md5()
    admin_password.update(args.admin_password.encode('utf-8'))

    secret_md5 = hashlib.md5()
    secret_md5.update(args.package.encode('utf-8'))

    if not args.url:
        args.url = 'https://github.com/%s/%s.git' %(args.author, args.package)

    context = {
        'package': args.package,
        'secret': secret_md5.hexdigest(),
        'project_name': args.name,
        'project_decsription': args.descript,
        'project_license': args.license,
        'project_url': args.url,
        'project_author': args.author,
        'project_author_email': args.email,
        'project_command': args.package.replace('_', '-'),
        'admin_user': args.admin_user,
        'admin_password': admin_password.hexdigest(),
        'routes': routes,
        'handlers': handlers,
        'menu': menu,
        'port': args.port,
    }

    with open(os.path.join(locales_path, 'en_US.csv'), 'w') as fp:
        fp.write('\n'.join(['"'+k+'","'+v+'"' for k, v in locales.items()]))
    with open(os.path.join(locales_path, 'zh_CN.csv'), 'w') as fp:
        fp.write('\n'.join(['"'+k+'","'+v+'"' for k, v in locales.items()]))

    env = Environment(loader = PackageLoader(__package__, 'resources'))
    with open(os.path.join(package_path, 'routes.py'), 'w') as fp:
        fp.write(env.get_template('project/routes.py').render(**context))
    with open(os.path.join(package_path, 'handler.py'), 'w') as fp:
        fp.write(env.get_template('project/handler.py').render(**context))
    with open(os.path.join(package_path, 'web.py'), 'w') as fp:
        fp.write(env.get_template('project/web.py').render(**context))
    with open(os.path.join(package_path, 'uimodules.py'), 'w') as fp:
        fp.write(env.get_template('project/uimodules.py').render(**context))
    with open(os.path.join(templates_path, 'layouts', 'default.html'), 'w') as fp:
        fp.write(env.get_template('templates/layouts/default.html').render(**context).encode('utf-8'))
    with open(os.path.join(templates_path, 'layouts', 'login.html'), 'w') as fp:
        fp.write(env.get_template('templates/layouts/login.html').render(**context))
    with open(os.path.join(templates_path, 'index.html'), 'w') as fp:
        fp.write(env.get_template('templates/index.html').render(**context))
    with open(os.path.join(templates_path, 'ui', 'menu.html'), 'w') as fp:
        fp.write(env.get_template('templates/ui/menu.html').render(**context))
    for handler, name in handlers.items():
        with open(os.path.join(templates_path, name+'.html'), 'w') as fp:
            fp.write(env.get_template('templates/panel.html').render(name = name))
    command_py = os.path.join(project_path, context['project_command']+'.py')
    with open(command_py, 'w') as fp:
        fp.write(env.get_template('project/command.py').render(**context))
    command_st = os.stat(command_py)
    os.chmod(command_py, command_st.st_mode | stat.S_IEXEC)
    setup_py = os.path.join(project_path, 'setup.py')
    with open(setup_py, 'w') as fp:
        fp.write(env.get_template('project/setup.py').render(**context))
    setup_st = os.stat(setup_py)
    os.chmod(setup_py, setup_st.st_mode | stat.S_IEXEC)

def run(args):
    method_name = args.command[0]
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    method(args)