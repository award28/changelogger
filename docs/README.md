# Changelogger

[![Continuous Deployment](https://github.com/award28/changelogger/actions/workflows/continuous_deployment.yml/badge.svg)](https://github.com/award28/changelogger/actions/workflows/continuous_deployment.yml)
[![Continuous Integration](https://github.com/award28/changelogger/actions/workflows/continuous_integration.yml/badge.svg)](https://github.com/award28/changelogger/actions/workflows/continuous_integration.yml)
[![codecov](https://codecov.io/gh/award28/changelogger/branch/main/graph/badge.svg?token=M0I9MA4ZNW)](https://codecov.io/gh/award28/changelogger)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![PyPI - Link](https://img.shields.io/pypi/v/changelogged?color=%2334D058&label=pypi%20package)](https://pypi.org/project/changelogged/)
[![Downloads](https://static.pepy.tech/badge/changelogged/month)](https://pepy.tech/project/changelogged)
[![PyPI - License](https://img.shields.io/pypi/l/changelogged)](https://pypi.org/project/changelogged/)
[![Github Project - Changelogger](https://img.shields.io/badge/Project-Changelogger-blue?logo=github)](https://github.com/users/award28/projects/2)

Automated management of your CHANGELOG.md and other versioned files, following
the principles of [Keep a Changelog](https://keepachangelog.com) and
[Semantic Versioning](https://semver.org).


This project uses [Jinja](https://jinja.palletsprojects.com/) for simple yet
powerful templating and regular expressions for pattern matching. To learn more
about this, checkout the [`.changelogger.yml` Syntax](#changelogger-syntax)
section. The next section will go over how this works, and you can use
changelogger to help manage your versioned files.

## Motivation

With any software that is versioned, it is typically necessary to include the
version number in more than one file. In addition to the version changes, there
is also a need for certain projects to include their changelog contents in
multiple locations. **Maintaining these files by hand is tedious and error prone.**

By automating the upgrade of each of these files, we can reduce the risk of
out-of-sync files, validate these changes in our CI/CD pipelines, and save
ourselves some time.

## Installation

```
pip install changelogged
```

## Usage

Run `changelog [SUBCOMMANDS] --help` to understand the usage for any command.

```
❯ changelogger --help

 Usage: changelogger [OPTIONS] COMMAND [ARGS]...

 Automated management of your CHANGELOG.md and other versioned files, following the principles
 of Keep a Changelog and Semantic Versioning.

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                       │
│ --show-completion             Show completion for the current shell, to copy it or customize  │
│                               the installation.                                               │
│ --help                        Show this message and exit.                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────╮
│ manage      Management commands for changelog and other versioned files, as specified in the  │
│             changelogger config file.                                                         │
│ unreleased  Commands for the unreleased section of the changelog.                             │
╰───────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Introduction

The `.changelogger.yml` configuration file allows you to customize what files
are versioned and maintained by Changelogger. Let's say you have a `pyproject.toml`
file which is versioned in addition to your `CHANGELOG.md` file. You would add the
`.changelogger.yml` file to the root of your project, with the following configuration.

```yml
versioned_files:
  - rel_path: "pyproject.toml"
    pattern: 'version = "{{ old_version }}"'
    jinja: 'version = "{{ new_version }}"'
```

In fact, that's the exact configuration used by this project! Let's breakdown
what each line means.

##### `versioned_files:`
This line lets Changelogger know that you have a list of files you would like
Changelogger to maintain. This list can be one or more, but if it doesn't exist,
Changelogger will only manage the `CHANGELOG.md` file.

##### `- rel_path: "pyproject.toml"`
The `-` is the start of a new versioned file section; it's unimportant that this
is on the `rel_path` field, but is important that this section is separated from
other versioned files, and that all other related fields are below the `-`'d field.

The `rel_path` lets Changelogger know that there is a file in the path, relative
to the `.changelogger.yml` file, that you would like Changelogger to maintain the
version in said file. In this case, the `pyproject.toml` file is at the root of
this project, so all we need is that name.

**Note** that you can list a file multiple times within the configuration file;
this can reduce the complexity of pattern matching while keeping all versioned
sections of a file in-sync.

##### `pattern: 'version = "{{ old_version }}"'`
The `pattern` field lets Changelogger know how to find the versioned segment in
this file. The `pattern` field supports Python's flavor of regular expressions,
as well as the use of Jinja with pre-determined variables. More on these can be
found [below](#jinja-variables). The combination of these two allow for a strong
yet simple pattern matching interface.

##### `jinja: 'version = "{{ new_version }}"'`
The `jinja` field is used as a jinja template to replace the matched pattern.
The same rendered variables which are available for the `pattern` field can
be utilized by this field.

Further, using standard yaml, you can create a multiline jinja to replace the
matched pattern. For instance, if our release also came with a release date,
we could use the following `.changelogger.yml` file to manage the required
changes.

```yml
versioned_files:
  - rel_path: "pyproject.toml"
    pattern: 'version = "{{ old_version }}"\nrelease_date = "\d+-\d+-\d+"'
    jinja: |
      version = "{{ new_version }}"
      release_date = "{{ today }}"
```

While this approach is great for a simple use case like the one above, it
falls short for more complex jinja templates. To help deal with this
limitation, the `template` field can be used. This allows us to move
our code to a jinja file and reference said file relative to the
`.changelogger.yml` file.

*.changelogger.yml*
```yml
versioned_files:
  - rel_path: "pyproject.toml"
    pattern: 'version = "{{ old_version }}"\nrelease_date = "\d+-\d+-\d+"'
    jinja: |
      version = "{{ new_version }}"
      release_date = "{{ today }}"
```

*.pyproject.toml.jinja2*
```jinja
version = "{{ new_version }}"
release_date = "{{ today }}"
```

Now we have our multiline Jinja outside of our configuration file and, with
the right IDE support, we can get Jinja syntax highlighting. Examples of Jinja
templates used by this project can be found in the [`templates`](../changelogger/templates)
directory.

---

With that, we now understand how the Changelogger configuration file works.
Now all you need to do is let Changelogger do the heavy lifting for any
upgrade with the `manage upgrade`. Make sure to explore what commands are
available by using the `changelogger --help` command!

## `.changelogger.yml` Syntax

This section reviews all available configuration sections of the Changelogger
configuration file. For a more streamlined introduction, review the
[introduction](#introduction) section. The
[JSON Schema Core](https://json-schema.org/latest/json-schema-core.html)
compliant schema can be found in the
[config.schema.json](../config.schema.json) file.


The `changelog` field is used for managing and updating the `CHANGELOG.md`.
If your project doesn't follow the standard changelog file format prescribed
by Changelogger, you will need to upate this section. **Note** that the changelog
section requires both the overview and links sub sections be provided. However,
if there are other versioned changes you would like to require Changelogger manage
on your behalf, you can add those to the `versioned_files` section.

*Example File with All Required Fields*
```yml
changelog:
  rel_path: "CHANGELOG.md"
  overview:
    pattern: '### \[Unreleased\]([\s\S]*)### \[{{ old_version }}]'
    template: ./templates/.cl.overview.jinja2
  links:
    pattern: '\[Unreleased\]:.*\n'
    template: ./templates/.cl.links.jinja2

versioned_files:
  - rel_path: "pyproject.toml"
    pattern: 'version = "{{ old_version }}"'
    jinja: 'version = "{{ new_version }}"'
```


# Jinja Variables
The following is an overview of the jinja variables available in the `pattern`
field and the `jinja` templating for managed replacement.

## `new_version`: string

The new version after the requested semantic version bump type has been applied.

### Example

*.some.jinja2*
```jinja
New Version: {{ new_version }}
```

## `old_version`: string

The current version of the project, which the requested semantic version bump type
will be applied on.

### Example

*.some.jinja2*
```jinja
Old Version: {{ old_version }}
```

## `today`: datetime.date

A [datetime.date](https://docs.python.org/3/library/datetime.html#date-objects)
object with today's date.

### Example

*.some.jinja2*
```jinja
Todays Date: {{ today }}
```

## `sections`: dict[str, list[str]]

A map from each section of the Keep a Changelog standard to the notes included for
that section.

### Example

*.some.jinja2*
```jinja
{% for name, notes in sections.items() -%}
{% if notes -%}
#### {{ name.title() }}
{% for note in notes -%}
- {{ note }}
{% endfor %}
{% endif %}

{%- endfor -%}
```
## `context`: dict[str, Any]

User specified context in the `.changelogger.yml` configuration file, available in
both the pattern and jinja through dot notation.

### Example

*.changelogger.yml*
```yml
versioned_files:
  - rel_path: "pyproject.toml"
    pattern: 'version = "{{ old_version }}"'
    template: '.pyproject.toml.jinja2'
    context:
      git:
        org: award28
        repo: changelogger
```

*.pyproject.toml.jinja2*
```jinja
org: {{ context.git.org }}
repo: {{ context.git.repo }}
```
