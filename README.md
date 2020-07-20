# Manylinux-wheel-builder
This action builds manylinux wheels for several recent versions of Python (3.6 - 3.9) and publishes to pypi. It uses docker image provided by pypa's [manylinux](https://github.com/pypa/manylinux) project. I am using [manylinux2010_x86_64 docker](https://quay.io/repository/pypa/manylinux2010_x86_64) image which requires `pip >= 19.0` on the client installing the built wheel.

## Basic Usage
If only want to build and publish wheels for linux platform then below CD action will be enough. It will only build and publish package if pushed commit contains a version tag because this seems the most appropriate in this case but you can change it if you want.
```yml
name: pypi deployer
on:
  push:
    tags:
      - 'v*' # Push events to matching v*, i.e. v1.0, v20.15.10
jobs:
  Linux-build:
    runs-on: ubuntu-latest
    env:
      TWINE_USERNAME: ${{ secrets.TWINE_USERNAME }}
      TWINE_PASSWORD: ${{ secrets.TWINE_PASSWORD }}
    steps:
      - uses: actions/checkout@v2
      - name: build and upload manylinux wheels
        uses:  Niraj-Kamdar/manylinux-wheel-builder@master
```

## Advanced Usage
If you also want to build and publish wheels for windows and macos in adition to linux, you can append above action with following yaml snippet. This relies on [setup-python](https://github.com/actions/setup-python) action.
```yml
Matrix-build:
    runs-on: ${{ matrix.os }}
    env:
      TWINE_USERNAME: ${{ secrets.TWINE_USERNAME }}
      TWINE_PASSWORD: ${{ secrets.TWINE_PASSWORD }}
    strategy:
      matrix:
        os: [macos-latest, windows-latest]
        python-version: [3.6, 3.7, 3.8]
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - name: build wheel
        run: |
          pip install wheel
          python setup.py bdist_wheel
      - name: upload wheel
        run: |
          pip install twine
          twine upload dist/*
        continue-on-error: true
```
Checkout example CD actions from [/examples](https://github.com/Niraj-Kamdar/manylinux-wheel-builder/tree/master/examples).
## FAQs
**1. Why don't I build wheel on ubuntu-latest and publish it directly to the PyPI?**

Building manylinux-compatible wheels is not trivial; as a general rule, binaries built on one Linux distro will only work on other Linux distros that are the same age or newer. Therefore, if we want to make binaries that run on most Linux distros, we have to use manylinux docker images. This is the reason why twine won't upload distro specific built wheel.

**2. Why did I choose manylinux2010?**

Pypa's manylinux has mentioned that - "The manylinux2010 tags allow projects to distribute wheels that are automatically installed (and work!) on the vast majority of desktop and server Linux distributions."

## Contributions
If you find any bugs or have any idea to improve this action please file an issue. You are also welcome to improve project documentation.
