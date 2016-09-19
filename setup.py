"""
motly-manager
------------
motly-manager handles the deployment of static files from github to s3

"""
from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]


setup(
    name='motly-manager',
    version='0.0.1',
    url='http://github.com/cacahootie/motly-manager/',
    license='MIT',
    author='Bradley Alan Smith',
    author_email='brad.alan.smith@gmail.com',
    description='deploying static files from github to s3',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=reqs,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
