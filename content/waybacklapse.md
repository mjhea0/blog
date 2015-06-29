title: Waybacklapse: A Python Wayback Machine Time-Lapse Creator
Date: 2014-12-06 13:23
Category: Software
Tags: python, development, timelapse, waybackmachine
Summary: Waybacklapse is a Wayback Machine time-lapse generator!


The [Wayback Machine](https://archive.org/web/) from the Internet Archive is a tool that allows you to view "captures" of websites from a specific time in the past. I have used this tool many times usually driven by curiosity and nostalgia for web design of the past. Recently I found myself wanting to view a timelapse of Wayback Machine images. I assumed there was something out there that would easily let me do this but to my surprise there was not!

Enter, waybacklapse.

# What is waybacklapse?

Waybacklapse is a Python package (that installs a command line tool) which allows a user to create a GIF of screen captures of any website for any given period of time. Awesome!

Here is an example output!

![reddit.com gif]({filename}/images/reddit-waybacklapse.gif)

# The Catch

## Catch #1 (Capturing Screenshots)

As it turns out capturing screenshots in python is not a simple task. It's absolutely possible and there are examples out there but I wanted a quick solution for this tool. For now I have found a great node application [screenshot-as-a-service](https://github.com/fzaninotto/screenshot-as-a-service) that is required for waybacklapse to work.

## Catch #2 (Generating a GIF)

Now at this point I REALLY just wanted a fast solution. Creating a GIF from a series of images in Python is not to difficult but I had [imagemagick](http://www.imagemagick.org/script/index.php) installed and ready to go. So I took the easy way out and shelled out to imagemagick.

## Well then, what DOES waybacklapse do?

Honestly, not much. It creates a nice command-line interface, wraps up the Wayback Machine [CDX API](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server) and manages directories. Other than that it's basically shelling out to do all the real work.

# Getting Started

So, now that the catch/s are out in the open here is what you need to run waybacklapse (on MacOS X) from scratch:

## Install screenshot-as-a-service

    :::bash
    $ brew install imagemagick
    $ brew install phantomjs
    $ git clone https://github.com/fzaninotto/screenshot-as-a-service.git
    $ cd screenshot-as-a-service
    $ git checkout -t v1.1.0
    $ npm install

## Install waybacklapse

Note, if you don't want to use a virtualenv skip the first two command.

    :::bash
    $ virtualenv .waybacklapse
    $ . .waybacklapse/bin/activate
    (waybacklapse) $ pip install waybacklapse

## Run waybacklapse

    :::bash
    (waybacklapse) $ waybacklapse
    [follow the user prompts]

After running this command you should have a GIF ready and waiting for you! You can take a look at the output to see the paths to the GIF and images.

# What's Next?

My grand plan is to turn this into a web application that allows the user to set all of the parameters in a nice web UI and send the processing off to some server. This goal may not be realized anytime soon (or ever), but it's a goal.

If your really dying to contribute let me know (I'll need to get some documentation together) but here are the most "pressing" tasks:

1. Tests! (A few unittests can't hurt)
2. Python native screenshot from a URL. (Possibly with [Ghost.py](http://jeanphix.me/Ghost.py/))
3. Python native PNG to GIF creation.

As always feel free to leave questions or comments here or on [Github](https://github.com/kpurdon/waybacklapse).
