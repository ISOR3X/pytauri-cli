# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "copier>=9.7.1",
# ]
# ///

import argparse

import copier

from pytauri_cli.build import build_project, embed_python


def create():
    copier.run_copy("https://github.com/ISOR3X/create-pytauri", ".")


def main():
    parser = argparse.ArgumentParser(description="PyTauri CLI tool with multiple commands")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("build", help="Build the current project")
    subparsers.add_parser("create", help="Create a new project")
    subparsers.add_parser("embed-python", help="Install a standalone python build for your project.")

    args = parser.parse_args()

    # Show help if no command is given
    if not args.command:
        parser.print_help()
        return

    if args.command == "build":
        build_project()
    elif args.command == "create":
        create()
    elif args.command == "embed-python":
        embed_python()


if __name__ == "__main__":
    main()
