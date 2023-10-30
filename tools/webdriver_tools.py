import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def clic(webdriver: webdriver, xpath_button: str, y_gap: int = 0) -> None:
    """if a button exists : scroll until it and click on it if its enable

    Args:
        webdriver (webdriver): the webdriver you are working on
        xpath_button (str): the xpath of the element you want to chek the presence
        y_gap (int): lenght of the gap to add to the position to scroll
    """
    if xpath_button != "":
        if check_exists_by_xpath(webdriver, xpath_button):
            display_button = webdriver.find_element(By.XPATH, xpath_button)
            x = display_button.location["x"]
            y = display_button.location["y"] - y_gap
            if display_button.is_enabled():
                webdriver.execute_script(f"""window.scrollTo({x}, {y})""")
                time.sleep(1)
                display_button.click()


def change_option(
    webdriver: webdriver, xpath: str, option: str, y_gap: int = 0
) -> None:
    if xpath != "":
        if check_exists_by_xpath(webdriver, xpath):
            display_button = webdriver.webdriver.find_element(By.XPATH, xpath)
            x = display_button.location["x"]
            y = display_button.location["y"] - y_gap
            if display_button.is_enabled():
                webdriver.execute_script(f"""window.scrollTo({x}, {y})""")
                time.sleep(1)
                op = Select(webdriver.webdriver.find_element(By.XPATH, xpath))
                op.select_by_visible_text(option)


def check_exists_by_xpath(webdriver: webdriver, xpath: str) -> bool:
    """check if a element exist or not on a actual webpage

    Args:
        webdriver (webdriver): the webdriver you are working on
        xpath (str): the xpath of the element you want to chek the presence

    Returns:
        bool: True if its present and False if not
    """
    try:
        webdriver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def get_text(webdriver: webdriver, xpath: str) -> str:
    """get the text of a element after check if it exists or not

    Args:
        webdriver (webdriver): the webdriver you are working on
        xpath (str):  the xpath of the element you want to extrat the text

    Returns:
        str: the tect on the element
    """
    if check_exists_by_xpath(webdriver, xpath):
        return webdriver.find_element(By.XPATH, xpath).text
    else:
        return ""


def add_several_elements(webdriver: webdriver, refs: list, storage: dict) -> dict:
    out = storage.copy()
    """search several information from refs in the actual webdriver and store it in storage

    Args:
        webdriver (webdriver): _description_
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
            clic(webdriver, ref["xpath"])
        else:
            try:
                content = get_text(webdriver, ref["xpath"])
            except Exception:
                content = "error"
                pass
            out[ref["name"]] = content
    return out


def extract_table(
    webdriver: webdriver, columns_refs: list, storage: list
) -> list:  # id: str,
    nb_element = 0
    dico = {}  # "code": id
    for column_ref in columns_refs:
        dico[column_ref["name"]] = ""
        new_nb = len(webdriver.find_elements(By.XPATH, column_ref["xpath"]))
        if new_nb > nb_element:
            nb_element = new_nb
    pre_out = [dico.copy() for _ in range(nb_element)]
    for _, column_ref in enumerate(columns_refs):
        content = webdriver.find_elements(By.XPATH, column_ref["xpath"])
        for i, x in enumerate(content):
            if column_ref["name"][:4] == "link":
                pre_out[i][column_ref["name"]] = x.get_attribute("href")
            else:
                pre_out[i][column_ref["name"]] = x.text
    return storage + pre_out
