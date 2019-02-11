from setuptools import setup, find_packages

#todo : create a new environment with pip requirements
setup(name='GroundZero',
      version='1.0',
      description='README.md',
      author='Raghava,Varun',
      packages=['kenfin'],
      install_requires=[
                     'selenium==3.141.0',
                     'kiteconnect==3.7.6',
                     'flask==1.0.2', 'schedule=0.6.0','sklearn=0.20.2']

      )
