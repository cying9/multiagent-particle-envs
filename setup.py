from setuptools import setup, find_packages

setup(name='multiagent',
      version='0.0.1',
      description='Multi-Agent Goal-Driven Communication Environment',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['gym', 'numpy-stl']
)
