
import os
import sys

from setuptools import Extension, setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
from Cython.Build import cythonize


def get_long_description():
    """Read the contents of README.md, INSTALL.md and CHANGES.md files."""
    from os import path

    repo_dir = path.abspath(path.dirname(__file__))
    markdown = []
    for filename in ["README.md", "INSTALL.md", "CHANGES.md"]:
        with open(path.join(repo_dir, filename), encoding="utf-8") as markdown_file:
            markdown.append(markdown_file.read())
    return "\n\n----\n\n".join(markdown)


class Test(TestCommand):
    def run_tests(self):
        import pytest
        errno = pytest.main(['tests/'])
        sys.exit(errno)


extra_compile_args = ["/O2" if os.name == "nt" else "-O3"]
define_macros = []

# comment out line to compile with type check assertions
# verify value at runtime with bunnybackend.types.COMPILED_WITH_ASSERTIONS
define_macros.append(('CYTHON_WITHOUT_ASSERTIONS', None))

extension = Extension("bunnybackend.types", ["bunnybackend/types.pyx"],
                      extra_compile_args=extra_compile_args,
                      define_macros=define_macros)

setup(
    name="bunnybackend",
    ext_modules=cythonize([extension], language_level=3, force=True),
    version="0.0.1",
    author="Joes Lie",
    author_email="liej6799@protonmail.ch",
    description="bunnytest backend service",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license="XFree86",
    url="https://github.com/liej6799/bunny-test",
    packages=find_packages(exclude=['tests*']),
    cmdclass={'test': Test},
    python_requires='>=3.8',
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: AsyncIO",
    ],
    tests_require=["pytest"],
    install_requires=[
        "requests>=2.18.4",
        "websockets>=15.0.1",
        "pyyaml",
        "aiohttp>=3.11.13",
        "aiofile>=2.0.0",
        "yapic.json",
        'uvloop ; platform_system!="Windows"',
        "numpy==1.24.4",
        "asyncpg>=0.30.0",
        "redis"
    ]
)
