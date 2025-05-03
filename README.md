# Pytauri-CLI

A command-line interface tool for building and creating PyTauri projects.

## Features

- **Embed python**: Downloads the appropriate Python standalone build
  from [python-build-standalone](https://github.com/astral-sh/python-build-standalone/releases) based on the Python
  version specified in your project's `.python-version` file.
- **Create**: Creates a new PyTauri project using a template.

## Installation

```bash
pip install pytauri-cli
```

## Usage

```bash
# Show help
pytauri-cli

# Build the current project
pytauri-cli build

# Create a new project
pytauri-cli create

```
