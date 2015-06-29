title: A Python Versioning Workflow with Bumpversion
Date: 2015-01-25 20:32
Category: Software
Tags: python, development, version
Summary: Bumpversion is a python versioning utility. This post details a specific example of it's usage for continously integrated and deployed Python packages.

Recently, at [NSIDC](http://nsidc.org) we developed a workflow for creating, continuously integrating, and releasing Python packages. A key aspect of this project was automating the process of versioning for development pre-releases and production releases. I devised a solution using the Python [bumpversion](https://pypi.python.org/pypi/bumpversion/0.5.0) utility.

# What Is Bumpversion?

> [Bumpversion is] a small command line tool to simplify releasing software by updating all version strings in your source code by the correct increment.

I have used bumpversion many times in [personal projects](https://github.com/kpurdon) and we have used the tool at NSIDC as well. However we have mostly been using the default implementation of bumpversion.

The basic setup of bumpversion is to drop a .bumversion.cfg in the root of your project that contains the following code:

    :::python
    [bumpversion]
    current_version = 0.0.0
    commit = True
    tag = True

With this file, and bumversion installed you can run the command

    :::bash
    $ bumpversion [patch | minor | major]

which will bump the version to 0.0.1, 0.1.0, or 1.0.0 respectively (assuming you started at 0.0.0). In addition because the commit, and tag flags are set to true bumpversion will create a tag and commit to your git repository. ([see this commit for an example](https://github.com/kpurdon/pymr/commit/5e87677563527beb6126b4c991abb53afbeb2a93)).

This setup works great if all you care about is patch, minor, or major versions. However when you need something like 1.0.0rc to indicate a pre-release (or snapshot) the setup is slightly more complex.

# NSIDC Python Package Workflow

Our current workflow for generating a Python package at NSIDC follows:

1. Developer creates a feature branch.
2. Developer creates and commits the feature.
3. Developer creates a pull request.
4. Development team reviews pull requests and merges to master when appropriate.
5. A custom [Jenkins](http://jenkins-ci.org/) integration server runs a series of tests.
6. A custom [Jenkins](http://jenkins-ci.org/) integration server publishes a python package to an internal  [devpi](http://doc.devpi.net/latest/) server. (snapshot)
7. A developer clicks a button to create a new production release.
8. A custom [Jenkins](http://jenkins-ci.org/) integration server publishes a python package to an internal  [devpi](http://doc.devpi.net/latest/) server. (production) and removes and snapshot packages.

Versioning comes into play at step 1 and step 7 in this workflow. To make this clear lets assume the current version is 1.0.0rc and we are at step 7 in the process. This step will execute the following tasks:

## 1. Bump Release Version

### Starting Version: 1.0.0rc

The release job runs the command `bumpversion release` which essentially drops and release qualifier ("rc" in this case) from the version.

### Ending Version: 1.0.0

## 2. Build Release Package

With a production version (no "rc") the job will build and release the package to an internal repo.

## 3. Prepare Next Development Version

### Starting Version: 1.0.0

To prepare the project git repository for the next developer to pick up at step 1 the job will run ```bumpversion patch```. Because of the custom configuration (described in the next section) the version will now be 1.0.1rc. This means that the next developer will be starting with the next (lowest possible) release candidate.

### Ending Version: 1.0.1rc

Note that we chose to use "patch" as the default next version. If the developer wants to work on a minor or major feature they can manually run `bumpversion [minor|major]` on the feature branch which would result in versions of 1.1.0rc or 2.0.0rc in the given example.

# NSIDC Bumpversion Implementation

The following is an example of the .bumversion.cfg we have devised for achieving the workflow outlined above:

    :::python
    [bumpversion]
    current_version = 1.0.0
    commit = True
    tag = True
    parse = (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)((?P<release>.*))?
    serialize =
	    {major}.{minor}.{patch}{release}
	    {major}.{minor}.{patch}

    [bumpversion:part:release]
    optional_value = production
    values =
	    rc
	    production

The following outlines the additions and modifications from the default example and there purpose:

## bumpversion:part:release

    :::python
    [bumpversion:part:release]
    optional_value = production
    values =
	    rc
	    production

This section adds an additional object to the default version number, the "release" part. This is the "rc" in the version 1.0.0rc. Note that we define two values "rc" and "production" and define the "production" value as optional.

Let's start with the version 1.0.0 and see what happens as we run a series of bumpversion commands:

### Patch Version
#### Starting Version: 1.0.0
#### Command: ```bumpversion patch```
#### Ending Version: 1.0.1rc

Note that minor and major perform the same as patch.

### Release Version
#### Starting Version: 2.0.0rc
#### Command: ```bumpversion release```
#### Ending Version: 2.0.0

Because we have added a "release" part and set the first value to "rc" any time that we run bumpversion with patch, minor, or major the "rc" part will be included in the version. Then when we "bump" the release value using ```bumpversion release``` it will become "production", which because it is set to optional will be omitted resulting in a version with only major.minor.patch.

## Custom parse & serialize

    :::python
    parse = (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)((?P<release>.*))?
    serialize =
	    {major}.{minor}.{patch}{release}
	    {major}.{minor}.{patch}

This block parses and serializes the version number. The default value for these is:

    :::python
    parse = (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)
    serialize =
	    {major}.{minor}.{patch}

Note that we have added "release" both to parse and serialize. The parse is just Python regex ```((?P<release>.*))?``` which is looking for any value (including an empty value) and storing it as "release". Serialize is simply a template specifying and additional possible serializer which includes the ```{release}``` part.

# Conclusion

Note that bumpversion provides a [similar example](https://github.com/peritus/bumpversion#part-specific-configuration) which I found a bit too confusing given the arbitrary values. I hope that the more concrete example I have outlined above will clarify the additional part configuration a bit.
