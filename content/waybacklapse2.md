title: Waybacklapse 2.0: A Python Wayback Machine Time-Lapse Creator (Now with Python3 and Docker!)
Date: 2015-07-18 13:57
Category: Software
Tags: python, development, timelapse, waybackmachine
Summary: Waybacklapse is a Wayback Machine time-lapse generator! (Now with Python3 and Docker!)

In December 2014 I released the first version of a Python command-line tool called Waybacklapse. If you did not see the release then I recommend you read the [short blog post](http://kylepurdon.com/blog/waybacklapse-a-python-wayback-machine-time-lapse-creator.html) about the original version.

# What is waybacklapse?

Waybacklapse is a Python  command line tool which allows a user to create a GIF of screen captures of any website for any given period of time. Awesome!

Here is an example output!

![reddit.com gif]({filename}/images/reddit-waybacklapse.gif)

# Version 2.0

The original version of Waybacklapse created a python package (available via pip) and required that the end-user installed imagemagick, phantomjs, node, npm, and [screenshot-as-a-service](https://github.com/fzaninotto/screenshot-as-a-service.git) on there own machine. For me all of these dependencies on the end-users system was unacceptable. In addition I didn't want to rely on an external service (screenshot-as-a-service) for something I could do internally. Enter version 2.0.

## Major Changes

**Docker!** I have now wrapped everything up into a docker container so that the user does not have to have anything installed on their own system (except docker of course). This also makes it very simple to get up and running.

**Python3** I upgraded the tool to Python3, enough said.

## Minor Changes

**WaybackCDX** I pulled out all of the Wayback Machine CDX API logic into a [utility class](https://github.com/kpurdon/waybacklapse/blob/v2.0.0/wayback/wayback.py).

**Tests** I've added some unit tests so that the tool is a bit more stable if/when I add new features.

# Getting Started

* Install [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).
* `git clone -b v2.0.0 git@github.com:kpurdon/waybacklapse.git`

## Manual Method

* `docker-compose build`
* `docker-compose up`
* `docker-compose run wayback python3 /usr/src/app/waybacklapse.py`
* For help `docker-compose run wayback python3 /usr/src/app/waybacklapse.py --help`

## Invoke Method

* `pip install invoke`
* `invoke runner`
* For help `invoke help`

After running the tool you should have a GIF ready and waiting for you! You can take a look at the output directory (in the current directory) to see your GIF!

# What's Next?

My grand plan is to turn this into a web application that allows the user to set all of the parameters in a nice web UI and send the processing off to some server. This goal may not be realized anytime soon (or ever), but it's a goal.

As always please report any bugs [on github](https://github.com/kpurdon/waybacklapse/issues).

# Examples

Note I have a [bug](https://github.com/kpurdon/waybacklapse/issues/5) to work on fixing the missing images.

## Google
![google.com gif]({filename}/images/google-waybacklapse.gif)

## Amazon
![amazon.com gif]({filename}/images/amazon-waybacklapse.gif)
