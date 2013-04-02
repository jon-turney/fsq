from distutils.core import setup

setup(
    name='fsq',
    version='0.1.0',
    author='Matthew Story',
    author_email='matt.story@axial.net',
    packages=['fsq', 'fsq.tests'],
    scripts=['bin/mkfsqueue','bin/fsq.py','bin/fsq'],
    data_files=[('/usr/share/man/man1', ['fsq.1',
                                         'fsq-down.1', 
                                         'fsq-enqueue.1',
                                         'fsq-scan.1',
                                         'fsq-up.1',
                                         'mkfsqueue.1',
                                         'mkfsqueue.1']),
                ('/usr/share/man/man7', ['fsq.7']) ],
    url='https://github.com/axialmarket/fsq',
    license='3-BSD',
    description='File System Queue',
    long_description=open('README.md').read(),
    install_requires='',
)

