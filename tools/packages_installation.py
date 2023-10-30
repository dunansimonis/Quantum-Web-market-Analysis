import sys
import subprocess
import pandas as pd


classic_packages = pd.read_csv('metadata/packages.csv')['name'].tolist()

def install_packages(packages: list) -> None:
    """Install a list of packages in the python environement.

    Args:
        packages (list): a list of packages to install.
    """
    for p in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", p])


if __name__ == "__main__":
    install_packages(['pyodbc'])
