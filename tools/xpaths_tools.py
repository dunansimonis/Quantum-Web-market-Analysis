import pandas as pd

def read_xpaths(file_name: str) -> dict:
    """read a .txt file and return the dictionary associated

    Args:
        file_name (str): the name and path of the file

    Returns:
        list: list of str which are each lines of the .txt file
    """
    df = pd.read_csv(file_name, sep=",")
    out = df.groupby("label")["xpath"].apply(list)
    return out.to_dict()