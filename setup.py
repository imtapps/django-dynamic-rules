from setuptools import setup

REQUIREMENTS = [
    'django',
    'django-admin-ext',
    'django-autoload',
    'django-fields',
]

TEST_REQUIREMENTS = [
    'mock',
]

setup(
    name="dynamic_rules",
    version='0.0.1',
    author="Author Name",
    author_email="author_email",
    description="Allows you to create dynamic rules related to a particular model",
    long_description=open('README.txt', 'r').read(),
    url="https://github.com/imtapps/django-dynamic-rules",
    packages=("dynamic_rules",),
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
)
