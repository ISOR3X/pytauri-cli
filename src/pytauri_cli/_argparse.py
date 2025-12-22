import argparse

from pytauri_cli.prompting import Color, colored


class ClapFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        super().start_section(colored(heading, Color.GREEN))

    def _format_usage(self, usage, actions, groups, prefix):
        return colored("Usage: ", Color.GREEN) + colored(
            f"{self._prog} [OPTIONS] <COMMAND>\n", Color.CYAN
        )

    def _format_action_invocation(self, action):
        res = super()._format_action_invocation(action)
        return colored(res, Color.CYAN)


class ClapArgumentParser(argparse.ArgumentParser):
    def __init__(
        self,
        prog=None,
        usage=None,
        description=None,
        epilog=None,
        parents=[],
        formatter_class=ClapFormatter,
        prefix_chars="-",
        fromfile_prefix_chars=None,
        argument_default=None,
        conflict_handler="error",
        add_help=False,
        allow_abbrev=True,
        exit_on_error=True,
    ):
        super().__init__(
            prog,
            usage,
            description,
            epilog,
            parents,
            formatter_class,
            prefix_chars,
            fromfile_prefix_chars,
            argument_default,
            conflict_handler,
            add_help,
            allow_abbrev,
            exit_on_error,
        )

    def format_help(self):
        """
        Same as default, just description and usage are flipped
        """
        formatter = self._get_formatter()

        # description
        formatter.add_text(self.description)

        # usage
        formatter.add_usage(
            self.usage,
            self._actions,
            self._mutually_exclusive_groups,
        )

        # positionals, optionals and user-defined groups
        for action_group in self._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        # epilog
        formatter.add_text(self.epilog)

        # determine help from format above
        return formatter.format_help()
