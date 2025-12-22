# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "copier>=9.7.1",
# ]
# ///
import copier

from pytauri_cli._argparse import ClapArgumentParser
from pytauri_cli.build import build_project, embed_python
from pytauri_cli.create import ask_info


def create(url: str = "https://github.com/pytauri/create-pytauri-app"):
    info = ask_info()
    copier.run_copy(url, ".", data=info)


def main():
    parser = ClapArgumentParser(
        prog="pytauri",
        description="Tauri bindings for Python through Pyo3",
    )

    commands = parser.add_subparsers(title="Commands", dest="commands")

    commands.add_parser("create", help="Create a new PyTauri project")

    commands.add_parser(
        "build",
        help="Build a project into a source distributions and wheels",
    )

    commands.add_parser("dev", help="Start the development server")

    args = parser.parse_args()
    # print(args)

    # Show help if no command is given
    if not args.commands:
        parser.print_help()
        return

    if args.command == "build":
        build_project()
    elif args.command == "create":
        create()
    elif args.command == "dev":
        pass
    elif args.command == "embed-python":
        embed_python()
