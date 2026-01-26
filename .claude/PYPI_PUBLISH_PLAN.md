# PyPI Publishing Plan for dash-mui-charts

This document outlines the steps to build and publish `dash-mui-charts` to PyPI using twine.

---

## Pre-Publication Checklist

### 1. Version Verification

Current version in `package.json`: **0.0.5**

Before publishing, ensure version is updated appropriately:
- Patch (0.0.x): Bug fixes
- Minor (0.x.0): New features, backward compatible
- Major (x.0.0): Breaking changes

```bash
# Check current version
grep '"version"' package.json
```

### v0.0.5 Release Notes

New features in this release:
- **LineChart Reference Lines**: Full `ChartsReferenceLine` API support
- **LineChart Brush Selection** (Pro): Range selection with `'default'` or `'values'` overlay
- **LineChart Axis Highlight**: Configurable hover highlighting
- **Type Enhancement**: `referenceLines.y` now accepts `string | number`
- **New Demo Pages**: `/linechart-brush`, `/linechart-referencelines`

### 2. Required Files Check

| File | Status | Purpose |
|------|--------|---------|
| `setup.py` | Required | Package configuration |
| `MANIFEST.in` | Required | Non-Python file inclusion |
| `README.md` | Required | PyPI project description |
| `LICENSE` | Required | License file |
| `CHANGELOG.md` | Recommended | Version history |

### 3. Build Verification

```bash
# Ensure components are built
npm run build

# Verify generated files exist
ls -la dash_mui_charts/*.py
ls -la dash_mui_charts/*.js
```

---

## Setup for PyPI Publishing

### 1. Install Build Tools

```bash
pip install --upgrade pip
pip install --upgrade build twine
```

### 2. Configure PyPI Credentials

Create or update `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_API_TOKEN_HERE

[testpypi]
username = __token__
password = pypi-YOUR_TEST_API_TOKEN_HERE
```

**Security Note:** Use API tokens instead of username/password. Generate tokens at:
- PyPI: https://pypi.org/manage/account/token/
- TestPyPI: https://test.pypi.org/manage/account/token/

---

## Update setup.py for PyPI

The current `setup.py` needs enhancements for PyPI:

```python
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
    author_email='your-email@example.com',  # Add email
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
```

---

## Update MANIFEST.in

Ensure all necessary files are included:

```
include dash_mui_charts/*.js
include dash_mui_charts/*.js.map
include dash_mui_charts/package-info.json
include dash_mui_charts/metadata.json
include README.md
include LICENSE
include CHANGELOG.md
```

---

## Build Process

### Step 1: Clean Previous Builds

```bash
rm -rf build/ dist/ *.egg-info/
```

### Step 2: Build Source Distribution and Wheel

```bash
python -m build
```

This creates:
- `dist/dash_mui_charts-0.0.5.tar.gz` (source distribution)
- `dist/dash_mui_charts-0.0.5-py3-none-any.whl` (wheel)

### Step 3: Verify Package Contents

```bash
# Check tarball contents
tar tzf dist/dash_mui_charts-0.0.5.tar.gz | head -30

# Check wheel contents
unzip -l dist/dash_mui_charts-0.0.5-py3-none-any.whl | head -30
```

### Step 4: Run Twine Check

```bash
twine check dist/*
```

Expected output:
```
Checking dist/dash_mui_charts-0.0.5.tar.gz: PASSED
Checking dist/dash_mui_charts-0.0.5-py3-none-any.whl: PASSED
```

---

## Publishing

### Option A: Test on TestPyPI First (Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    dash-mui-charts
```

### Option B: Publish to PyPI

```bash
# Upload to PyPI (production)
twine upload dist/*
```

---

## Post-Publication Verification

### 1. Install from PyPI

```bash
pip install dash-mui-charts
```

### 2. Test Import

```python
from dash_mui_charts import LineChart, PieChart, Heatmap, SparklineChart
print("All components imported successfully!")
```

### 3. Run Example

```bash
python usage.py
```

---

## Version Bump Workflow

For subsequent releases:

### 1. Update Version

Edit `package.json`:
```json
{
  "version": "0.0.6"
}
```

### 2. Update CHANGELOG.md

Add new version section with changes.

### 3. Rebuild and Publish

```bash
npm run build
rm -rf build/ dist/ *.egg-info/
python -m build
twine check dist/*
twine upload dist/*
```

### 4. Create Git Tag

```bash
git add -A
git commit -m "Release v0.0.6"
git tag -a v0.0.6 -m "Version 0.0.6"
git push origin main --tags
```

---

## Troubleshooting

### "File already exists" Error

Each version can only be uploaded once. Bump the version number.

### Missing Files in Package

Check `MANIFEST.in` includes all required files. Verify with:
```bash
tar tzf dist/dash_mui_charts-*.tar.gz
```

### README Not Rendering on PyPI

Ensure `long_description_content_type='text/markdown'` is set in `setup.py`.

### Import Errors After Installation

Verify `__init__.py` exports all components:
```python
from dash_mui_charts._imports_ import *
```

---

## Quick Reference Commands

```bash
# Full build and publish workflow
npm run build                       # Build React components
rm -rf build/ dist/ *.egg-info/     # Clean old builds
python -m build                      # Build Python package
twine check dist/*                   # Verify package
twine upload --repository testpypi dist/*  # Test upload
twine upload dist/*                  # Production upload
```

---

## Links

- **PyPI Project**: https://pypi.org/project/dash-mui-charts/
- **TestPyPI Project**: https://test.pypi.org/project/dash-mui-charts/
- **GitHub Repository**: https://github.com/pip-install-python/dash-mui-charts
- **PyPI Publishing Guide**: https://packaging.python.org/tutorials/packaging-projects/