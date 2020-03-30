"""
Flask-SQLAlchemy-Helpers
-------------
"""

from setuptools import setup


setup(
    name='Flask-SQLAlchemy-Helpers',
    version='1.0',
    url='https://github.com/tonykamillo/Flask-SQLAchemy-Helpers',
    license='BSD',
    author='Tony Kamillo',
    author_email='tonykamillo@gmail.com',
    description='Helpers classes and functions to make work with SQLAlchemy and Flask easier and less repetitive (DRY).',
    # long_description=__doc__,
    py_modules=['flask_sqlalchemy_helpers'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'SQLAlchemy',
        'Flask-SQLAlchemy',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',        
    ]
)