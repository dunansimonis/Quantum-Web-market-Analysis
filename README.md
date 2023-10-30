# **Quantum Job Market Scraping**

This gitlab contains all the code and data for analysis of Quantum Job Market. This Read me is to edit it's not complete now. 

First notice that an non-technical documentation of the project is available here : ####

Bellow is an overview of the project, note that most python file and notebook are properly commented so newcommers should be able to keep on with the logic.

## First Overview of the Project

The project aimed at studying the market of Quantum Physics in the World and more precisely in Europe. To do that the project is divided in two parts.

![pipeline](https://gitlab.com/scienceathome/datasci/quantum-jobs/-/blob/9fc3c4e1f228fb03a755ea6b92b5a264f023c886/data/lix_scrapper/useful/pipeline.png)

1. **Linkedin Scrapping**

Jobs offers are scrapped from linkedin with all data relative to company, job post to build a strong database.


2. **GPT analysis**

We use LLM (GPT API) to perform analysis on text data that we could not analyse precisely on a big scale.

## **Getting started**
 
 The baseline of this project is the webscrapping (Linkedin webscrapping). A class web_session is define in *web_session.py* and is the starting point for all webscrapping algorithms. It opens firefox browser and use Selenium to navigate. Note that a lot of very useful basic functions are define : to clic, search an element by xpath, scrap text, look if a element is available etc.


## **Linkedin Scrapping**

Linkedin Scrapping is the most advance part of the project.

![Linkedin](https://gitlab.com/scienceathome/datasci/quantum-jobs/-/blob/9fc3c4e1f228fb03a755ea6b92b5a264f023c886/data/lix_scrapper/useful/database.png)


The *linkedin.session.py* then defines a subclass and functions to navigate easily on linkedin. The *linkedin_search.py* helps with navigating on a big scale. Functions are defined so that you can input a list of companies you want to scrap and it will devide the list into batches, launch different sessions to prevent linkedin to block us etc.

The pipeline is the most important thing to understand. Here are slides presenting the general pipeline : 
https://docs.google.com/presentation/d/1CGWA4GVnPIxfiL-HpQMmwiNFoDIX3nVif95-K1htxWk/edit#slide=id.g24857244fbc_0_5

The idea is the following : 
1. We use LIX Google chrome extention to scrap a list of jobs offers from linkedin, we receive only the job title, the name of the company and the link to the jobpost. This has to be run on a daily basis and is currently in automation in file *lix_automate.ipynb* . 

2. Once we have input data we can apply our Algorithm to scrap linkedin. The file *lix_search.py* is the one with the pipeline current pipeline. It uses *linkedin_search.py* and therefore also the class defined in linkedin_session. At this point the algorithm scrap all data about the company and merge it with the input file (job offers) after filtering. The file is then merged with the total database in 
*data\lix_scrapper\offers.xlsx* .

3. Note that some cleaning and  quantum filtering is made to improve the database. 

4. We perform analysis on the data we have collected. Create plots etc.

## **GPT Analysis** 

The GPT Analysis has not been added to the full pipeline in *lix_search.py* for now as we are still reviewing the results in details.

A notebook gpt_classification.ipynb has been created, it's made to use GPT-API to cluster jobs and perform skills analysis. Plots are also made. It should also be export as a .py file  at some point so that we can use the functions defined inside in others parts of the code. So please edit the notebook and don't forget to export changes to the python file after. 

scheme : 
1. Create connection with the API, define usefull functions
2. Ask for a "Quantum Confidence Score" and a job category
3. Clean database based on the previous score
4. Extract skills from job description
5. Skills analysis 
6. Plots, visualisation 

 Extended database (with GPT analysis) is then stored in the *data\lix_scrapper\offers_with_gpt_analysis.xlsx* file. Europe only version is available at *europe_only.xlsx*. 

 ![skills](https://gitlab.com/scienceathome/datasci/quantum-jobs/-/blob/9fc3c4e1f228fb03a755ea6b92b5a264f023c886/data/lix_scrapper/useful/skills%20analysis.png)
 
## **Understanding the gitlab structure and file**

### data/lix_scrapper folder

The file *data/offer.xlxs* is the output of the lix/linkedin pipeline. It's updated automatically by the *lix_search.py* when run. 

The files *companies_data.csv*, *continent_data.csv*, *location_data.csv* are **storage of data updated at every run** of the algorithm so that we don't search every day a 1000 times the same data. Thanks to this storage the pipeline can run in 30mins instead of 8hours.

The plots are used for analysis and made using the ploting tools define bellow.

The *data\lix_scrapper\daily_extracts* folder inside stores all excel file extracted using lix, naming convention is LIX_DDMMYYY.xslx . Once the linkedin algorihtm is applied to this file, a file LIX_DDMMYYY_data_quantum.xlxs is generated with only the relevant rows and with all additional data from the algorithm. This is the file that is merged with offers.py

The notebook *data\lix_scrapper\clustering_skills_kmeans.ipynb* perform quickly a kmeans algorithms on skills extracted with gpt. It was just a quick trial (edited version of previous trial on our partner's data) annd it's not cleaned. 

### data/Quantumaoalooza folder

Contains data from our partner Tarrils. The notebook *clusteringjobs.ipynb* was used to perform the clustering on job titles using Kmeans. It was a trial to see the kind of results we could have and we did not have the job description at this moment. 
The notebook *jup.ipynb* is used to perform clustering using a list of labeled words.

### Tools folder 
Contains a lot of python files defining functions usefull for analysis. 
*cleaning_file.py* is extremely important for cleaning/filtering/adding data during the linkedin algorithm.
*file_tools.py* and *xpaths_tools.py* are used during the pipeline to read files / find xpaths . 
*plot_tools.py* define functions used to generate basic plots. 

### Metadata folder 

*metada\linkedin_login.csv* contains different account login/pwd used to connect on linkedin. We are using different accounts to prevent linkedin from blocking us and to lower the amount of user verification asked.

*metadata\openai_api_key.txt* name is explicit.
### xpaths folder

csv files containing xpaths and description(key) of what we are trying to scrap. The format is a bit specific but the functions used to read xpaths are made so that you can put different xpaths for the same key and the scrapper will try all the xpath for this key until one is found.

## **Utils**

A lot of file are not currently used, I need to clean the gitlab I'm on it ! Done
