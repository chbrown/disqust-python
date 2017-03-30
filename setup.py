from setuptools import setup, find_packages

setup(
    name='disqust',
    version='0.1.0',
    description='Disqus API client',
    long_description=open('README.rst').read(),
    url='http://github.com/chbrown/disqust-python',
    author='Christopher Brown',
    author_email='io@henrian.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)
