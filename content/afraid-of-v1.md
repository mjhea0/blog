Title: Why Are Developers Afraid of 1.0.0?
Date: 2014-11-11 20:53
Category: Software
Tags: development, SemVer, version
Summary: Developers should release v1.0.0 as soon as possible. Let me explain why.

I'm a big fan of releasing version 1.0.0 as soon as I possibly can. Let me tell you why I think this is the responsible thing to do as an open source software developer.

# What does v0.#.# mean?

I recently stumbled across the [Semantic Visioning (SemVer)](http://SemVer.org/) definition of pre-1.0.0:

> Major version zero (0.y.z) is for initial development. Anything may change at any time. The public API should not be considered stable.

Pretty simple. As long as something is v0.#.# anything goes. The developer can change anything, break everything, and anybody using the tool at this point is at the mercy of the developer.

# What does v1.#.# mean?

According to SemVer v1.#.#+

> Version 1.0.0 defines the public API. The way in which the version number is incremented after this release is dependent on this public API and how it changes.

This basally means that any subsequent changes in version mean something. I wont repeat the SemVer specification here but just point out that after a release of v1.0.0 any changes not following the SemVer spec should be considered a failure on the part of the developer.

# When Do I Release v1.0.0?

## AS SOON AS I POSSIBLY CAN.

![The Flash]({filename}/images/the-flash.gif)

At the point in any of my projects where I have a working, tested, usable product that solves the issue I set out to solve I release v1.0.0. By doing this I'm telling users that I will not break this code without an increment to the appropriate version numbers. This should allow them to use my software in a manor that allows me to push usable bug fixes and minor improvements without breaking there dependent software.

# Shouldn't I be Afraid of v1.0.0 Failing?

## NO!

![Treadmill Fail]({filename}/images/treadmill-fail.gif)

Sure it might hurt and I might look silly but that's fine. I can release all the patch versions (1.0.#) that I need to do the fixes. All v1.0.0 says is that I guarantee as a developer that patch, minor, and major versions mean something.

# An Example

Lets say there exists two Python modules (Foo and Bar).

Foo has released version 1.0.0
Bar has released version 0.1.0

I'm writing a new Python modules called Baz that uses both Foo and Bar. My requirements file will look like this:

    :::python
    Foo >=1.0.0,<2
    Bar == 0.1.0

That's right Bar I don't trust you! And why should I? According to SemVer your version of 0.1.0 tells me that you are ready and willing to rip everything out from under me. So, no I wont take your new version 0.2.0 because it could, by definition, break everything I have worked so hard for in Baz.

On the other side Foo I will let you upgrade all the way until you release 2.0.0. That's right! A bug fix in 1.0.1, a new minor feature in 1.1.1, I'll take it! You, Foo, have committed to releasing stable changes and for that I commend you.

# Conclusion

v1.0.0 does not mean anything other than you, the developer, are committing to stable, SemVer compatible releases. So why not get there as fast as you can and leave your users with a little peace of mind?

[More To Chew On](https://github.com/dominictarr/semver-ftw/issues/2)
