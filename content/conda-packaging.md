title: Packaging Python Basics with Continuum Analytics Conda.
date: 2015-07-26 11:30
category: Software, Tools
tags: python, development, conda
summary: Continuum Analytics Conda can be used as a replacement for virtualenv, pyenv, and more. This post will dive into the "more" and show you how to build packages from scratch and from existing python projects.

![continuum analytics]({filename}/images/continuum-logo.png)
![anaconda]({filename}/images/anaconda-logo.png)

After my [recent post](http://kylepurdon.com/blog/using-continuum-analytics-conda-as-a-replacement-for-virtualenv-pyenv-and-more.html) on conda basics I got a request on [reddit](https://www.reddit.com/r/Python/comments/3ep2ae/using_continuum_analytics_conda_as_a_replacement/).

I posted:
> 2\. Is the author willing to package on anaconda.org (if yes: help, then conda install)
>
> 3\. Does the author care if I put it on anaconda.org (if not: conda skeleton from pypi and then conda install)

And got this [response](https://www.reddit.com/r/Python/comments/3ep2ae/using_continuum_analytics_conda_as_a_replacement/cthvzl9) from [/u/Ogi010](https://www.reddit.com/user/Ogi010):
> Is there a guide for step 2 or 3 out there? I would love to help packages be available on the conda environment, and I want to be a good citizen about it, but I don't want to get in the way...

What I found, other than the [official docs](http://conda.pydata.org/docs/build_tutorials.html) was a fairly sparse set of [google results](https://www.google.com/search?q=conda+packaging&oq=conda+&aqs=chrome.0.69i59j69i60l2j69i59j69i60l2.1252j0j4&sourceid=chrome&es_sm=119&ie=UTF-8) on the topic.

What I want to accomplish with this blog post is to get a new conda user to the point that they can:

1. Build a simple conda package from scratch.
2. Convert an existing python package to conda.
3. Take a package from pypi and put it on anaconda.org.

# What is a conda package?

> A conda package is a package that can be installed using the conda install [packagename] command.
>
> It includes a link to a tarball or bzipped tar archive (.tar.bz2) which contains metadata under the info/ directory, and a collection of files which are installed directly into an install prefix.
>
> The format is identical across platforms and operating systems. During the install process, files are extracted into the install prefix, except for files in the info/ directory. Installing the files of a conda package into an environment can be thought of as changing the directory to an environment, then downloading and extracting the zip file and its dependencies – all with the single conda install [packagename] command.
>
-- [Continuum Analytics Docs](http://conda.pydata.org/docs/build_tutorials/pkgs2.html#what-is-a-conda-package)


# Example Project

For all of the following tutorials we'll be using the same example project. It's a simple tool that given a string "YYYYMMDD" it will return the day of the year. We'll be able to both run the tool from the command line, and from other python code by importing it. Let's look at the bare Python project without any conda specific configuration.

```
dtools/
├── conversion
│   ├── __init__.py
│   ├── cli.py
│   ├── convert.py
│   └── tests
│       └── test_convert.py
├── setup.py
└── tasks.py
└── .flake8rc
```

This directory defines a project *dtools*, a package *conversion*, and two modules *cli.py* and *convert.py*. In addition it includes the standard python package descriptor file *setup.py*, and an [invoke](https://github.com/pyinvoke/invoke) tasks file *tasks.py*.

The actual source is VERY simple:

*convert.py*
```python
from datetime import datetime as dt


def yyyymmdd_to_doy(yyyymmdd):
    """
    Convert a yyyymmdd (str) to a day-of-year (str)
    """

    yyyymmdd_dt = dt.strptime(yyyymmdd, '%Y%m%d')

    return yyyymmdd_dt.strftime('%j')
```

*cli.py*
```python
import pkg_resources

import click

from conversion import convert


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    version = pkg_resources.get_distribution('dtools').version
    click.echo(version)
    ctx.exit()


@click.command()
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False,
              is_eager=True)
@click.help_option('-h', '--help')
@click.argument('yyyymmdd', type=click.STRING)
def main(yyyymmdd):
    """
    Converts a given YYYYMMDD to DOY.
    """
    doy = convert.yyyymmdd_to_doy(yyyymmdd)
    click.echo(doy)

if __name__ == '__main__':
    main()
```

*setup.py*
```python
from setuptools import setup, find_packages

setup(
    name='dtools',
    version='0.0.1',
    description='Date Tools',
    url='https://github.com/kpurdon/dtools',
    author='Kyle W. Purdon',
    author_email='kylepurdon@gmail.com',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 1 - Planning'
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages()
)
```

*tasks.py*
```python
from invoke import task, run


@task
def clean():
    run('find . -name "*.pyc" -type f -delete')
    run('find . -name "__pycache__" -type d -delete')


@task()
def test():
    run('flake8 . -v --config=.flake8rc')
    run('nosetests --verbose')


@task(pre=[test])
def build():
    run('python setup.py install')
```

# Packaging A Project

Amazingly to turn this project into a conda package we only need to add a single file, the *meta.yaml*.

**EDIT 07/29/2015**: The build:script commands were incorrect.

```python
package:
  name: dtools
  version: "0.0.1"

source:
  path: .

build:
  script:
    - flake8 . -v --config=.flake8rc
    - nosetests --verbose
    - python setup.py install
  entry_points:
    - yyyymmdd2doy = conversion.cli:main

requirements:
  build:
    - python
    - setuptools
    - nose
    - flake8
    - click
  run:
    - python
    - click

test:
  imports:
    - conversion
  commands:
    - yyyymmdd2doy -v
    - yyyymmdd2doy --version
    - yyyymmdd2doy -h
    - yyyymmdd2doy --help

about:
  home: https://github.com/kpurdon/dtools
  license: GPLv3+
```

I think the best way to explain how conda packaging works is to work through this file section by section. For more detailed information (and all available options) you should read through the [official documentation](http://conda.pydata.org/docs/building/meta-yaml.html).

### package

```yaml
package:
  name: dtools
  version: "0.0.1"
```

This section describes the basic information about the package including it's name and version. This is actually the only required information for a meta.yaml.

### source

```yaml
source:
  path: .
```

This section tells conda where to get the source from. In this case we are just building from the local directory, but you can specify a version controlled repo and conda will automatically download the source.

### build

```yaml
build:
  script:
    - flake8 . -v --config=.flake8rc
    - nosetests --verbose
    - python setup.py install
  entry_points:
    - yyyymmdd2doy = conversion.cli:main
```

This section is the meat of building a python package. Here we are defining the following build process:

* Run [flake8](https://pypi.python.org/pypi/flake8) to check the syntax for pep8 compatibility. (optional, but I recommend it)
* Run [nosetests](https://nose.readthedocs.org/en/latest/) to run any unittests defined in the project.
* Run install on the *setup.py*.

We are also defining an entry_point (a command that can be run directly from the command-line after install). The format of an entry_point is `command = package.module:function`.

### requirements

```yaml
requirements:
  build:
    - python
    - setuptools
    - nose
    - flake8
    - click
  run:
    - python
    - click
```

This section defines the build and runtime requirements for our package.

### test

```yaml
test:
  imports:
    - conversion
  commands:
    - yyyymmdd2doy -v
    - yyyymmdd2doy --version
    - yyyymmdd2doy -h
    - yyyymmdd2doy --help
```

This section defines post-install tests that we can run during the `conda build` process. Conda installs the built package in a temporary environment during the build process and then will run any tests defined in this section.

### about

```yaml
about:
  home: https://github.com/kpurdon/dtools
  license: GPLv3+
```

This is a "metadata" section that is optional.

# Converting an Existing Package

Notice in the test section of the *meta.yaml* we are duplicating logic that we already have in our file *tasks.py*. Ideally we could add a new task called *build* and then change the section from:

```yaml
build:
  script:
    - flake8 . -v --config=.flake8rc
    - nosetests --verbose
    - python setup.py install
```

to the following:

```yaml
build:
  script: invoke build
```

The build task:

```python
@task(pre=[test])
def build():
    run('python setup.py install')
```

This would require us to add *invoke* to our build requirements:

```yaml
requirements:
  build:
    ...
    - invoke
    ...
```

However, after adding this and running `conda build .` from the root of the project we get the following error:

`Error: No packages found in current osx-64 channels matching: invoke`

This means that none of the channels on [anaconda.org](http://anaconda.org/) that are included by default contain the package *invoke*. If we search for [invoke on anaconda.org](http://anaconda.org/search?q=access%3Apublic+type%3Aconda+invoke) we see the following results:

![anaconda.org invoke results]({filename}/images/anaconda-invoke-results.png)

None of these results are from official channels and therefore I would not recommend using them as there is no guarantee they will be correct, and/or exist tomorrow. We have a few options now:

1. Ask the authors of invoke to package and distribute on conda.
2. Add invoke to the [conda-recipes](https://github.com/conda/conda-recipes) repo. (An official conda channel).
3. Create our own conda package from the current invoke package on pypi.

In this case I'm fairly certain option 1 is not going to happen as the authors never packaged fabric for conda, and fabric is already included in the conda-recipes repo. This makes option 2 a good option, so lets start with that!

### Contribute Invoke Recipe

For those of you that have never contributed to an open-source project you might want to take a look at [this guide](https://guides.github.com/activities/contributing-to-open-source/). Here is what we are going to do:

1. Fork the [conda-recipes](https://github.com/conda/conda-recipes) repo.
2. Add a new recipe for invoke.
3. Create a pull-request to submit the recipe back to the original repo.

After forking the repo on github I run the follwing commands to add a recipe for invoke:

```
$ git clone git@github.com:kpurdon/conda-recipes.git
$ cd conda-recipes
$ conda skeleton pypi invoke
$ git add invoke/
$ git commit -m 'add skeleton invoke recipe'
$ git push
```

Before we submit a pull-request we'll want to confirm that we can build and install from the recipe that was generated by the `conda skeleton` command. *conda skeleton* gives us the following directory:

```
invoke/
├── bld.bat
├── build.sh
└── meta.yaml
```

The *bld.bat* and *build.sh* files both just contain `python setup.py install` so the *meta.yaml* is all we need to look at.

*metal.yaml*
```yaml
package:
  name: invoke
  version: "0.10.1"

source:
  fn: invoke-0.10.1.tar.gz
  url: https://pypi.python.org/packages/source/i/invoke/invoke-0.10.1.tar.gz
  md5: 68b5858e2d03e2df00c35d3ae843b45e

build:
  entry_points:
    - invoke = invoke.cli:main
    - inv = invoke.cli:main

requirements:
  build:
    - python
    - setuptools
  run:
    - python

test:
  imports:
    - invoke
    - invoke.parser
    - invoke.vendor
    - invoke.vendor.fluidity
    - invoke.vendor.lexicon
    - invoke.vendor.yaml2
    - invoke.vendor.yaml3
  commands:
    - invoke --help
    - inv --help

about:
  home: http://docs.pyinvoke.org
  license: BSD License
  summary: 'Pythonic task execution'
```

We can now run the following command to test the build: `conda build invoke`. From the default skeleton we'll get this error:

`ImportError: No module named 'error'`

As it turns out there is (I think) a small bug with relative imports in the **invoke.vendor.yaml2** package. For now we can just comment out that line in the *meta.yaml* imports section and get a successful build. After the build succeeds we'll get the following message:

```
# If you want to upload this package to binstar.org later, type:
#
# $ binstar upload /Users/kpurdon/miniconda/conda-bld/osx-64/invoke-0.10.1-py34_0.tar.bz2
```

This is the point when we could upload this package to our own channel on *anaconda.org*. I'll cover how to do this shortly, but for now we need to install this package locally and test that it works. To do that I run the following command:

`conda install /Users/kpurdon/miniconda/conda-bld/osx-64/invoke-0.10.1-py34_0.tar.bz2`

After this I run a few basic tests (just running normal invoke commands on my own project) to confirm that it is working. After that confirmation the contribution is ready for a pull request back to *conda-recipes*. You can see the pull request I submitted [here](https://github.com/conda/conda-recipes/pull/365).

At this point I want to continue with this tutorial and getting the invoke package officially out (from my pull request) might take a while. In the meantime I want to upload the package to my own channel on anaconda.org.

### Upload Invoke to Your Channel

This section will cover the original (option 3) posed in the introduction:

> 3\. Does the author care if I put it on anaconda.org (if not: conda skeleton from pypi and then conda install)

As long as the license allows redistribution you can upload whatever you want to anaconda.org. For this the process is very similar to a contribution to the *conda-recipes* repository. To create a package on my user channel (kpurdon) for invoke I ran the following commands:

```bash
$ conda skeleton pypi invoke
$ conda build invoke
```

I then get the following:

```
# If you want to upload this package to binstar.org later, type:
#
# $ binstar upload /Users/kpurdon/miniconda/conda-bld/osx-64/invoke-0.10.1-py34_0.tar.bz2
```

At this point I could run the command shown, and have the osx-64 version on binstar. However I want to upload a version for all operating systems (it's just good practice). For that I run the following commands:

```bash
$ cd /Users/kpurdon/miniconda/conda-bld/
$ conda convert osx-64/invoke-0.10.1-py34_0.tar.bz2 -p all
$ binstar upload */invoke-0.10.1-py34_0.tar.bz2
```

After running this command we can perform the same search for invoke on anaconda.org we did earlier and we now get the following results:

![anaconda.org invoke results kpurdon]({filename}/images/anaconda-invoke-results-kpurdon.png)

Notice now that my channel (kpurdon) contains the *invoke 0.10.1* package for all operating systems. We can now install the kpurdon version of invoke with the following command:

`$ conda install -c kpurdon invoke`

Now we can continue packaging our project!

# Packaging A Project (cont...)

Remember that we were trying to add *invoke* as a requirement in our *meta.yaml* so that we didn't duplicate build logic we were already defining in our *tasks.py*.

```yaml
requirements:
  build:
    ...
    - invoke
    ...
```

However, after adding this and running `conda build .` from the root of the project we got the following error:

`Error: No packages found in current osx-64 channels matching: invoke`

Again, this means that no package called invoke is available in any of the default channels. However in the previous section we created the invoke package and uploaded it to the (kpurdon) channel. In order for our *meta.yaml* to pick up invoke from `-c kpurdon` we need to set up our conda configuration by running:

`conda config --add channels kpurdon`

Now we can run `conda build .` and we will not get the above error about invoke not working, instead we get:

**Success!**
```
# If you want to upload this package to binstar.org later, type:
#
# $ binstar upload /Users/kpurdon/miniconda/conda-bld/osx-64/dtools-0.0.1-py34_0.tar.bz2
#
# To have conda build upload to binstar automatically, use
# $ conda config --set binstar_upload yes
```

Instead of uploading to binstar let's just install it locally:

`conda install /Users/kpurdon/miniconda/conda-bld/osx-64/dtools-0.0.1-py34_0.tar.bz2`

Then we can run the command to test everything works:

```bash
$ yyyymmdd2doy --version
0.0.1
```

```bash
$ yyyymmdd2doy --help
Usage: yyyymmdd2doy [OPTIONS] YYYYMMDD

  Converts a given YYYYMMDD to DOY.

Options:
  -v, --version
  -h, --help     Show this message and exit.
```

```bash
$ yyyymmdd2doy 20110101
001
```

We can also use this from a file:

*test.py*
```python
from conversion import convert

doy = convert.yyyymmdd_to_doy('20110101')
print(doy)
```

And we get the follwing results:

```bash
$ python test.py
001
```

# Conclusion

I hope that this post will help new users, and current users grasp the basics of conda packaging.  If this post was helpful and you want more (diving deeper into conda) let me know on [twitter](https://twitter.com/PurdonKyle/status/625781622126698496).
