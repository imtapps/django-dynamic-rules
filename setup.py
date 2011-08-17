from setuptools import setup, find_packages

REQUIREMENTS = [
    'django',
    'django-admin-ext',
    'django-autoload',
    'django-fields',
]

TEST_REQUIREMENTS = [
    'mock',
]

from dynamic_rules import VERSION

setup(
    name="django-dynamic-rules",
    version=VERSION,
    author="Matthew J. Morrison & Aaron Madison",
    author_email="mattjmorrison@mattjmorrison.com",
    description="Allows you to create dynamic rules related to a particular model",
    long_description=open('README.txt', 'r').read(),
    url="https://github.com/imtapps/django-dynamic-rules",
    packages=find_packages(exclude=["example"]),
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite='runtests.runtests',
    zip_safe=False,
    classifiers = [
        "Development Status :: 3 - Alpha",
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
    )
)
