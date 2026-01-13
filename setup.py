import json
from setuptools import setup

with open('package.json') as f:
    package = json.load(f)

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

package_name = package['name'].replace(' ', '_').replace('-', '_')

setup(
    name=package_name,
    version=package['version'],
    author=package['author'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pip-install-python/dash-mui-charts',
    project_urls={
        'Bug Reports': 'https://github.com/pip-install-python/dash-mui-charts/issues',
        'Source': 'https://github.com/pip-install-python/dash-mui-charts',
        'Documentation': 'https://github.com/pip-install-python/dash-mui-charts#readme',
    },
    install_requires=['dash>=3.0.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Dash',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    keywords='dash plotly charts mui material-ui visualization',
    python_requires='>=3.8',
)