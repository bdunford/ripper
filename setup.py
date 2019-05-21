from setuptools import setup

setup(name='ripper',
    version='1.1',
    description='Utility for copying a website',
    url='http://github.com/bdunford/ripper',
    author='Frustrated User',
    author_email='fu@gmail.com',
    license='MIT',
    packages=['ripper'],
    zip_safe=False,
    scripts=['bin/ripper'],
    install_requires=[
        'requests',
    ]
)
#http://www.scotttorborg.com/python-packaging/
