import pandas as pd
from linkedin_search import scrap_several_companies, scrap_several_jobs
import os
import tools.cleaning_file as cf

def new_filter(lix_extended_data:str)-> None :
    ''' Input : the scraped list of job provided by LIX with data provided from linkedin algorithm (.csv)
        Action : Filter the file by keeping only the rows in which quantum is either in the job title 
                        or Compagny name or Commpany description or Company Overview  
        Output : .xlsx file
      '''
    df=pd.read_csv(lix_extended_data,encoding="utf-8")
    size=df.shape[0]
    ind=[]
    df.fillna('')
    for i in range(size):
        title=df.loc[i]['Title']
        company=df.loc[i]['query']
        description=df.loc[i]['query']
        overview=df.loc[i]['overview']
        L=[title, company, description, overview]
        string=''
        for word in L:
            if isinstance(word,str):
                string+=' ' +word
        string=string.lower().split()
        if not 'quantum' in string and not 'quantique' in string:
            ind.append(i)
    dfq=df.drop(ind)
    dfq.to_excel(lix_extended_data[:-4]+'_quantum'+ '.xlsx',index=False)

def pre_processing(lix_row_data:str) -> None :
    ''' Input : lix scraped row job list (.xlsx)
        Action: return a csv with just the  names of the organisation. This file is to be 
                used for scratching the companies data with function scrap_several_compagnies 
                from linkedin_search
      '''
    df=pd.read_excel(lix_row_data)
    df.drop([df.shape[0]-1],inplace=True)
    companies=[]
    for i, company in enumerate(df['Organisation Name']):
        try :
            companies.append(company.lower())
        except:
            companies.append('')
    df['companies']=companies
    df['companies'].to_csv(lix_row_data[:-5]+ '_companies.csv', header=['query'], index = False)
    names=df['Organisation Name'].apply(lambda x : str(x).lower())
    df.drop(columns=['Organisation Name'],inplace=True)
    df.insert(3,'Organisation Name',names)
    df.to_excel(lix_row_data,index=False)


def new_merge(lix_row_data:str, compagny_data:str)-> None :
    """Merge data from lix with data from linkedin algorithm into one new xlsx document
        input : lix original file (.xlsx) and file resulting from linkedin algorithm (.csv)
        """
    df_row=pd.read_excel(lix_row_data)
    df_cp=pd.read_csv(compagny_data)
    df_merge=df_row.merge(df_cp,how='left',left_on='Organisation Name', right_on='query')
    df_merge.to_csv(lix_row_data[:-5]+'_data.csv',encoding="utf-8",index=False)


def new_lix_pipeline(lix_row_data:str, del_file :bool=True) -> None:
    ''' Add data from linkedin algorithm to data receive from lix.
        Result is stored in a new .xlsx file
        Input :lix_row_data = Name of the row lix file
                del_file = Bool , True if we want to delete the intermediary files.
      '''
    name=lix_row_data[:-5]
    try : 
        df_loss=pd.read_csv(name+'_companies_data_loss.csv')
        df_known=pd.read_csv(name+'_companies_data.csv')
        print(df_loss.shape[0])
        if df_loss.shape[0]>1:
            scrap_several_companies(name+'_companies_data_loss.csv',name+'_companies_data2.csv')
            df=pd.concat([df_known,pd.read_csv(name+'_companies_data2.csv')])
            df.to_csv(name+'_recovery.csv', encoding="utf-8", index=False)
            new_merge(lix_row_data,name+'_recovery.csv')
            new_filter(name+'_data.csv')
    except:
        pre_processing(lix_row_data)
        scrap_several_companies(name+'_companies.csv',name+'_companies_data.csv')
        new_merge(lix_row_data,name+'_companies_data.csv')
        new_filter(name+'_data.csv')
        scrap_several_jobs(name+'_data_quantum.xlsx')
        delete_file(lix_row_data,del_file)
        # gpt_pipeline(name+'_data_quantum.xlsx')
    print("quantum data extracted ! ")
    clean_merge(name+'_data_quantum.xlsx')


def delete_file(input_lix:str, del_file:bool):
    if del_file:
        os.remove(input_lix[:-5]+'_companies.csv')
        os.remove(input_lix[:-5]+'_companies_data.csv')
        os.remove(input_lix[:-5]+'_data.csv')
        df=pd.read_csv(input_lix[:-5]+'_companies_data_loss.csv')
        if df.shape[1]==1:
            os.remove(input_lix[:-5]+'_companies_data_loss.csv')


def total_job_offers(file1:str,file2=str,to_store=str):
    """ Concatenate two excel files
        """
    df1=pd.read_excel(file1)
    df2=pd.read_excel(file2)
    df=pd.concat([df1,df2])
    df.to_excel(to_store,index=False)
    print('merged',file1,'with',file2,'into',to_store)

def clean_merge(file:str):
    """ Clean company size, add country et continent to a file and then merge it with the total file of offers
        """
    cf.clean_company_size(file)
    cf.add_countries_continent(file)
    offers_file='data\lix_scrapper\offers.xlsx'
    total_job_offers(offers_file,file,offers_file)


new_lix_pipeline('data\lix_scrapper\daily_extracts\LIX_200823.xlsx')


#clean_merge('data\lix_scrapper\daily_extracts\LIX_210423_data_quantum.xlsx')

# total_job_offers('data\lix_scrapper\LIX_140423_data_quantum.xlsx','data\lix_scrapper\offers.xlsx','data\lix_scrapper\offers.xlsx')

# ########## Previous Pipeline where the quantum filtering was done only on the title of job

# def filter(input_lix:str) -> None:
#     """ Input : the scraped list of job provided by LIX 
#         Action :  create 2 files :
#             1) filtered  .csv file with only the jobs containing quantum
#             2) Same but only the name of the organisation. This file is destined 
#                 to be used as input to scratch the compagy data
#         """
#     output_quantum=input_lix[:-5]+'_quantum'
#     output_quantum_companies=output_quantum+'_companies'
#     df = pd.read_excel(input_lix)
#     ind=[df.shape[0]-1]
#     titles = df["Title"].dropna()
#     for i,x in enumerate(titles):
#         l = x.lower().split()
#         if not "quantum" in l:
#             if not "quantique" in l:
#                 ind.append(i)
#     dfq=df.drop(ind)
#     dfq.to_csv(output_quantum+'.csv')
#     dfqc=dfq.filter(['Organisation Name'])
#     dfqc.to_csv(output_quantum_companies+'.csv', header=['query'],index=False)

# def merge(lix_row_data:str, compagny_data:str)->None:
#     """Merge data from lix with data from linkedin algorithm into one new xlsx document
#         input : lix original file and file resulting from linkedin algorithm
#         """
#     df_row=pd.read_csv(lix_row_data)
#     df_cp=pd.read_csv(compagny_data)
#     df_merge=df_row.merge(df_cp,how='left',left_on='Organisation Name', right_on='query')
#     df_merge.to_excel(lix_row_data[:-5]+'_data.xlsx')

# #merge('data\lix_scrapper\LIX_trial_quantum.csv','data\lix_scrapper\LIX_test.csv')

# def lix_pipeline(input_lix:str, del_file:bool=True)->None:

#     """Add data from linkedin algorithm to data receive from lix.
#         Result is stored in a new .xlsx file
#         Input :input_lix = Name of the row lix file
#                 del_file = Bool , True if we want to delete the intermediary files.
        
#         """
#     filter(input_lix)
#     scrap_several_companies(input_lix[:-5]+'_quantum_companies.csv',input_lix[:-5]+'_companies_data.csv')
#     merge(input_lix[:-5]+'_quantum.csv',input_lix[:-5]+'_companies_data.csv')
#     delete_file(input_lix,del_file)

# lix_pipeline('data\lix_scrapper\LIX_trial.xlsx')
