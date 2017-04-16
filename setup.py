"""
Flask-Wizard
-----------------

Easy Bot development Framework for Flask
"""

from setuptools import setup 


setup(
    name='Flask-Wizard',
    version='0.0.1',
    url='https://github.com/ozzai/flask-wizard',
    license='Apache 2.0',
    author='Akshay Kulkarni',
    author_email='akshay@ozz.ai',
    description='Rapid and easy bot development in Python',
    long_description=__doc__,
    packages=['flask_wizard'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'rasa_nlu',
        'spacy',
        'scikit-learn'
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
    ]
)