from distutils.core import setup

packages=['phonostats','phonostats.media']
template_patterns = [
    'templates/*.html',
    'templates/*/*.html',
    'templates/*/*/*.html',
    ]

setup(
    name='django-phonological-statistics',
    version='0.1.20',
    author='Michael McAuliffe',
    author_email='michael.e.mcauliffe@gmail.com',
    url='http://pypi.python.org/pypi/django-phonological-statistics/',
    license='LICENSE.txt',
    description='Django module that allows for querying of a database of phonological lemmas to determine statistics about inputted phonological strings',
    long_description=open('README.md').read(),
    install_requires=['django',
                        'python-BLICK'],
    packages=packages,
    package_data=dict( (package_name, template_patterns)
                   for package_name in packages )
)
