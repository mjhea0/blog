title: Comparing Python Command-Line Utility Libraries.
date:
category: Software, Tools
tags: python, development
summary: A comparison of Python command-line utility libraries (argparse, docopt, and click).
status: draft

Some Introduction Here.

# Command Line Example

The command line tool that we are creating will have the following interface:

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

This simple command line tool breaks down into a few things the library we choose will need to implement:

1. Commands (hello, goodbye)
2. Arguments (name)
3. Flags/Options (--greeting, --caps)

In addition automated help messages are important, and to throw a wrench in lets say we also want a `-v/--version` option that will print the version number and quit. As you would expect argparse, docopt, and click implement all of these features (as any simple command line library would). This means that this comparison is going to break down into a stylistic preference. I'll leave my personal preferences for the end!

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

With this we now have two commands (hello, goodbye) and a built-in help message. Notice that the help message **DOES NOT** change when run as an option on the command hello. In addition we do not actually need to explecitly specify the `commands.py -h | --help` or the *Options* section to get a help command. However, if we do not specify them they will not show up in the output help message as options.

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

Even at this point you can see that we have very different approaches to constructing a basic command line tool. Next let's add the *NAME* argument, and the logic to print the result to each tool.

# Arguments

In this section I will be adding new logic to the same code shown in the previous section. I'll add comments to new lines stating there purpose. Arguments (a.k.a positional arguments) are required inputs to a command line tool. In this case we are adding a required "name" argument so that the tool can greet a specific person.

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

In order to add an option we simply add a `<name>` to the docstring. The `<>` are used to designame a positional argument. In order to execute the correct logic we must check if the command (treated as an argument) is True at runtime `if arguments['hello']:`, then dispatching to the correct functions.

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

In order to add an argument to a click command we simply use the `@click.argument` decorator. In this case we are just passing the argument name, but there are [many more options](http://click.pocoo.org/4/arguments/) some of which we'll use later. With click command/subcommand dispatching is native. Since we are just decorating the logic (function) with the argument we dont need to do anything to set/dispatch to the correct logic.

```python
import click


@click.group()
def greet():
    pass


@greet.command()
@click.argument('name')  # add the name agrument
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

In this section I will again be adding new logic to the same code shown in the previous section. I'll add comments to new lines stating there purpose. Options are non-required inputs that can be given to alter the execution of a command-line tool. Flags are a subset of options that are True/False. For example: `--foo=bar` will pass *bar* as the value for the *foo* option, `--baz` (if defined as a flag) will pass the value of True is the option is given, or False if not.

For this example we are going to add the `--greeting=[greeting]` option, and the `--caps` flag. The *greeting* optiona will have default values of "Hello" and "Goodbye" (for hello, and goodbye commands) and allow the user to pass in a custom greeting. For example given `--greeting=Wazzup` the tool will respond with *Wazzup, [name]!*. The `--caps` flag will uppercase the entire response if given. For example given `--caps` the tool will respond with *HELLO, [NAME]!*.

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

Once we hit the case of adding options with defaults we hit a snag with the basic implmentation of commands in docopt. Let's continue just to illistrate the issue.

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

As you can see the *hello|goodbye* subcommands are now there own doctrings ties to variables *HELLO* and *GOODBYE*. When the tool is executed it uses a new argument *command* to decide which to parse. Not only does this correct the problem we had with only one default, but we now have subcommand specific help messages as well.

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

Adding the *greeting* and *caps* option to click is very simple, as we just use the `@click.option` decorator for both. Again, since we have default greetings now we have refactored the logic out into a single function.

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

# Version Option (-v/--version)

### Argparse

```python
```

```bash
```

### Docopt

```python
```

```bash
```

### Click

```python

```

```bash
```


# Improving Help (-h/--help)

### Argparse

```python
```

```bash
```

### Docopt

```python
```

```bash
```

### Click

```python

```

```bash
```
