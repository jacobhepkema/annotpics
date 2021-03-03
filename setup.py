from setuptools import setup
from setuptools import find_packages

import sys

def setup_package():
  install_requires = ['numpy', 'pandas', 'Pillow', 'click']
  metadata = dict(
      name = 'annotpics',
      version = '0.0.1',
      description = 'annotpics: utilities for picture annotation',
      url = 'https://github.com/jacobhepkema/annotpics',
      author = 'Jacob Hepkema',
      author_email = 'jacob.hepkema@sanger.ac.uk',
      license = 'MIT License',
      packages = find_packages(),
      install_requires = install_requires
    )

  setup(**metadata)

if __name__ == '__main__':
  if sys.version_info < (2,7):
    sys.exit('Sorry, Python < 2.7 is not supported')
    
  setup_package()
