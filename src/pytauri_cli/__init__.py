# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "copier>=9.7.1",
# ]
# ///

import argparse

import copier


def build():
    print("Building will come at a later date!")


def create():
    copier.run_copy("https://github.com/ISOR3X/create-pytauri", ".")


def main():
    parser = argparse.ArgumentParser(description="My CLI tool with multiple commands")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("build", help="Build the current project")

    subparsers.add_parser("create", help="Create a new project")

    args = parser.parse_args()

    # Show help if no command is given
    if not args.command:
        parser.print_help()
        return

    if args.command == "build":
        build()
    elif args.command == "create":
        create()


if __name__ == "__main__":
    main()
