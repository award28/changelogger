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
[Unreleased]: https://github.com/award28/changelogger/compare/0.8.0...HEAD
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
