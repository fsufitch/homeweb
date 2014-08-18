from setuptools import setup, Extension, find_packages

setup(name='fsufitch_homeweb',
      version='0.1',
      author='Filip Sufitchi',
      author_email="fsufitchi@gmail.com",
      description="Overwrought personal webpage",
      url="http://opensourcenerd.com",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      entry_points = {'console_scripts':
                      ['homeweb=homeweb.server:main_service',
                       'homeweb_cli=homeweb.server:main_cli']
                      },
      install_requires=[],
      )
