title: Using Continuum Analytics Conda as a replacement for virtualenv, pyenv, and more!
date: 2015-07-26 11:30
category: Software, Tools
tags: python, development, conda
summary: Continuum Analytics Conda can be used as a replacement for virtualenv, pyenv, and more. This post will show you how to adopt conda for the basics of python development.

For the last year I have been using [conda](http://conda.pydata.org/docs/) by [Continuum Analytics](http://continuum.io/) as my primary python development toolkit. While conda provides much more than isolated environments (virtualenv), and switchable python versions (pyenv) those two features alone make it work the switch. This blog post will walk you (a new user) through the basic setup and use of [miniconda](http://conda.pydata.org/miniconda.html) (a light-weight distribution of conda).

![continuum analytics]({filename}/images/continuum-logo.png)
![anaconda]({filename}/images/anaconda-logo.png)

# Introduction To Conda

First a few (fairly confusing terms):

* **Continuum Analytics:** The company developing and distributing conda/miniconda/anaconda.
* **Conda:** The command-line tool itself. (Like *pip* or *virtualenv*)
* **Miniconda:** A minimal distribution of conda with nothing but the most basic features. (You should almost always start with an install of this)
* **Anaconda:** A curated collection (by Continuum Analytics) of common packages for scientific python users. This goes on top of miniconda.

Conda is normally marketed as much more than a simple replacement for the version of python on your system and isolated environments, and in reality it is! It's a completely new packaging system, package repository, and much more. However, at it's most basic level you can use it to manage the version of python you use and create isolated environments. You can even still use `pip` to install packages. **This blog post will cover this basic level of use.**

# Installation

For this guide we'll be installing the miniconda distribution. While conda is supported on all operating systems I'll be using OS X 10.10.3. You can find the official installation instructions [here](http://conda.pydata.org/docs/install/quick.html#quick-install).

### Download Miniconda

Go [here](http://conda.pydata.org/miniconda.html) and download the distribution for your operating system. You'll notice that there are both Python 2 and Python 3 versions. It actually does not matter which you get as conda treats Python itself as an install-able package so you can change the version at any time (more on this later). Choose whichever you want to be the default.

```bash
wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
```

### Install Miniconda

Run the installer and follow the prompts.

```bash
bash Miniconda-latest-MacOSX-x86_64.sh
```

*Note*: To run this install unattended you can use the `-b` option in the above command.

The installer will ask you if it should automatically add conda to the system path. Unless you plan to manually do this yourself let the installer do it for you. [Here](https://github.com/kpurdon/dotfiles/blob/master/bash/env#L2) is how I set up my PATH for conda.

# Replacing Virtualenv

For those of you that are not familiar with [virtualenv](https://virtualenv.pypa.io/en/latest/) it is a tool that allows you to create isolated environments with a set of packages installed from pip. The same functionality is available with the `conda create` and `conda env` command. For basic usage *conda create* is the command you want.

### Create An Environment

Let's say we want an environment to start working on a flask application.

* `conda create -n myflaskapp flask`

This command will create a new environment with the name *myflaskapp* and install the package *flask* in the environment.

**Note** that the *conda create* command requires that you give it the name of a package to install in the new environment. I really don't like this required argument, but a simple way to get around it is just to pass in `python` as the required package.

* `conda create -n myflaskapp python`

After running the above command you will be given the following information:

```
#
# To activate this environment, use:
# $ source activate myflaskapp
#
# To deactivate this environment, use:
# $ source deactivate
#
```

After running the command `source activate myflaskapp` you can see the list of installed packages in the environment with the `conda list` command.

```
(myflaskapp) $ conda list
# packages in environment at /Users/kpurdon/miniconda/envs/myflaskapp:
#
openssl                   1.0.1k                        1
pip                       7.1.0                    py34_0
python                    3.4.3                         0
readline                  6.2                           2
setuptools                18.0.1                   py34_0
sqlite                    3.8.4.1                       1
tk                        8.5.18                        0
xz                        5.0.5                         0
zlib                      1.2.8                         0
```

Notice the *py34_0* line on the right, these are the only python packages installed. The rest (python, readline, sqlite, tk, xz, and zlib) are non-python packages installed by conda. You can get a list of the python packages installed with `pip list`.

```
(myflaskapp) $ pip list
pip (7.1.0)
setuptools (18.0.1)
```

### Install Packages

Conda provides a complete alternative to *pip* and *pypi* packages, however you can still use *pip* just as you normally would. Let's continue our flask example and install the flask package using *pip* and then the *conda* alternative.

* `pip install flask`

```
(myflaskapp) $ conda list
# packages in environment at /Users/kpurdon/miniconda/envs/myflaskapp:
#
flask                     0.10.1                    <pip>
itsdangerous              0.24                      <pip>
jinja2                    2.8                       <pip>
markupsafe                0.23                      <pip>
openssl                   1.0.1k                        1
pip                       7.1.0                    py34_0
python                    3.4.3                         0
readline                  6.2                           2
setuptools                18.0.1                   py34_0
sqlite                    3.8.4.1                       1
tk                        8.5.18                        0
werkzeug                  0.10.4                    <pip>
xz                        5.0.5                         0
zlib                      1.2.8                         0
```

Notice that *conda list* shows the packages installed with pip by denoting *<pip\>* in the right column. Running `pip list` will show these:

```
(myflaskapp) $ pip list
Flask (0.10.1)
itsdangerous (0.24)
Jinja2 (2.8)
MarkupSafe (0.23)
pip (7.1.0)
setuptools (18.0.1)
Werkzeug (0.10.4)
```

Let's do the exact same thing using conda's alternative to *pip*, `conda install`. First let's remove the packages we just installed with *pip*.

```
(myflaskapp) $ pip uninstall flask itsdangerous Jinja2 MarkupSafe Werkzeug
```

Now we can install Flask with `conda install flask`.

```
(myflaskapp) $ conda list
# packages in environment at /Users/kpurdon/miniconda/envs/myflaskapp:
#
flask                     0.10.1                   py34_1
itsdangerous              0.24                     py34_0
jinja2                    2.7.3                    py34_1
markupsafe                0.23                     py34_0
openssl                   1.0.1k                        1
pip                       7.1.0                    py34_0
python                    3.4.3                         0
readline                  6.2                           2
setuptools                18.0.1                   py34_0
sqlite                    3.8.4.1                       1
tk                        8.5.18                        0
werkzeug                  0.10.4                   py34_0
xz                        5.0.5                         0
zlib                      1.2.8                         0
```

Notice now that flask and it's dependencies are shown just like pip and setuptools were *py34_0*. This means that instead of being installed from *pip* they were installed from [anaconda.org](http://anaconda.org/) (formerly binstar.org). However, if you go to that site and search for *flask* you'll see a ton of results, which one did we get? We can use `conda config` to find out.

Run the following command:

* `conda config --set show_channel_urls yes`

This will create/update a file in your home directory called *.condarc*. If this was the first time you set any config it will look like this:

```
$ cat ~/.condarc
show_channel_urls: yes
```

Now run `conda list`:

```
(myflaskapp) $ conda list
# packages in environment at /Users/kpurdon/miniconda/envs/myflaskapp:
#
flask                     0.10.1                   py34_1    defaults
itsdangerous              0.24                     py34_0    defaults
jinja2                    2.7.3                    py34_1    defaults
markupsafe                0.23                     py34_0    defaults
openssl                   1.0.1k                        1    http://repo.continuum.io/pkgs/free/osx-64/openssl-1.0.1k-1.tar.bz2
pip                       7.1.0                    py34_0    defaults
python                    3.4.3                         0    defaults
readline                  6.2                           2    <unknown>
setuptools                18.0.1                   py34_0    defaults
sqlite                    3.8.4.1                       1    http://repo.continuum.io/pkgs/free/osx-64/sqlite-3.8.4.1-1.tar.bz2
tk                        8.5.18                        0    http://repo.continuum.io/pkgs/free/osx-64/tk-8.5.18-0.tar.bz2
werkzeug                  0.10.4                   py34_0    defaults
xz                        5.0.5                         0    defaults
zlib                      1.2.8                         0    <unknown>
```

We have a new column on the right that lists the **channel** that the package came from. `defaults` is one of the official Continuum Analytics channels.

### pip install v. conda install

Now that we know that we can use both *pip* and *conda install* why/when should we use one over the other?

#### pip install

*Pro*

* Standard selection of Python packages.
* Most (if not all) packages are published here first.
* Most up-to-date releases.

*Con*

* Scientific Python (numpy, scipy, ...) take longer to install (and are often troublesome)

#### conda install

*Pro*

* Best integration with conda.
* Scientific Python (numpy, scipy, ...) are much easier/faster to install.

*Con*

* Often packages are not as up to date as pip
* Often packages on pip are not available on anaconda.org.

### Creating Requirements Files

A **requirements.txt** file is a standard way to store a list of versioned requirements from a virtualenv. Conda has an equivalent file called and **environment.yaml**. We can create both from a conda environment.

Given the following conda environment:

```
(myflaskapp) $ conda list
# packages in environment at /Users/kpurdon/miniconda/envs/myflaskapp:
#
flask                     0.10.1                   py34_1    defaults
itsdangerous              0.24                     py34_0    defaults
jinja2                    2.7.3                    py34_1    defaults
markupsafe                0.23                     py34_0    defaults
openssl                   1.0.1k                        1    http://repo.continuum.io/pkgs/free/osx-64/openssl-1.0.1k-1.tar.bz2
pip                       7.1.0                    py34_0    defaults
python                    3.4.3                         0    defaults
readline                  6.2                           2    <unknown>
setuptools                18.0.1                   py34_0    defaults
sqlite                    3.8.4.1                       1    http://repo.continuum.io/pkgs/free/osx-64/sqlite-3.8.4.1-1.tar.bz2
tk                        8.5.18                        0    http://repo.continuum.io/pkgs/free/osx-64/tk-8.5.18-0.tar.bz2
werkzeug                  0.10.4                   py34_0    defaults
xz                        5.0.5                         0    defaults
zlib                      1.2.8                         0    <unknown>
```

We can create a *requirements.txt* `pip list > requirements.txt`.

```
Flask (0.10.1)
itsdangerous (0.24)
Jinja2 (2.7.3)
MarkupSafe (0.23)
pip (7.1.0)
setuptools (18.0.1)
Werkzeug (0.10.4)
```

and an *environment.yaml* `conda env export > environment.yaml`.

```yaml
name: myflaskapp
dependencies:
- flask=0.10.1=py34_1
- itsdangerous=0.24=py34_0
- jinja2=2.7.3=py34_1
- markupsafe=0.23=py34_0
- openssl=1.0.1k=1
- pip=7.1.0=py34_0
- python=3.4.3=0
- readline=6.2=2
- setuptools=18.0.1=py34_0
- sqlite=3.8.4.1=1
- tk=8.5.18=0
- werkzeug=0.10.4=py34_0
- xz=5.0.5=0
- zlib=1.2.8=0
```


# Replacing pyenv

For those of you that are unfamiliar with [pyenv](https://github.com/yyuu/pyenv) it is a tool that allows you to install and switch between multiple versions of Python on a single system. We can do the same thing using *conda environments*. The following is how I use conda to manage Python versions.

### Create Environments

```
$ conda create -n py3 python=3*
$ conda create -n py2 python=2*
```

This will create two environments, one with Python3 and the other with Python2. I typically set one of these as my default by adding `source activate py3` to my terminal startup. Typically I only use these "named python" environments to run a Python REPL or do general Python tasks. I'll create another conda environment named specifically for each real project I work on.

# Conclusion

I hope this will get new users up and running with conda as a replacement for virtualenv and pyenv. If this post was helpful and you want more (diving deeper into conda) let me know on [twitter](https://twitter.com/PurdonKyle/status/625392730890309632).
