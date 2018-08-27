import os
import sys

import shapeshifter

from setuptools import setup, find_packages


if sys.argv[-1] == "publish":
    # Thanks to crispy-forms for this
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to tag the version now:")
    print(
        "  git tag -a %s -m 'version %s'"
        % (shapeshifter.__version__, shapeshifter.__version__)
    )
    print("  git push --tags")
    sys.exit()

setup(
    name="django-shapeshifter",
    version=shapeshifter.__version__,
    description="Class-based views for simultaneously handling multiple forms in Django",
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: User Interfaces"
    ],
    keywords=["forms", "django", "multi", "cbv", "class-based views"],
    author="Kenneth Love",
    author_email="kennethlove@gmail.com",
    url="https://github.com/kennethlove/django-shapeshifter",
    license="Apache 2.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
