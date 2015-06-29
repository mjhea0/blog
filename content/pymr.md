Title: PyMR A Python Multi-Repository Manager
Date: 2014-11-11 19:35
Category: Software
Tags: python, development
Summary: PyMR is a is Python command-line utility for running operations on sets of tagged directories.

[PyMR](https://github.com/kpurdon/pymr) is Python command-line utility for running operations on sets of tagged directories. I wrote PyMR in response to an issue development team I was part of ran into.

# The Issue

At [NSIDC](http://nsidc.org) we recently developed a polar data visualization application called [Satellite Observations of Arctic Change (SOAC)](http://nsidc.org/soac).

This application required quite a few components including:

* A JavaScript Web Application (Backbone, Leaflet)
* A Python Web Service (Flask)
* A Customized MapServer (MapServer)
* A Python Data Processing Pipeline (SciPy Stack)
* A Data Processing VM
* A Web VM (NGINX, Gunicorn, Upstart)

All of these components are developed in separate git repositories which means we end up with a project structure that looks like this:

    └── soac
        ├── soac-data
        ├── soac-data-vm
        ├── soac-mapserver
        ├── soac-service
        ├── soac-vm
        └── soac-webapp

This is perfect for our development workflow and allows us to develop, test, and deploy all of the components independently.

## So what's the problem?

### Versioning

When we are ready to release a version of the project we generally run some form of the command:

    :::bash
    $ git tag v#.#.# && git push --tags


The problem is that, although we have 6 repositories, we only have two release-able things.

1. The Web Application (soac-vm + soac-service + soac-mapserver + soac-webapp)
2. The Data Application (soac-data-vm + soac-data)

Say we want to release a new version of the web application we end up doing something like this:

    :::bash
    $ cd soac-vm && git tag v#.#.# && git push --tags
    $ cd soac-service && git tag v#.#.# && git push --tags
    $ cd soac-webapp && git tag v#.#.# && git push --tags
    $ cd soac-mapserver && git tag v#.#.# && git push --tags


This process involves a lot of human interaction and is prone to error. Initially a bash script was created to solve this issue however I found that unsatisfactory.

PyMR was created to simplify this process.

# Introducting PyMR

I created PyMR to simplify the problem outlined above.

After [installing](http://pymr.readthedocs.org/en/latest/installation/) PyMR the tool allows us to "register" directories.

In the case of the SOAC application we want two sets of registered directories.

1. The "web" directories
2. The "data" directories

Here is how we do it:

    :::bash
    $ cd soac-vm && pymr-register -t web
    $ cd soac-service && pymr-register -t web
    $ cd soac-webapp && pymr-register -t web
    $ cd soac-mapserver && pymr-register -t web
    $ cd soac-data-vm && pymr-register -t data
    $ cd soac-data && pymr-register -t data

This set of commands will create a file called ".pymr" in each of the directories where the register command was executed. The ".pymr" file has the following simple structure:

    [tags]
    tags = web

Now let's say we want to create a release of the SOAC web application.

## Before (Without PyMR)

    ::: bash
    $ cd soac-vm && git tag v#.#.# && git push --tags
    $ cd soac-service && git tag v#.#.# && git push --tags
    $ cd soac-webapp && git tag v#.#.# && git push --tags
    $ cd soac-mapserver && git tag v#.#.# && git push --tags

## After (With PyMR)

    :::bash
    pymr-run -t web 'git tag v#.#.# && git push --tags'


The "pymr-run" command will find all of the ".pymr" files that contain the tag "web" and then execute the given command in that directory.

I believe this is a simple, easy to install, and easy to use solution to a common development problem.

# What About (MU/MR/GR)?

Yes, other tools have already solved this problem. Here are the common ones I explored before creating PyMR:

* [GR](http://mixu.net/gr/)
* [MR](http://myrepos.branchable.com/)
* [MU](https://github.com/fabioz/mu-repo)

I found flaws in each of these tools that did not allow me to complete the task at hand in a satisfactory manner.

The biggest selling feature of PyMR (in my opinion) over others is that PyMR creates a configuration file (.pymr) WITH THE SOURCE DIRECTORY. Most of the above tools (if not all) create a single configuration file in the home directory which maps all of the "tagged" or "registered" directories so commands can be executed on them later. This does not allow the configuration to be source controlled and shared among a development team with the actual project source code.

In addition another selling feature of PyMR is that it is command agnostic. Meaning that any command you can run in the terminal you can pass to PyMR.

# Whats Next?

1. Try out PyMR on your own projects!
2. Find bugs, submit issues, think of features!
3. Contribute!
