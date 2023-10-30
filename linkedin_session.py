from web_session import WebSession
import pandas as pd
import time
from random import randint


class LinkedInSession(WebSession):
    def __init__(self):
        super().__init__()
        self.login()

    def login(self, login_file: str = "metadata/linkedin_login.csv"):
        """ Log in to linkedin with a random account from the login_file file."""
        url_log_in = """https://www.linkedin.com/login"""
        df_login = pd.read_csv(login_file)
        payload = dict(df_login.loc[randint(0, len(df_login) - 1)])
        self.go_to_url(url_log_in)
        username = self.find_by_xpath('//*[@id="username"]')
        username.send_keys(payload["username"])
        print(username)
        password = self.find_by_xpath('//*[@id="password"]')
        password.send_keys(payload["password"])
        self.clic("""/html/body/div/main/div[3]/div[1]/form/div[3]/button""")
        time.sleep(1)
        while self.driver.current_url != "https://www.linkedin.com/feed/":
            time.sleep(10)

    def search_for_companies(self, query: str):
        """Search for a company on linkedin and return the url of the first result"""
        url_0 = """https://www.linkedin.com/search/results/companies/?keywords="""
        url_1 = """&origin=GLOBAL_SEARCH_HEADER&sid=3oM"""
        try:
            query = query.replace("&", " ")
        except:
            return []
        url = url_0 + query + url_1
        self.go_to_url(url)
        time.sleep(1)
        class_0 = """reusable-search__result-container"""
        xpath_0 = """/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[*]/div/div/div[2]/div[1]/div[1]/div/span/span/a"""
        results = self.find_several_by_xpath(xpath_0)
        urls = []
        if len(results) == 0:
            xpath_1="""/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[3]/div/ul/li[1]/div/div/div[2]/div[1]/div[1]/div/span/span/a"""
            results = self.find_several_by_xpath(xpath_1)
        if len(results) == 0:
            urls = []
        else:
            for result in results:
                url = result.get_attribute("href")
                urls.append(url)
        time.sleep(0.25)
        return urls

    def scrap_a_company(self, url: str, query: str = "") -> dict:
        """Scrap a company page on linkedin and return a dictionary with the results"""
        if query == "":
            query = url.strip("/")[-1]
        dic = {"query": query, "url": url}
        dic = self.scrap_a_page("xpaths/linkedin/company.csv", dic, url=url)
        dic = self.scrap_a_page("xpaths/linkedin/about.csv", dic, url=url + "about/")
        categories = self.find_all_elements("dl", """overflow-hidden""")
        if not categories == []:
            els = list(categories[0])
            for el in els:
                if el.name == "dt":
                    title = el.text.strip()
                    description = ""
                elif el.name == "dd":
                    to_add = el.text.strip().replace("\n", " ").replace(",", ".")
                    description = description + " " + to_add
                    dic[title] = description
        return dic


    def scrap_a_job(self, url=str) -> str : 
        """ Scrap a job page on linkedin and return the job description"""
        self.go_to_url(url)
        time.sleep(1)
        button='/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[4]/footer/button'
        self.clic(button)
        time.sleep(1)
        xpaths=['/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[4]/article/div','/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[2]',\
                '/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[2]/article/div']
        description=""
        for xpath in xpaths : 
            if len(description)==0:
                description=self.get_text(xpath)
        return description

if __name__ == "__main__":
    print("Done")
