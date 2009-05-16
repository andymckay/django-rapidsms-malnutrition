from setuptools import setup, find_packages

setup(
    name='django-rapidsms-baseui',
    version=__import__('malnutrition').__version__,
    description='Base models for rapidsms that can be re-used, not a django app.',
    long_description=open('README.rst').read(),
    author='Andy McKay',
    author_email='andy@clearwind.ca',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
