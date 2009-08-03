# -*- coding: utf-8 -*-

from paver.easy import *
from paver.setuputils import find_packages, setup


setup(
    name='DjanJinja',
    version='0.5',
    packages=find_packages(exclude=('djanjinja_test', 'djanjinja_test.*')),
    url='http://bitbucket.org/zacharyvoase/djanjinja/',
    
    author='Zachary Voase',
    author_email='zacharyvoase@me.com',
)


@task
def lint(options):
    """Run PyLint on the ``djanjinja`` and ``djanjinja_test`` directories."""
    
    import os
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'djanjinja_test.settings'
    rcfile = path(__file__).abspath().dirname() / 'pylintrc'
    
    run_pylint('djanjinja', rcfile=rcfile)
    run_pylint('djanjinja_test', rcfile=rcfile, disable_msg='C0111')


def run_pylint(directory, **options):
    """Run PyLint on a given directory, with some command-line options."""
    
    from pylint import lint
    
    rcfile = options.pop('rcfile', None)
    if not rcfile:
        if (path(__file__).abspath().dirname() / 'pylintrc').exists():
            rcfile = path(__file__).abspath().dirname() / 'pylintrc'
    if rcfile:
        options['rcfile'] = rcfile
    
    arguments = []
    for option, value in options.items():
        arguments.append('--%s=%s' % (option.replace('_', '-'), value))
    arguments.append(directory)
    
    message = 'pylint ' + ' '.join(
        argument.replace(' ', r'\ ') for argument in arguments)
    
    try:
        dry(message, lint.Run, arguments)
    except SystemExit, exc:
        if exc.args[0] != 0:
            raise BuildFailure('PyLint returned with a non-zero exit code.')
