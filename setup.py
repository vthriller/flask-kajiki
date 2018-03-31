#!/usr/bin/env python
from setuptools import setup


with open('README.rst') as file:
    readme = file.read()


setup(
    name='Flask-Kajiki',
    version='0.5.1',
    url='http://packages.python.org/Flask-Kajiki',
    license='BSD',
    author='Dag Odenhall',
    author_email='dag.odenhall@gmail.com',
    description='An extension to Flask for easy Kajiki templating.',
    long_description=readme,
    py_modules=['flask_kajiki'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Kajiki>=0.7'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML'
    ]
)
