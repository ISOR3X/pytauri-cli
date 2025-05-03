# Pytauri-CLI

A command-line interface tool for building and creating PyTauri projects.

## Features

- **Create**: Creates a new PyTauri project using a template.
- **Build**: Work in progress.
- **Embed python**: Downloads the appropriate Python standalone build
  from [python-build-standalone](https://github.com/astral-sh/python-build-standalone/releases) based on the Python
  version specified in your project's `.python-version` file.

## Installation

```bash
uv tool install git+https://github.com/ISOR3X/pytauri-cli
pytauri-cli
```

## Usage

```bash
# Show help
pytauri-cli

# Create a new project
pytauri-cli create
```

The following commands must be run from the project root. 
```bash
# Build the current project
pytauri-cli build

# Install standalone python for building 
pytauri-cli embed-python
```
