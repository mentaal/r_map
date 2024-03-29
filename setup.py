"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='r_map',  # Required
    version='0.9.0',  # Required
    description='A data structure for working with register map information',  # Required
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/mentaal/r_map',  # Optional
    # This should be your name or the name of the organization which owns the
    # project.
    author='Gregory Kuhn',  # Optional

    # This should be a valid email address corresponding to the author listed
    # above.
    author_email='gregorykuhn@gmail.com',  # Optional

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],

    keywords='register bitfield registermap',  # Optional
    packages=['r_map'],
    python_requires='>=3.6',

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/mentaal/r_map/issues',
        'Source': 'https://github.com/mentaal/r_map',
    },
)
