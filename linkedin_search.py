import pandas as pd
from linkedin_session import LinkedInSession
from tqdm import tqdm
import tools.files_tools as ft
import tools.plot_tools as pt


def scrap_several_companies(
    queries_file_name: str, file_to_store: str, batch_size: int = 100) -> None:
    """ Create batches of queries and launch a search on linkedin and store the results in a csv file.
        Queries being the name of the companies to look for.
        Args :
            queries_file_name (str): a path of a csv file with the queries
            file_to_store (str): a path of a csv file to store the results
            batch_size (int): the size of the batch of queries to be processed at once 
        To improve efficiency, all data companies are stored in a csv file name companies_data.csv so that we don't look twice for the same company.
        """
    data_in = pd.read_csv(queries_file_name)
    step = batch_size
    n = data_in.shape[0]
    url_in=[]
    known_companies=pd.read_csv('data\lix_scrapper\companies_data.csv').set_index('query',drop=False)
    if "query" in data_in.columns:
        if n > 0:
            for i in tqdm(range(n // step)):
                l_in = data_in.loc[(step * i) : (step * (i + 1)), "query"].to_list()
                if "url" in data_in.columns:
                    url_in = data_in.loc[(step * i) : (step * (i + 1)), "url"].to_list()
                search(l_in, file_to_store, url_in,known_companies)
                update_loss_file(file_to_store, queries_file_name)
                pd.DataFrame(known_companies).to_csv('data\lix_scrapper\companies_data.csv',index=False)

            l_in = data_in.loc[(n // step * step) :, "query"].to_list()
            if "url" in data_in.columns:
                url_in = data_in.loc[(n // step * step) :, "url"].to_list()
            else:
                url_in = []
            search(l_in, file_to_store, url_in,known_companies)
            update_loss_file(file_to_store, queries_file_name)
    pd.DataFrame(known_companies).to_csv('data\lix_scrapper\companies_data.csv',index=False)

def search(queries: list, file_to_store: str, urls_: list = [],known_companies=pd.DataFrame()) -> None:
    """launch a search on linkedin and store the results ( company data ) in a csv file

    Args:
        queries (list): a list of queries
        file_to_store (str): a path of a csv file to store the results
        known_companies:(dict) : previous queries history to enable not to go twice on the same company webpage
    """
    ls = LinkedInSession()
    for index, query in enumerate(queries):
        if query in known_companies.index.to_list():
            dic=known_companies.loc[query].to_dict()
        else: 
            if urls_ == [] or len(str(urls_[index])) < 5:
                urls = ls.search_for_companies(query)
            else:
                urls = [urls_[index]]
            if len(urls) > 0:
                dic = ls.scrap_a_company(urls[0], query)
                df = pd.Series(dic)
                known_companies.loc[query]=df
                # df = pd.DataFrame.from_dict(dic)
            else:
                dic = {"query": [query]}
        df_out = ft.concat(file_to_store, dic)
        df_out.drop_duplicates(subset="query", keep="last", inplace=True)
        df_out.to_csv(file_to_store, encoding="utf-8", index=False)
    ls.driver.close()


def update_loss_file(file_to_store: str, file_in: str) -> None:
    """update the file of queries that have not been processed yet
    Not very useful anuymore """
    data_in = pd.read_csv(file_in)
    list_index = []
    queries = pd.read_csv(file_to_store)["query"]
    for index, query in enumerate(data_in["query"]):
        if not query in list(queries):
            list_index.append(index)
    data_in.loc[list_index].to_csv(file_to_store[:-4] + "_loss.csv", index=False)


def scrap_several_jobs(offers:str,description_memory:str='data\lix_scrapper\job_descriptions.csv') -> None : 
    """ Launch a linkedin session and scratch the job descriptions
        Args: file.xlsx with the list of jobs of interest
        """
    jobs=pd.read_excel(offers)
    links=jobs['Link'].to_list()
    descriptions=[]
    #Create groups of links(jobs) to look for in the same session. size of the group is chunk_size
    links_for_session=[]
    chunk_size=30
    for i in range(0,len(links),chunk_size):
        links_for_session.append(links[i:i+chunk_size])
    for links_list in tqdm(links_for_session):
        ls= LinkedInSession()
        for link in links_list:
            description='Not found'
            description=ls.scrap_a_job(link)
            descriptions.append(description)
        ls.driver.close()
    jobs['Description']=descriptions
    jobs.to_excel(offers,index=False)
    print("done for file ", offers)

offers=r'data\lix_scrapper\trial.xlsx'


if __name__ == "__main__":
    # scrap_several_companies("data\quantumapalooza\companies.csv", "data\quantumapalooza\companies_data.csv")
    pt.plot_category_h(r'C:\Users\Simonis\Documents\quantum-jobs\data\lix_scrapper\offers_with_gpt_analysis.xlsx', "Industry Cluster")
    pt.plot_category_h(r'C:\Users\Simonis\Documents\quantum-jobs\data\lix_scrapper\offers_with_gpt_analysis.xlsx', "country")
    pt.plot_category_h(r'C:\Users\Simonis\Documents\quantum-jobs\data\lix_scrapper\offers_with_gpt_analysis.xlsx', "Company size")
    pt.plot_category_h(r'C:\Users\Simonis\Documents\quantum-jobs\data\lix_scrapper\offers_with_gpt_analysis.xlsx', "continent")




