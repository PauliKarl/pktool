from setuptools import setup,find_packages

setup(name='Atool',
      version='0.1',
      description='paulikarl tools',
      classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
      url='https://www.python.org/',
      author='paulikarl',
      author_email='paulikarlcn@gmail.com',
      license='pd',
      packages=find_packages(exclude=["build"]),
      zip_safe=True
     )