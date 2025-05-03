import os
import re
import shutil
import subprocess
import tarfile
from pathlib import Path

import requests


def get_python_version(root: Path):
    """
    Get the python version to use for the standalone
    :return: The Python version string (e.g., "3.12.0")
    """
    p = root / "src-tauri" / "src-python" / ".python-version"

    if not p.exists():
        raise FileNotFoundError(
            f"Python version file not found at {p.absolute()}. Make sure you run the CLI from project root!")

    with open(p, "r") as f:
        py_version = f.read().strip()
    print(f"Python version: {py_version}")
    return py_version


def get_standalone_url(py_version) -> str | None:
    """
    Fetch the standalone from the GitHub release page
    :param py_version: The Python version string (e.g., "3.12.0")
    :return: Path to the downloaded standalone file
    """
    # Fetch the latest release from GitHub
    url = "https://api.github.com/repos/astral-sh/python-build-standalone/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    release_data = response.json()

    # Extract version from py_version (e.g., "3.12.0" from "3.12.0")
    version_pattern = re.compile(r'(\d+\.\d+)')
    version_match = version_pattern.search(py_version)
    if not version_match:
        raise ValueError(f"Could not extract version from {py_version}")

    py_version_short = version_match.group(1)  # e.g., "3.12"

    # Find the appropriate asset for Windows that matches the Python version
    # Looking for pattern like: cpython-3.12.10+20250409-x86_64-pc-windows-msvc-install_only_stripped.tar.gz
    # Using $ at the end to exclude .sha256 files
    windows_pattern = re.compile(
        rf'cpython-{py_version_short}\.\d\d(?:\+\d+)?-x86_64-pc-windows-msvc-install_only_stripped\.tar\.gz$')

    matching_assets = [
        asset for asset in release_data["assets"]
        if windows_pattern.search(asset["name"])
    ]

    if not matching_assets:
        raise ValueError(
            f"No matching Python standalone build found for Python {py_version} on Windows with pattern cpython-{py_version_short}.XX[+YYYYMMDD]-x86_64-pc-windows-msvc-install_only_stripped.tar.gz")

    # Select the first matching asset
    selected_asset = matching_assets[0]

    print(f"Found matching Python standalone build: {selected_asset['name']}")

    # Download the asset
    download_url = selected_asset["browser_download_url"]
    return download_url


def download_standalone(download_url, to: Path):
    if not to.name.endswith(".tar.gz"):
        raise ValueError(f"Expected .tar.gz file, got {to.name}")

    print(f"Downloading from {download_url}...")
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(to, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"Downloaded Python standalone build to {to.absolute()}")


def extract_to_pyembed(tar_file, root) -> Path | None:
    """
    Extract the standalone .tar.gz and extract it to './src-tauri/pyembed'
    :param root: Root directory of the project (e.g., Path.cwd())
    :param tar_file: Path to the downloaded standalone file
    :return: Path to the extracted directory
    """
    # Create the pyembed directory if it doesn't exist
    pyembed_dir = root / "src-tauri" / "pyembed"
    pyembed_dir.mkdir(parents=True, exist_ok=True)

    extraction_path = root / "src-tauri" / "temp_extract"
    extraction_path = extraction_path.absolute()

    # Extract the tar.gz file
    with tarfile.open(tar_file, 'r:gz') as tar:
        tar.extractall(path=str(extraction_path))

    # Find the python directory in the extracted files
    python_dir = root / "src-tauri" / "temp_extract" / "python"
    if not python_dir.exists():
        raise FileNotFoundError(f"Python directory not found in extracted files at {python_dir.absolute()}")

    # Copy the contents from python\ to pyembed\
    print(f"Extracting contents to {pyembed_dir}...")
    for item in python_dir.iterdir():
        if item.is_dir():
            shutil.copytree(item, pyembed_dir / item.name, dirs_exist_ok=True)
        else:
            shutil.copy2(item, pyembed_dir / item.name)

    # Clean up the temporary directory
    shutil.rmtree(str(extraction_path))
    os.remove(tar_file)

    print(f"Python standalone build extracted to {pyembed_dir.absolute()}")
    return pyembed_dir


def add_pyembed(root):
    download_url = get_standalone_url(get_python_version(root))

    tar_file = root / "src-tauri" / "standalone.tar.gz"

    download_standalone(download_url, tar_file)
    extract_to_pyembed(tar_file, root)


def get_package_name(root: Path) -> str:
    toml_path = root / "src-tauri" / "src-python" / "pyproject.toml"

    if not toml_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found at {toml_path.absolute()}")

    with open(toml_path, "r") as f:
        toml_content = f.read()

    package_name = re.search(r'name = "(.*)"', toml_content).group(1)
    return package_name


def install_pkg_to_pyembed(package_name: str, root: Path):
    """

    :return:
    """

    tauri_src = root / "src-tauri"
    python_exe = tauri_src / "pyembed" / "python.exe"

    command = [
        "uv", "pip", "install",
        "--exact",
        "--python", str(python_exe),
        "--reinstall-package", package_name,  # Use the dynamically found package name
        str(tauri_src / "src-python"),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True, shell=False)
    print(result.stdout)
    print("Completed installation of package to pyembed")


def embed_python():
    root = Path.cwd()

    add_pyembed(root)
    install_pkg_to_pyembed(get_package_name(root), root)


def build_project():
    """
    Builds the PyTauri project.
    """
