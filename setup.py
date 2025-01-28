from setuptools import setup, find_packages

setup(
    name='kom-python-core',
    version='0.1.14',
    description='Core centralized packages for KominskyOrg Python utilities.',
    author='Jared Kominsky',
    author_email='kominskyjared@gmail.com',
    url='https://github.com/kominskyorg/kom_python_core',
    packages=find_packages(include=['kom_python_core', 'kom_python_core.*']),
    install_requires=[
        'requests',
        'python-json-logger',
    ],
    extras_require={
        'dev': [
            'ruff',
            'pytest',
            'pytest-cov',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    include_package_data=True,
    zip_safe=False,
)