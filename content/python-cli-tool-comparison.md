title: Comparing Python Command-Line Parsing Libraries (Argparse, Docopt, and Click)
date:
category: Software, Tools
tags: python, development
summary: A comparison of Python command-line utility libraries (argparse, docopt, and click).
status: draft

About a year ago I began a job where building command-line applications was a common occurrence. At that time I had used [argparse](https://docs.python.org/3/library/argparse.html) quite a bit and wanted to explore what other options were available. I found that the most popular alternatives available were [click](http://click.pocoo.org/4/) and [docopt](http://docopt.org/). During my exploration I also found that other than each libraries "why use me" section there was not much available for a complete comparison of the three libraries. Now there is! If you want to you can [head directly to the source](https://github.com/kpurdon/greeters) though it really won't do much good without the comparisons and step-by-step construction presented in this article. I'll keep my opinion out of the construction and comparison (as much as possible) and present my preference in the conclusion.

I'll be using the following versions in the comparisons during this article:

```bash
$ python --version
Python 3.4.3 :: Continuum Analytics, Inc.

# argparse is a Python core library

$ pip list | grep click
click (4.1)

$ pip list | grep docopt
docopt (0.6.2)

$ pip list | grep invoke  # ignore this for now, it's a special surprise for later!
invoke (0.10.1)
```

# Command-Line Example

The command-line application that we are creating will have the following interface:

`python [file].py [command] [options] NAME`

**Basic Usage**
```bash
$ python [file].py hello Kyle
Hello, Kyle!

$ python [file].py goodbye Kyle
Goodbye, Kyle!
```

**Usage w/ Options (Flags)**
```bash
$ python [file].py hello --greeting=Wazzup Kyle
Whazzup, Kyle!

$ python [file].py goodbye --greeting=Later Kyle
Later, Kyle!

$ python [file].py hello --caps Kyle
HELLO, KYLE!

$ python [file].py hello --greeting=Wazzup --caps Kyle
WAZZUP, KYLE!
```

This command-line application breaks down into a few things the library we choose will need to implement. This article will compare each libraries method for implementing the following features:

1. Commands (hello, goodbye)
2. Arguments (name)
3. Options/Flags (--greeting=<str\>, --caps)

In addition automated help messages are important, and to throw a wrench in lets say we also want a `-v/--version` option that will print the version number and quit. As you would expect argparse, docopt, and click implement all of these features (as any complete command-line library would). This fact means that the actual implementation of these features is what we will compare. Each library takes a very different approach (argparse=standard, docopt=docstrings, click=decorators) that will lend to a very interesting comparison.

**Bonus Sections**

1. I've been curious about using task-runner libraries like [fabric](https://fabric.readthedocs.org/en/latest/) and it's python3 replacement [invoke](https://invoke.readthedocs.org/en/latest/) to create simple command-line interfaces I will try and put the same interface together with invoke.
2. A few extra steps are needed when packaging command-line applications, i'll cover those as well!

# Commands

Let's begin by setting up the basic skeleton (no arguments or options) with each library.

### Argparse

```python
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

hello_parser = subparsers.add_parser('hello')
goodbye_parser = subparsers.add_parser('goodbye')

if __name__ == '__main__':
    args = parser.parse_args()
```

With this we now have two commands (hello, goodbye) and a built-in help message. Notice that the help message changes when run as an option on the command hello.

```bash
$ python argparse/commands.py --help
usage: commands.py [-h] {hello,goodbye} ...

positional arguments:
  {hello,goodbye}

optional arguments:
  -h, --help       show this help message and exit

$ python argparse/commands.py hello --help
usage: commands.py hello [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### Docopt

```python
"""Greeter.

Usage:
  commands.py hello
  commands.py goodbye
  commands.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__)
```

With this we now have two commands (hello, goodbye) and a built-in help message. Notice that the help message **DOES NOT** change when run as an option on the command hello. In addition we **do not** need to explicitly specify the `commands.py -h | --help` in the *Options* section to get a help command. However, if we don't they will not show up in the output help message as options.

```bash

$ python docopt/commands.py --help
Greeter.

Usage:
  commands.py hello
  commands.py goodbye
  commands.py -h | --help

Options:
  -h --help     Show this screen.

$ python docopt/commands.py hello --help
Greeter.

Usage:
  commands.py hello
  commands.py goodbye
  commands.py -h | --help

Options:
  -h --help     Show this screen.
```

### Click

```python
import click


@click.group()
def greet():
    pass


@greet.command()
def hello(**kwargs):
    pass


@greet.command()
def goodbye(**kwargs):
    pass

if __name__ == '__main__':
    greet()
```

With this we now have two commands (hello, goodbye) and a built-in help message. Notice that the help message changes when run as an option on the command hello.

```bash
$ python click/commands.py --help
Usage: commands.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  goodbye
  hello

$ python click/commands.py hello --help
Usage: commands.py hello [OPTIONS]

Options:
  --help  Show this message and exit.
```

Even at this point you can see that we have very different approaches to constructing a basic command-line application. Next let's add the *NAME* argument, and the logic to print the result to each tool.

# Arguments

In this section I will be adding new logic to the same code shown in the previous section. I'll add comments to new lines stating there purpose. Arguments (a.k.a positional arguments) are required inputs to a command-line application. In this case we are adding a required "name" argument so that the tool can greet a specific person.

### Argparse

To add an argument to a subcommand we use the `add_argument` method. And in order to execute the correct logic when a command is called we use the `set_defaults` method to set a default function. Finally we execute the default function by calling `args.func(args)` after we parse the arguments at runtime.

```python
import argparse


def hello(args):
    print('Hello, {0}!'.format(args.name))


def goodbye(args):
    print('Goodbye, {0}!'.format(args.name))

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

hello_parser = subparsers.add_parser('hello')
hello_parser.add_argument('name')  # add the name argument
hello_parser.set_defaults(func=hello)  # set the default function to hello

goodbye_parser = subparsers.add_parser('goodbye')
goodbye_parser.add_argument('name')
goodbye_parser.set_defaults(func=goodbye)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)  # call the default function
```

```bash
$ python argparse/arguments.py hello Kyle
Hello, Kyle!

$ python argparse/arguments.py hello --help
usage: arguments.py hello [-h] name

positional arguments:
  name

optional arguments:
  -h, --help  show this help message and exit
```

### Docopt

In order to add an option we add a `<name>` to the docstring. The `<>` are used to designate a positional argument. In order to execute the correct logic we must check if the command (treated as an argument) is True at runtime `if arguments['hello']:`, then call the correct function.

```python
"""Greeter.

Usage:
  basic.py hello <name>
  basic.py goodbye <name>
  basic.py (-h | --help)

Options:
  -h --help     Show this screen.

"""
from docopt import docopt


def hello(name):
    print('Hello, {0}'.format(name))


def goodbye(name):
    print('Goodbye, {0}'.format(name))

if __name__ == '__main__':
    arguments = docopt(__doc__)

    if arguments['hello']:  # if an argument called hello was passed, execute the hello logic.
        hello(arguments['<name>'])
    elif arguments['goodbye']:
        goodbye(arguments['<name>'])
```

```bash
$ python docopt/arguments.py hello Kyle
Hello, Kyle

$ python docopt/arguments.py hello --help
Greeter.

Usage:
  basic.py hello <name>
  basic.py goodbye <name>
  basic.py (-h | --help)

Options:
  -h --help     Show this screen.
```

Note that the help message is not specific to the subcommand, rather it is the entire docstring for the program.

### Click

In order to add an argument to a click command we use the `@click.argument` decorator. In this case we are just passing the argument name, but there are [many more options](http://click.pocoo.org/4/arguments/) some of which we'll use later. Since we are decorating the logic (function) with the argument we don't need to do anything to set or make a call to the correct logic.

```python
import click


@click.group()
def greet():
    pass


@greet.command()
@click.argument('name')  # add the name argument
def hello(**kwargs):
    print('Hello, {0}!'.format(kwargs['name']))


@greet.command()
@click.argument('name')
def goodbye(**kwargs):
    print('Goodbye, {0}!'.format(kwargs['name']))

if __name__ == '__main__':
    greet()
```

```bash
$ python click/arguments.py hello Kyle
Hello, Kyle!

$ python click/arguments.py hello --help
Usage: arguments.py hello [OPTIONS] NAME

Options:
  --help  Show this message and exit.
```

# Flags/Options

In this section I will again be adding new logic to the same code shown in the previous section. I'll add comments to new lines stating there purpose. Options are non-required inputs that can be given to alter the execution of a command-line application. Flags are a boolean only (True/False) subset of options. For example: `--foo=bar` will pass *bar* as the value for the *foo* option, `--baz` (if defined as a flag) will pass the value of True is the option is given, or False if not.

For this example we are going to add the `--greeting=[greeting]` option, and the `--caps` flag. The *greeting* option will have default values of "Hello" and "Goodbye" (for hello, and goodbye commands) and allow the user to pass in a custom greeting. For example given `--greeting=Wazzup` the tool will respond with *Wazzup, [name]!*. The `--caps` flag will uppercase the entire response if given. For example given `--caps` the tool will respond with *HELLO, [NAME]!*.

### Argparse

```python
import argparse

# since we are now passing in the greeting the logic has been consolidated to a single greet function
def greet(args):
    output = '{0}, {1}!'.format(args.greeting, args.name)
    if args.caps:
        output = output.upper()
    print(output)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

hello_parser = subparsers.add_parser('hello')
hello_parser.add_argument('name')
hello_parser.add_argument('--greeting', default='Hello')  # add greeting option w/ default
hello_parser.add_argument('--caps', action='store_true')  # add a flag (default=False)
hello_parser.set_defaults(func=greet)

goodbye_parser = subparsers.add_parser('goodbye')
goodbye_parser.add_argument('name')
goodbye_parser.add_argument('--greeting', default='Goodbye')
goodbye_parser.add_argument('--caps', action='store_true')
goodbye_parser.set_defaults(func=greet)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
```

```bash
$ python argparse/options.py hello --greeting=Wazzup Kyle
Wazzup, Kyle!

$ python argparse/options.py hello --caps Kyle
HELLO, KYLE!

$ python argparse/options.py hello --greeting=Wazzup --caps Kyle
WAZZUP, KYLE!

$ python argparse/options.py hello --help
usage: options.py hello [-h] [--greeting GREETING] [--caps] name

positional arguments:
  name

optional arguments:
  -h, --help           show this help message and exit
  --greeting GREETING
  --caps
```

### Docopt

Once we hit the case of adding options with defaults we hit a snag with the basic implementation of commands in docopt. Let's continue just to illustrate the issue.

```python
"""Greeter.

Usage:
  basic.py hello <name> [--caps] [--greeting=<str>]
  basic.py goodbye <name> [--caps] [--greeting=<str>]
  basic.py (-h | --help)

Options:
  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Hello].

"""
from docopt import docopt


def greet(args):
    output = '{0}, {1}!'.format(args['--greeting'],
                                args['<name>'])
    if args['--caps']:
        output = output.upper()
    print(output)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    greet(arguments)
```

Now, see what happens when we run the following commands:

```bash
$ python docopt/options.py hello Kyle
Hello, Kyle!

$ python docopt/options.py goodbye Kyle
Hello, Kyle!
```

What?! Because we can only set a single default for the `--greeting` option both of our *Hello* and *Goodbye* commands now respond with **Hello, Kyle!**. In order for us to make this work we'll need to follow the [git example](https://github.com/docopt/docopt/tree/master/examples/git) docopt provides. The refactored code is shown below:

```python
"""usage: greet [--help] <command> [<args>...]

options:
  -h --help         Show this screen.

commands:
   hello       Say hello
   goodbye     Say goodbye

"""

from docopt import docopt

HELLO = """usage: basic.py hello [options] [--] [<name>]

  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Hello].
"""

GOODBYE = """usage: basic.py goodbye [options] [--] [<name>]

  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Goodbye].
"""


def greet(args):
    output = '{0}, {1}!'.format(args['--greeting'],
                                args['<name>'])
    if args['--caps']:
        output = output.upper()
    print(output)


if __name__ == '__main__':
    arguments = docopt(__doc__, options_first=True)

    if arguments['<command>'] == 'hello':
        greet(docopt(HELLO))
    elif arguments['<command>'] == 'goodbye':
        greet(docopt(GOODBYE))
    else:
        exit("{0} is not a command. See 'options.py --help'.".format(arguments['<command>']))
```

As you can see the *hello|goodbye* subcommands are now there own docstrings tied to the variables *HELLO* and *GOODBYE*. When the tool is executed it uses a new argument, *command*, to decide which to parse. Not only does this correct the problem we had with only one default, but we now have subcommand specific help messages as well.

```bash
$ python docopt/options.py --help
usage: greet [--help] <command> [<args>...]

options:
  -h --help         Show this screen.

commands:
   hello       Say hello
   goodbye     Say goodbye

$ python docopt/options.py hello --help
usage: basic.py hello [options] [--] [<name>]

  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Hello].

$ python docopt/options.py hello Kyle
Hello, Kyle!

$ python docopt/options.py goodbye Kyle
Goodbye, Kyle!
```

In addition all of our new options/flags are working:

```bash
$ python docopt/options.py hello --greeting=Wazzup Kyle
Wazzup, Kyle!

$ python docopt/options.py hello --caps Kyle
HELLO, KYLE!

$ python docopt/options.py hello --greeting=Wazzup --caps Kyle
WAZZUP, KYLE!
```

### Click

To add the *greeting* and *caps* options as we use the `@click.option` decorator. Again, since we have default greetings now we have pulled the logic out into a single function (`def greeter(**kwargs):`).

```python
import click


def greeter(**kwargs):
    output = '{0}, {1}!'.format(kwargs['greeting'],
                                kwargs['name'])
    if kwargs['caps']:
        output = output.upper()
    print(output)


@click.group()
def greet():
    pass


@greet.command()
@click.argument('name')
@click.option('--greeting', default='Hello')  # add an option with 'Hello' as the default
@click.option('--caps', is_flag=True)  # add a flag (is_flag=True)
def hello(**kwargs):
    greeter(**kwargs)  # the application logic has been refactored into a single function


@greet.command()
@click.argument('name')
@click.option('--greeting', default='Goodbye')
@click.option('--caps', is_flag=True)
def goodbye(**kwargs):
    greeter(**kwargs)

if __name__ == '__main__':
    greet()
```

```bash
$ python click/options.py hello --greeting=Wazzup Kyle
Wazzup, Kyle!

$ python click/options.py hello --greeting=Wazzup --caps Kyle
WAZZUP, KYLE!

$ python click/options.py hello --caps Kyle
HELLO, KYLE!
```

# Version Option (--version)

In this section I'll be showing how to add a `--version` argument to each of our tools. For simplicity we'll just hardcode the version number to *1.0.0*. In a production application you will want to pull this from the installed application. One way I have done this (there are many options) is with this simple process:

```python
>>> import pkg_resources
>>> pkg_resources.get_distribution("click").version  # replace click with the name of your tool
>>> '4.1'
```

A second option for determining the version would be to have automated version-bumping software change the version number defined in the file when a new version is released. This is possible with [bumpversion](https://pypi.python.org/pypi/bumpversion) but I would not recommend the approach as it's easy to get out of sync. Generally it's best practice to keep a version number in as few places as possible.

Since the implementation of adding a hard-coded version option is fairly simple I will use the `...` to denote skipped sections of the code from the last section.

### Argparse

For argparse we again need to use the `add_argument` method, this time with the `action='version'` parameter and a value for `version` passed in. We apply this method to the root parser (instead of the *hello* or *goodbye* subparsers).

```python
...
parser = argparse.ArgumentParser()
parser.add_argument('--version', action='version', version='1.0.0')
...
```

```bash
$ python argparse/version.py --version
1.0.0
```

### Docopt

In order to add `--version` to docopt we add it as an option to our primary docstring. In addition we add the `version` parameter to our first call to docopt (parsing the primary docstring).

```python
"""usage: greet [--help] <command> [<args>...]

options:
  -h --help         Show this screen.
  --version         Show the version.

commands:
   hello       Say hello
   goodbye     Say goodbye

"""

from docopt import docopt

...

if __name__ == '__main__':
    arguments = docopt(__doc__, options_first=True, version='1.0.0')
    ...
```

```bash
$ python docopt/version.py --version
1.0.0
```

### Click

Click provides us with a convince in the `@click.version_option` decorator. To add this we decorate our greet function (main `@click.group` function).

```python
...
@click.group()
@click.version_option(version='1.0.0')
def greet():
    ...
```

```bash
$ python click/version.py --version
version.py, version 1.0.0
```

# Improving Help (-h/--help)

The final step to completing our application is to improve the help documentation for each of the tools. We'll want to make sure that we can access help with both `-h` and `--help` and that each *argument* and *option* has some level of description.

### Argparse

By default argparse provides us with both `-h` and `--help` so we don't need to add anything for that. However our current help documentation for the subcommands is lacking information on what `--caps` and `--greeting` do and what the `name` argument is.

```bash
$ python argparse/version.py hello -h
usage: version.py hello [-h] [--greeting GREETING] [--caps] name

positional arguments:
  name

optional arguments:
  -h, --help           show this help message and exit
  --greeting GREETING
  --caps
```

In order to add more information we use the `help` parameter of the `add_argument` method.

```python
...

hello_parser = subparsers.add_parser('hello')
hello_parser.add_argument('name', help='name of the person to greet')
hello_parser.add_argument('--greeting', default='Hello', help='word to use for the greeting')
hello_parser.add_argument('--caps', action='store_true', help='uppercase the output')
hello_parser.set_defaults(func=greet)

goodbye_parser = subparsers.add_parser('goodbye')
goodbye_parser.add_argument('name', help='name of the person to greet')
goodbye_parser.add_argument('--greeting', default='Hello', help='word to use for the greeting')
goodbye_parser.add_argument('--caps', action='store_true', help='uppercase the output')

...
```

Now when we provide the help flag we get a much more complete result:

```bash
$ python argparse/help.py hello -h
usage: help.py hello [-h] [--greeting GREETING] [--caps] name

positional arguments:
  name                 name of the person to greet

optional arguments:
  -h, --help           show this help message and exit
  --greeting GREETING  word to use for the greeting
  --caps               uppercase the output
```

### Docopt

This section is where docopt gets it's chance to shine. Because we wrote the documentation as the definition of the command-line interface itself we already have a complete help. In addition `-h` and `--help` are already provided.

```bash
$ python docopt/help.py hello -h
usage: basic.py hello [options] [--] [<name>]

  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Hello].
```

### Click

Adding help documentation in click is very similar to argparse. We need to add the `help` parameter to all of our `@click.option` decorators.

```python
...

@greet.command()
@click.argument('name')
@click.option('--greeting', default='Hello', help='word to use for the greeting')
@click.option('--caps', is_flag=True, help='uppercase the output')
def hello(**kwargs):
    greeter(**kwargs)


@greet.command()
@click.argument('name')
@click.option('--greeting', default='Goodbye', help='word to use for the greeting')
@click.option('--caps', is_flag=True, help='uppercase the output')
def goodbye(**kwargs):
    greeter(**kwargs)

...
```

However, click **DOES NOT** provide us `-h` by default. We need to use the `context_settings` parameter to override the default `help_option_names`.

```python
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

...

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def greet():
    pass
```

Now the click help documentation is complete.

```bash
$ python click/help.py hello -h
Usage: help.py hello [OPTIONS] NAME

Options:
  --greeting TEXT  word to use for the greeting
  --caps           uppercase the output
  -h, --help       Show this message and exit.
```

With that we have completed the construction of the command-line application we set out to build. Before we conclude let's take a look at another possible option.

# Invoke

Can we use [invoke](https://invoke.readthedocs.org/en/latest/), a simple task running library, to build the greeter command-line application? Let's find out!

To start let's begin with the simplest version of the greeter:

*tasks.py*
```python
from invoke import task


@task
def hello(name):
    print('Hello, {0}!'. format(name))


@task
def goodbye(name):
    print('Goodbye, {0}!'.format(name))
```

With this very simple file we get a two tasks, and a very minimal help. From the same directory as *tasks.py* we get the following results:

```bash
$ invoke -l
Available tasks:

  goodbye
  hello

$ invoke hello Kyle
Hello, Kyle!

$ invoke goodbye Kyle
Goodbye, Kyle!
```

Now let's add in our options/flags `--greeting` and `--caps`. In addition we can pull out the greet logic into it's own function just as we did with the other tools.

```python
from invoke import task


def greet(name, greeting, caps):
    output = '{0}, {1}!'.format(greeting, name)
    if caps:
        output = output.upper()
    print(output)


@task
def hello(name, greeting='Hello', caps=False):
    greet(name, greeting, caps)


@task
def goodbye(name, greeting='Goodbye', caps=False):
    greet(name, greeting, caps)
```

Now we actually have the complete interface we designated in the beginning!

```bash
$ invoke hello Kyle
Hello, Kyle!

$ invoke hello --greeting=Wazzup Kyle
Wazzup, Kyle!

$ invoke hello --greeting=Wazzup --caps Kyle
WAZZUP, KYLE!

$ invoke hello --caps Kyle
HELLO, KYLE!
```

### Help Documentation

In order to compete with argparse, docopt, and click we'll also need to be able to add complete help documentation. Luckily this is also available in *invoke* by using the `help` parameter of the `@task` decorator and adding docstrings to the decorated functions.

```python
...

HELP = {
    'name': 'name of the person to greet',
    'greeting': 'word to use for the greeting',
    'caps': 'uppercase the output'
}


@task(help=HELP)
def hello(name, greeting='Hello', caps=False):
    """
    Say hello.
    """
    greet(name, greeting, caps)


@task(help=HELP)
def goodbye(name, greeting='Goodbye', caps=False):
    """
    Say goodbye.
    """
    greet(name, greeting, caps)

```

```bash
$ invoke --help hello
Usage: inv[oke] [--core-opts] hello [--options] [other tasks here ...]

Docstring:
  Say hello.

Options:
  -c, --caps                     uppercase the output
  -g STRING, --greeting=STRING   word to use for the greeting
  -n STRING, --name=STRING       name of the person to greet
  -v, --version
```

### Version Option

Implementing a `--version` option is not quite as simple and comes with a caveat. The basics are that we will add `version=False` as an option to each of the tasks that calls a new `print_version` function if True. In order to make this work we cannot have any positional arguments without defaults or we get:

```bash
$ invoke hello --version
'hello' did not receive all required positional arguments!
```

Also note that we are calling `--version` on our commands *hello* and *goodbye* because *invoke* itself has a version command:

```bash
$ invoke --version
Invoke 0.10.1
```

The completed implementation of a version command follows:

```python
...

def print_version():
    print('1.0.0')
    exit(0)


@task(help=HELP)
def hello(name='', greeting='Hello', caps=False, version=False):
    """
    Say hello.
    """
    if version:
        print_version()
    greet(name, greeting, caps)

...
```

Now we are able to ask invoke for the version of our tool:

```bash
$ invoke hello --version
1.0.0
```

# Conclusion

To review let's take a look at the final version of each of the tools we created.

### Argparse

```python
import argparse


def greet(args):
    output = '{0}, {1}!'.format(args.greeting, args.name)
    if args.caps:
        output = output.upper()
    print(output)

parser = argparse.ArgumentParser()
parser.add_argument('--version', action='version', version='1.0.0')
subparsers = parser.add_subparsers()

hello_parser = subparsers.add_parser('hello')
hello_parser.add_argument('name', help='name of the person to greet')
hello_parser.add_argument('--greeting', default='Hello', help='word to use for the greeting')
hello_parser.add_argument('--caps', action='store_true', help='uppercase the output')
hello_parser.set_defaults(func=greet)

goodbye_parser = subparsers.add_parser('goodbye')
goodbye_parser.add_argument('name', help='name of the person to greet')
goodbye_parser.add_argument('--greeting', default='Hello', help='word to use for the greeting')
goodbye_parser.add_argument('--caps', action='store_true', help='uppercase the output')
goodbye_parser.set_defaults(func=greet)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
```

### Docopt

```python
"""usage: greet [--help] <command> [<args>...]

options:
  -h --help         Show this screen.
  --version         Show the version.

commands:
   hello       Say hello
   goodbye     Say goodbye

"""

from docopt import docopt

HELLO = """usage: basic.py hello [options] [--] [<name>]

  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Hello].
"""

GOODBYE = """usage: basic.py goodbye [options] [--] [<name>]

  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Goodbye].
"""


def greet(args):
    output = '{0}, {1}!'.format(args['--greeting'],
                                args['<name>'])
    if args['--caps']:
        output = output.upper()
    print(output)


if __name__ == '__main__':
    arguments = docopt(__doc__, options_first=True, version='1.0.0')

    if arguments['<command>'] == 'hello':
        greet(docopt(HELLO))
    elif arguments['<command>'] == 'goodbye':
        greet(docopt(GOODBYE))
    else:
        exit("{0} is not a command. See 'options.py --help'.".format(arguments['<command>']))
```

### Click

```python
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def greeter(**kwargs):
    output = '{0}, {1}!'.format(kwargs['greeting'],
                                kwargs['name'])
    if kwargs['caps']:
        output = output.upper()
    print(output)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def greet():
    pass


@greet.command()
@click.argument('name')
@click.option('--greeting', default='Hello', help='word to use for the greeting')
@click.option('--caps', is_flag=True, help='uppercase the output')
def hello(**kwargs):
    greeter(**kwargs)


@greet.command()
@click.argument('name')
@click.option('--greeting', default='Goodbye', help='word to use for the greeting')
@click.option('--caps', is_flag=True, help='uppercase the output')
def goodbye(**kwargs):
    greeter(**kwargs)

if __name__ == '__main__':
    greet()
```

### Invoke

```python
from invoke import task


def greet(name, greeting, caps):
    output = '{0}, {1}!'.format(greeting, name)
    if caps:
        output = output.upper()
    print(output)


HELP = {
    'name': 'name of the person to greet',
    'greeting': 'word to use for the greeting',
    'caps': 'uppercase the output'
}


def print_version():
    print('1.0.0')
    exit(0)


@task(help=HELP)
def hello(name='', greeting='Hello', caps=False, version=False):
    """
    Say hello.
    """
    if version:
        print_version()
    greet(name, greeting, caps)


@task(help=HELP)
def goodbye(name='', greeting='Goodbye', caps=False, version=False):
    """
    Say goodbye.
    """
    if version:
        print_version()
    greet(name, greeting, caps)
```

Now, to get this out of the way my personal go-to library is click. I have been using it on large, multi-command, complex interfaces for the last year. (Credit goes to [@kwbeam](https://twitter.com/kwbeam) for introducing me to click). I prefer the decorator approach and think it lends a very clean, composable interface. That being said, let's evaluate each option fairly.

### arparse

**Arparse is the standard library (included with Python) for creating command-line utilities.** For that fact alone it is arguably the most used of the tools examined here. Argparse is also very simple to use as lots of *magic* (implicit work that happens behind the scenes) is used to construct the interface. For example both arguments and options are defined using the `add_arguments` method and argparse figures out which is which behind the scenes.

### docopt

**If you think writing documentation is great, docopt is for you!** In addition docopt has implementations for [many other languages](https://github.com/docopt) meaning you can learn one library and use it across many languages. The downside of docopt is that it is very structured in the way you have to define your command-line interface. (Some might say this is a good thing!)

### click

I've already said that I really like click and have been using it in production for over a year. **I encourage you to read the very complete [Why Click?](http://click.pocoo.org/4/why/) documentation.** In fact that documentation is what inspired this blog post! The decorator style implementation of click is very simple to use and since you are decorating the function you want executed it makes it very easy to read the code and figure out what is going to be executed. In addition click supports advanced features like callbacks, command nesting, and more. Click is based on a fork of the now deprecated [optparse](https://docs.python.org/2/library/optparse.html) library.

### invoke

**Invoke surprised me in this comparison.** I thought that a library designed for task execution might not be able to easily match full command-line libraries but it did! That being said I would not recommend using it for this type of work as you will certainly run into limitations for anything more complex than the example presented here.

# Bonus: Packaging Command-Line Applications

Since not everyone is packaging up there python source with [setuptools](https://pypi.python.org/pypi/setuptools) (or other solutions) I decided not to make this a core component of the article. In addition I don't want to cover *packaging* as a complete topic. If you want to learn more about packaging with setuptools [go here](https://packaging.python.org/en/latest/) or with conda [go here](http://conda.pydata.org/docs/building/build.html) or you can read my previous [blog post](http://kylepurdon.com/blog/packaging-python-basics-with-continuum-analytics-conda.html) on conda packaging. **What I will cover here is how to use the entry_points option to make a command-line application an executable command on install**.

### Entry Point Basics

An [entry_point](https://packaging.python.org/en/latest/distributing.html?highlight=entry_points#entry-points) is essentially a map to a single function in your code that will be given a command on your systems PATH. An entry_point has the form: `command = package.module:function`

The best way to explain this is to just look at our *click* example and add an entry point.

### Packaging Click Commands

Click makes packaging simple as by default we are calling a single function when we execute our program.

```python
if __name__ == '__main__':
    greet()
```

In addition to the rest of the *setup.py* (not covered here) we would add the following to create an entry_point for our click application.

Assuming the following directory structure:

```
greeter/
├── greet
│   ├── __init__.py
│   └── cli.py       <-- the same as our final.py
└── setup.py
```

We will create the following entry_point:

```python
entry_points={
    'console_scripts': [
        'greet=greet.cli:greet',  # command=package.module:function
    ],
},
```

When a user installs the package created with this entry_point setuptools will create the following executable script (called greet) and place it on the PATH of the users system.

```python
#!/usr/bin/python
if __name__ == '__main__':
    import sys
    from greet.cli import greet

    sys.exit(greet())
```

After installation the user will now be able to run the following:

```bash
$ greet --help
Usage: greet [OPTIONS] COMMAND [ARGS]...

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  goodbye
  hello
```

### Packaging Argparse Commands

The only thing we need to do differently from click is to pull all of the application initialization into a single function that we can call in our entry_point.

This:

```python
if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
```

Becomes:

```python

def greet():
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    greet()

```

Now we can use the same pattern for the entry_point we defined for click.

### Packaging Docopt Commands

Packaging docopt commands requires the same process as argparse.

This:

```python
if __name__ == '__main__':
    arguments = docopt(__doc__, options_first=True, version='1.0.0')

    if arguments['<command>'] == 'hello':
        greet(docopt(HELLO))
    elif arguments['<command>'] == 'goodbye':
        greet(docopt(GOODBYE))
    else:
        exit("{0} is not a command. See 'options.py --help'.".format(arguments['<command>']))
```

Becomes:

```python
def greet():
    arguments = docopt(__doc__, options_first=True, version='1.0.0')

    if arguments['<command>'] == 'hello':
        greet(docopt(HELLO))
    elif arguments['<command>'] == 'goodbye':
        greet(docopt(GOODBYE))
    else:
        exit("{0} is not a command. See 'options.py --help'.".format(arguments['<command>']))

if __name__ == '__main__':
    greet()
```
