"""
Flask-Wizard
-----------------

Easy Bot development Framework for Flask
"""

from setuptools import setup 


setup(
    name='Flask-Wizard',
    version='0.5.13',
    url='https://github.com/ozzai/flask-wizard',
    license='Apache 2.0',
    author='Akshay Kulkarni',
    author_email='akshay@ozz.ai',
    description='Rapid and easy chatbot development in Python for multiple channels',
    long_description=__doc__,
    packages=['flask_wizard_cli','flask_wizard'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'future',
        'jsonschema',
        'wget',
        'requests',
        'PyJWT',
        'slackclient',
        'telepot',
        'redis',
        'Flask-PyMongo',
        'PyMongo'
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Framework :: Flask',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points = {
        'console_scripts':['wiz=flask_wizard_cli.command_line:main']
    }
)
