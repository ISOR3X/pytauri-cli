from pathlib import Path

from pytauri_cli.prompting import ask, select


def ask_info() -> dict[str, str | None]:
    project_name = ask("Project name", "pytauri-app")
    user = Path.home().name.lower()
    identifier = ask("Identifier", f"com.{user}.{project_name}")

    frontend_types = [
        ("Python", "uv"),
        ("TypeScript / JavaScript", "pnpm, yarn, npm, bun"),
    ]

    frontend_lang = select(
        "Choose which language to use for your frontend", frontend_types
    )

    match frontend_lang:
        case "TypeScript / JavaScript":
            frontend_frameworks = [
                ("Vanilla", None),
                ("Vue", "https://vuejs.org/"),
                ("Svelte", "https://svelte.dev/"),
                ("React", "https://react.dev/"),
            ]
        case default:
            frontend_frameworks = [
                ("NiceGUI", "https://nicegui.io/"),
            ]

    frontend_template = select("Choose your UI template", frontend_frameworks)

    frontend_flavor = None
    if frontend_lang == "TypeScript / JavaScript":
        frontend_flavors = [
            ("TypeScript", None),
            ("JavaScript", None),
        ]
        frontend_flavor = select("Choose your UI flavor", frontend_flavors)

    return {
        "project_name": project_name,
        "identifier": identifier,
        "frontend_lang": frontend_lang,
        "frontend_template": frontend_template,
        "frontend_flavor": frontend_flavor,
    }
