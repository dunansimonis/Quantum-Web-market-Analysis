import pandas as pd
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from tools import xpaths_tools
from selenium.webdriver.firefox.service import Service


class WebSession:
    def __init__(self):
        """open the firefox browser"""
        options = Options()
        df = pd.read_csv("metadata/major_paths.csv")
        options.binary_location = df[df["name"] == "firefox"].loc[0, "path"]
        # s=Service('geckodriver.exe')
        # # path_to_use=df[df["name"] == "firefox"].loc[0, "path"]
        self.driver = webdriver.Firefox(
            executable_path="out/geckodriver.exe", options=options
        )
        # self.driver=webdriver.Firefox(service=s)

    def go_to_url(self, url: str) -> None:
        """go to a url"""
        time.sleep(0.3)
        self.driver.get(url)

    def get_current_url(self):
        """get current url"""
        return self.driver.current_url

    def close(self):
        """close the browser"""
        self.driver.close()

    def check_exists_by_xpath(self, xpath: str) -> bool:
        """check if a element exist or not on a actual webpage

        Args:
            xpath (str): the xpath of the element you want to chek the presence

        Returns:
            bool: True if its present and False if not
        """
        try:
            self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def find_by_xpath(self, xpath: str):
        """find the element by xpath

        Args:
            xpath (str): xpath of the element to find

        Returns:
            str: _description_
        """
        return self.driver.find_element(By.XPATH, xpath)

    def find_several_by_xpath(self, xpath: str):
        """find the element by xpath

        Args:
            xpath (str): xpath of the element to find

        Returns:
            str: _description_
        """
        return self.driver.find_elements(By.XPATH, xpath)

    def clic(self, xpath_button: str, y_gap: int = 0) -> None:
        """if a button exists : scroll until it and click on it if its enable

        Args:
            xpath_button (str): the xpath of the element you want to chek the presence
            y_gap (int): lenght of the gap to add to the position to scroll
        """
        if xpath_button != "":
            if self.check_exists_by_xpath(xpath_button):
                display_button = self.find_by_xpath(xpath_button)
                x = display_button.location["x"]
                y = display_button.location["y"] - y_gap
                if display_button.is_enabled():
                    self.driver.execute_script(f"""window.scrollTo({x}, {y})""")
                    time.sleep(1)
                    try:
                        display_button.click()
                    except: #Sometimes a header on the website is above the button we want to click on so we stop scrolling before the button so that we can clic on it 
                        self.driver.execute_script(f"""window.scrollTo({x}, {y-100})""")
                        display_button.click()


    def change_option(self, xpath: str, option: str, y_gap: int = 0) -> None:
        if xpath != "":
            if self.check_exists_by_xpath(xpath):
                display_button = self.find_by_xpath(xpath)
                x = display_button.location["x"]
                y = display_button.location["y"] - y_gap
                if display_button.is_enabled():
                    self.driver.execute_script(f"""window.scrollTo({x}, {y})""")
                    time.sleep(1)
                    op = Select(self.find_by_xpath(xpath))
                    op.select_by_visible_text(option)

    def get_text(self, xpath: str) -> str:
        """get the text of a element after check if it exists or not

        Args:
            xpath (str):  the xpath of the element you want to extrat the text

        Returns:
            str: the tect on the element
        """
        if self.check_exists_by_xpath(xpath):
            return self.find_by_xpath(xpath).text
        else:
            return ""

    def scrap_a_page(self, refs: str, dic: dict, add:str="",url: str = "") -> dict:
        xpaths = xpaths_tools.read_xpaths(refs)
        if url != "":
            self.go_to_url(url)
        time.sleep(1.5)
        for key in list(xpaths.keys()):
            dic[add + key] = None
        for el in xpaths.keys():
            value = ""
            i = 0
            try:
                while value == "" and i < len(xpaths[el]):
                    time.sleep(0.1)
                    value = self.get_text(xpaths[el][i])
                    value = value.replace(",", ".").replace("\n", " ")
                    i += 1
                dic[add + el]=value
            except:
                dic[add + el]=None
        return dic

    def find_all_elements(self, ref: str, class_: str) -> list:
        time.sleep(0.5)
        page_source = self.driver.page_source.encode("utf-8")
        soup = BeautifulSoup(page_source, "html.parser")
        out = soup.find_all(ref, class_)
        return out

    def extract_table(self, refs: str) -> dict:
        """extract table from websession using the given refs

        Args:
            refs (str): a path to a xpath containing file

        Returns:
            dict: a dictionnary containing the extracted data
        """
        xpaths = xpaths_tools.read_xpaths(refs)
        dic = {}
        for label in xpaths.keys():
            dic[label] = []
        for _, label in enumerate(xpaths.keys()):
            content = self.find_several_by_xpath(xpaths[label][0])
            for el in content:
                if label == "link":
                    dic[label].append(el.get_attribute("href"))
                else:
                    dic[label].append(el.text.replace("\n", " ").replace(",", " "))
        return dic

    def add_several_elements(self, refs: list, storage: dict) -> dict:
        out = storage.copy()
        """search several information from refs in the actual webdriver and store it in storage

        Args:
            refs (list): a list of dictionnary with labels :
                            - 'name' : that will be the label of the found value in the storage
                            - 'xpath': that is the xpath of the element to extraxt the text
            storage (dict): a dictionnary where will be add the founded elements

        Returns:
            dict: previous and new elements
        """
        for ref in refs:
            if len(ref["xpath"].split("/")) <= 1:
                content = ref["xpath"]
                out[ref["name"]] = content
            elif ref["name"] == "cookies":
                self.clic(ref["xpath"])
            else:
                try:
                    content = self.get_text(ref["xpath"])
                except Exception:
                    content = "error"
                    pass
                out[ref["name"]] = content
        return out

