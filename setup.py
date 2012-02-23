import os
import re
from distutils.core import Command, setup
from setuptools import find_packages

REQUIREMENTS = [
    'django',
    'django-admin-ext',
    'django-autoload',
    'django-fields',
    'django-class-registry>=0.0.3',
]

TEST_REQUIREMENTS = [
    'mock',
    'django-jenkins',
    'pep8',
    'pyflakes',
]

def do_setup():
    setup(
        name="django-dynamic-rules",
        version="0.3.2",
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
        cmdclass={
            'install_dev': InstallDependencies,
        },
    )


class InstallDependencies(Command):
    """
    Command to install both develop dependencies and test dependencies.

    Not sure why we can't find a built in command to do that already
    in an accessible way.
    """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def get_test_dependencies(self):
        """
        replace all > or < in the dependencies so the system does not
        try to redirect stdin or stdout from/to a file.
        """
        command_line_deps = ' '.join(TEST_REQUIREMENTS)
        return re.sub(re.compile(r'([<>])'), r'\\\1', command_line_deps)

    def run(self):
        os.system("pip install ./")
        os.system("pip install %s" % self.get_test_dependencies())


if __name__ == '__main__':
    do_setup()