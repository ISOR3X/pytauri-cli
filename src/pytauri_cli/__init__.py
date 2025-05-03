# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

import argparse
import subprocess

def build():
    print("Running build steps...")
    subprocess.run(["echo", "Step 1: Compiling"])
    subprocess.run(["echo", "Step 2: Packaging"])
    print("Build complete!")

def create():
    print("Running create steps...")
    subprocess.run(["echo", "Step 1: Scaffolding project"])
    subprocess.run(["echo", "Step 2: Initializing Git"])
    print("Create complete!")

def main():
    parser = argparse.ArgumentParser(description="My CLI tool with multiple commands")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for 'build'
    subparsers.add_parser("build", help="Build the project")

    # Subparser for 'create'
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
