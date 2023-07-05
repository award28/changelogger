<!--
  !! THIS FILE IS MAINTAINED USING CHANGELOGGER.
  !! MODIFICATION OF THIS FILE BY HAND MAY BREAK USAGE WITH CHANGELOGGER.

  Learn more: https://github.com/award28/changelogger
-->
# Changelog
*All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
The [Changelogger tool](https://pypi.org/project/changelogged) is used for automated management of this file.

<!-- BEGIN RELEASE NOTES -->
### [Unreleased]

### [0.13.0] - 2023-07-05

#### Added
- The `force` command, allowing users to override the next version of their release.

### [0.12.0] - 2023-03-18

#### Added
- The `template_dir` option in the `.changelogger.yml` config file. This option allows users to override the default template location.
- Jinja templates now have full funcitonality, as the BaseLoader has been deprecated in favor of the FileSystemLoader.
- Exception information is now provided to help understand the cause of an upgrade exception.

#### Changed
- The `jinja_rel_path` versioned file key has been replaced with the `template` key.

### [0.11.4] - 2023-03-17

#### Added
- Precommit hook to validate versioned files

### [0.11.3] - 2023-03-06

#### Fixed
- Removed project metadata from settings.

### [0.11.2] - 2023-03-06

#### Fixed
- Removed dependency on "pyproject.toml", which doesn't get packaged with changelogger.

### [0.11.1] - 2023-03-06

#### Added
- Users can now have their `.changelogger.yml` file in `.changelogger/` or `.github/` in addition to the root directory.

### [0.11.0] - 2023-03-05

#### Added
- Jinja templates now have access to the `match` variable. This allows access to match groups.

### [0.10.2] - 2023-03-05

#### Changed
- Moved dev dependencies into separate group, reducing install size.

### [0.10.1] - 2023-03-05

#### Changed
- `SemVerType` to `BumpTarget`.

### [0.10.0] - 2023-03-05

#### Added
- Alias commands `up` and `ch` for `upgrade` and `check`, respectively.
- Add the `--file` option to the check command, allowing users to specify which files to check.
- Added progress feedback as versioned files are checked.

### [0.9.1] - 2023-03-05

#### Changed
- The `check` command will now validate all versioned files, not just the changelog file.

### [0.9.0] - 2023-03-04

#### Changed
- Added `cl` as an alias for `changelogger`.
- Moved all commands under the top level `changelogger` app.
- Removed the `unreleased content` and `manage content` commands in favor of `notes`.
- Changed `num_versions` flag with the `start` and `offset` flags in the `versions` command.

#### Removed
- Removed the `manage` and `unreleased` sub apps in favor of top level commands.

#### Fixed
- Release notes with dashes resulted in a single note getting split.

### [0.8.0] - 2023-03-04

#### Added
- Added the `init` command, which will perform guided initialization on new projects.
- Added the `-v` or `--version` flag to get the installed changelogger version.

#### Changed
- The git context now contains the first commit hash.

### [0.7.0] - 2023-03-01

#### Added
- Created the `manage versions` command

### [0.6.0] - 2023-02-08

#### Changed
- Pattern recognition of partitioned sections within the changelog file.
- Semantic Version strings with old semver API to use the new semver.VersionInfo class.

#### Removed
- The LINKS section of the changelog file.

#### Fixed
- Incomplete semantic version parsing. Prerelease and Build sections are now allowed.

### [0.5.0] - 2023-02-04

#### Added
- Continuous Delivery Workflow
- Continuous Deployment Workflow

### [0.4.0] - 2023-02-04

#### Added
- Docstrings for different subcommands.

#### Changed
- README installation and usage sections.

### [0.3.4] - 2023-02-04

#### Changed
- Moved assets dir into changelogger so it's included in the wheel.

### [0.3.3] - 2023-02-04

#### Fixed
- `assets` directory not included with build.

### [0.3.2] - 2023-02-04

#### Added
- Configuration information to pyproject.toml.

### [0.3.1] - 2023-02-04

#### Changed
- Project description to headline.

### [0.3.0] - 2023-02-04

#### Added
- Documentation on Changelogger configuration syntax.

### [0.2.0] - 2023-02-03

#### Changed
- Add pre-commit and formatted all files.

### [0.1.0] - 2023-02-03

#### Added
- `manage` command, with management subcommands.
- `manage content`, which lists the content for the specified version.
- `manage check`, which checks the versioned files are parsable.
- `manage ugprade`, which performs the specified semantic version upgrade across the specified versioned files.
- `unreleased` command, with unreleased subcommands.
- `unreleased content`, which lists the unreleased content.
- `unreleased add`, which allows inline or prompted adding of unreleased changes.
<!-- END RELEASE NOTES -->
<!-- BEGIN LINKS -->
[Unreleased]: https://github.com/award28/changelogger/compare/0.13.0...HEAD
[0.13.0]: https://github.com/award28/changelogger/compare/0.12.0...0.13.0
[0.12.0]: https://github.com/award28/changelogger/compare/0.11.4...0.12.0
[0.11.4]: https://github.com/award28/changelogger/compare/0.11.3...0.11.4
[0.11.3]: https://github.com/award28/changelogger/compare/0.11.2...0.11.3
[0.11.2]: https://github.com/award28/changelogger/compare/0.11.1...0.11.2
[0.11.1]: https://github.com/award28/changelogger/compare/0.11.0...0.11.1
[0.11.0]: https://github.com/award28/changelogger/compare/0.10.2...0.11.0
[0.10.2]: https://github.com/award28/changelogger/compare/0.10.1...0.10.2
[0.10.1]: https://github.com/award28/changelogger/compare/0.10.0...0.10.1
[0.10.0]: https://github.com/award28/changelogger/compare/0.9.1...0.10.0
[0.9.1]: https://github.com/award28/changelogger/compare/0.9.0...0.9.1
[0.9.0]: https://github.com/award28/changelogger/compare/0.8.0...0.9.0
[0.8.0]: https://github.com/award28/changelogger/compare/0.7.0...0.8.0
[0.7.0]: https://github.com/award28/changelogger/compare/0.6.0...0.7.0
[0.6.0]: https://github.com/award28/changelogger/compare/0.5.0...0.6.0
[0.5.0]: https://github.com/award28/changelogger/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/award28/changelogger/compare/0.3.4...0.4.0
[0.3.4]: https://github.com/award28/changelogger/compare/0.3.3...0.3.4
[0.3.3]: https://github.com/award28/changelogger/compare/0.3.2...0.3.3
[0.3.2]: https://github.com/award28/changelogger/compare/0.3.1...0.3.2
[0.3.1]: https://github.com/award28/changelogger/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/award28/changelogger/compare/0.2.0...0.3.0
[0.2.1]: https://github.com/award28/changelogger/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/award28/changelogger/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/award28/changelogger/compare/b89ca3a520...0.1.0
<!-- END LINKS -->
