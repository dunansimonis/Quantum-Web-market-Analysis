import pandas as pd

def checkFileExistance(filePath:str)->bool:
    """checks if the file exists
    Args:
        filePath (str): the path to the file

    Returns:
        bool: True if the file exists, False otherwise
    """
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

def concat(file_to_store,dic):
    if checkFileExistance(file_to_store):
        df_in = pd.read_csv(file_to_store)
        cols = df_in.columns.tolist()
        for col in cols:
            try:
                _ = dic[col]
            except:
                dic[col] = None
        for index in dic.keys():
            if not index in cols:
                df_in[index] = None
        df = pd.DataFrame(dic, index=[dic['query']])
        df_out = pd.concat([df_in, df])
    else:
        df_out = pd.DataFrame(dic,index=[dic['query']])
    return df_out

def update_loss_file(file_to_store: str, file_in: str,name_col:str) -> None:
    data_in = pd.read_csv(file_in)
    list_index = []
    queries = pd.read_csv(file_to_store)[name_col]
    for index, query in enumerate(data_in[name_col]):
        if not query in list(queries):
            list_index.append(index)
    data_in.loc[list_index].to_csv(file_to_store[:-4] + "_loss.csv", index=False)

def delete_french_data():
    index=[]
    df=pd.read_csv('data\lix_scrapper\companies_data.csv')
    print(df.columns)
    size=df.shape[0]
    for i in range(size):
        french_size=df.loc[i]["Taille de l’entreprise"]
        try : 
            if len(french_size)>=1 : 
                index.append(i)
        except :
            a=1
    print(len(index))
    df.drop(index, inplace=True)
    df.to_csv('data\lix_scrapper\companies_data.csv')