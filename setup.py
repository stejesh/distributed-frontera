from setuptools import setup, find_packages

import versioneer

setup(
    name='distributed-frontera',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(exclude=('tests', 'tests.*', 'examples', 'examples.*')),
    url='https://github.com/scrapinghub/distributed-frontera',
    description='Distributed version of Frontera, flexible frontier for web crawlers',
    author='Scrapy developers',
    maintainer='Alexander Sibiryakov',
    maintainer_email='sibiryakov@scrapinghub.com',
    license='BSD',
    include_package_data=True,
    zip_safe=False,
    keywords=['crawler', 'frontier', 'scrapy', 'web', 'requests', 'frontera', 'distributed'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'happybase',
        'kafka-python',
        'msgpack-python',
        'python-snappy',
        'frontera'
    ],
    extras_require={},
    tests_require=[
        'pytest>=2.6.4'
    ]
)
