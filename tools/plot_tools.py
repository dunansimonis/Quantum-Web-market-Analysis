import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_match(
    df0: pd.DataFrame,
    col_labels: list,
    name_plot: str,
    limit: int = 10,
    min_Y: float = 1,
) -> None:
    df = pd.DataFrame(df0[col_labels])
    list_to_gather = []
    df = set_quantity(df, col_labels)
    df = gather(df, "quantity", col_labels, list_to_gather, "ok")
    print("number : ", df["quantity"].sum())
    df = df[df["quantity"] > min_Y]
    df = df.sort_values(by=["quantity"], ascending=False)
    labels = remove_space(df[col_labels], limit=limit)
    plot_bar(df["quantity"], labels, name_plot)


def plot_bar(Y: list, labels: list, title: str, path_plot: str = "") -> None:
    """plot a bar diagram with Y list and adding labels

    Args:
        Y (list): list oy y-axis values (bars)
        labels (list): list of labels for each bar
        title (str): title of the plot
        path_plot (str, optional): the path where you want to save your plot. Defaults to "".
    """
    fig = plt.figure(figsize=(8, 5))
    fig.subplots_adjust(bottom=0.4)
    X = [i for i in range(len(Y))]
    plt.bar(X, Y)
    plt.xticks(X, labels)
    plt.xticks(fontsize=8,rotation=90)
    plt.title(title)
    if path_plot != "":
        plt.savefig(path_plot, dpi=1200)

def plot_barh(Y: list, labels: list, title: str, path_plot: str = "") -> None:
    """plot a bar diagram with Y list and adding labels

    Args:
        Y (list): list oy y-axis values (bars)
        labels (list): list of labels for each bar
        title (str): title of the plot
        path_plot (str, optional): the path where you want to save your plot. Defaults to "".
    """
    fig = plt.figure(figsize=(8, 5))
    fig.subplots_adjust(left=0.3)
    X = [i for i in range(len(Y))]
    X=X[::-1]
    plt.barh(X, Y)
    plt.yticks(X, labels)
    plt.yticks(fontsize=5)
    plt.title(title)
    if path_plot != "":
        plt.savefig(path_plot, dpi=1200)


def set_quantity(df: pd.DataFrame, name_col: str, sort: bool = True) -> pd.DataFrame:
    """Return the dataframe in entry with a added column containing the quantity of each element of the name_column

    Args:
        df (pd.DataFrame): data
        name_col (str): the name of the column of the dataframe you want to set quantity
        sort (bool, optional): True for descending, False for ascending. Defaults to True.

    Returns:
        pd.DataFrame: return a copy of the original dataframe where a "quantity" column was added
    """
    res = []
    for code in df[name_col].unique():
        df_code = df[df[name_col] == code]
        dic = {"quantity": df_code.shape[0]}
        for col_name in df.columns.values:
            dic[col_name] = df_code[col_name].iloc[0]
        res.append(dic)
    df = pd.DataFrame(res)
    if sort:
        df = df.sort_values("quantity", ascending=False)
    return df


def gather(df, quantity_col, col_name, list_name, new_name):
    new = []  # "Astronomers", "Materials Scientists", "Physicists"
    quantity = 0
    for x in df[col_name].values:
        if x in list_name:
            new.append(new_name)
            quantity += df[df[col_name] == x][quantity_col].iloc[0]
        else:
            new.append(x)
    df2 = df.assign(new=new)
    return df2


def remove_space(bars, limit: int = 10):
    labels = []
    for i, x in enumerate(bars):
        value = 0
        new_c = ""
        for c in x:
            if value > limit and c == " ":
                new_c = new_c + "\n"
                value = 0
            else:
                new_c = new_c + c
                value += 1
        labels.append(new_c)
    return labels

def plot_category(filename: str, category :str) -> None:
    df = pd.read_excel(filename)
    if "query" in df.columns and category in df.columns:
        df = df[["query", category]]
        df = df.dropna()
        quantity = set_quantity(df, category)
        cat = quantity[quantity["quantity"] > 2][
            ["quantity", category]
        ]
        nb_other = df.shape[0] - cat["quantity"].sum()
        cat= cat.append(
            {"quantity": nb_other, category: "others"},
            ignore_index=True,
        )
        path = filename[:-5] + category+'.png'
        plot_bar(
            cat["quantity"],
            cat[category],
            title="",
            path_plot=path,
        )

def plot_category_h(filename: str, category :str,name_of_data:str ='') -> None:
    df = pd.read_excel(filename)
    if "query" in df.columns and category in df.columns:
        df = df[["query", category]]
        df = df.dropna()
        quantity = set_quantity(df, category)
        cat = quantity[quantity["quantity"] > 2][
            ["quantity", category]
        ]
        nb_other = df.shape[0] - cat["quantity"].sum()
        cat= cat.append(
            {"quantity": nb_other, category: "others"},
            ignore_index=True,
        )
        path = 'Distribution_of_'+category+'_h'+'.png'
        plot_barh(
            cat["quantity"],
            cat[category],
            title='Distribution of ' + category ,
            path_plot=path,
        )

def plot_category_employer(filename: str, category :str) -> None:
    df = pd.read_excel(filename)
    if "employer" in df.columns and category in df.columns:
        df = df[["employer", category]]
        df = df.dropna()
        quantity = set_quantity(df, category)
        cat = quantity[quantity["quantity"] > 2][
            ["quantity", category]
        ]
        # nb_other = df.shape[0] - cat["quantity"].sum()
        # cat= cat.append(
        #     {"quantity": nb_other, category: "others"},
        #     ignore_index=True,
        # )
        path = filename[:-5] + category+'.png'
        plot_bar(
            cat["quantity"],
            cat[category],
            title="",
            path_plot=path,
        )
