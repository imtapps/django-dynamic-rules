from distutils.core import setup
from setuptools import find_packages

TEST_REQUIREMENTS = [
]

setup(
    name="django-dynamic-rules",
    version="0.6.0",
    author="IMT Computer Services",
    author_email="webadmin@imtapps.com",
    description="Allows you to create dynamic rules related to a particular model",
    long_description=open('README.txt', 'r').read(),
    url="https://github.com/imtapps/django-dynamic-rules",
    packages=find_packages(exclude=["example"]),
    install_requires=file('requirements/dist.txt').read().split('\n'),
    zip_safe=False,
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    dependency_links = (
        'https://bitbucket.org/twanschik/django-autoload/get/tip.tar.gz#egg=django-autoload',
    ),
)
