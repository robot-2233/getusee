from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from .cupdate import WebdriverAutoUpdate
from .traversement import *
from .common import *
import time
import subprocess


# cd C:\Users\Administrator\AppData\Local\Google\Chrome\Application
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"

class smart_driver():
    by_choices = {'id': By.ID,
                  'class': By.CLASS_NAME,
                  'css': By.CSS_SELECTOR,
                  'xpath': By.XPATH}

    def __init__(self, debug: bool = True, invisible: bool = True, port: str = '9222', update: bool = False) -> None:
        super(smart_driver, self).__init__()

        self.port = str(port)
        self.debug = debug
        self.sys = see_system()
        self.options = webdriver.ChromeOptions()
        self.chrome_options = webdriver.ChromeOptions()

        self.chrome_driver_path = get_chromedriver_path(self.sys)
        if update:
            path = sys.executable
            driver_directory = path.rsplit('\\', 1)[0] if '\\' in path else path
            WebdriverAutoUpdate(driver_directory)
        if not debug:
            prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
            self.chrome_options.add_experimental_option("prefs", prefs)
            if invisible:
                self.chrome_options.add_argument('headless')
            self.options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
            self.driver = webdriver.Chrome(options=self.options, chrome_options=self.chrome_options, executable_path=self.chrome_driver_path)
        else:
            if is_port_in_use(port=port):
                print('[INFO]: Already driving...')
                self.options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
                self.driver = webdriver.Chrome(options=self.options, executable_path=self.chrome_driver_path)
            else:
                chrome_path = get_chrome_path(self.sys)
                chrome_cmd = [chrome_path, '--remote-debugging-port=9222',
                              '--user-data-dir=C:\selenum\AutomationProfile']  # Custom browser user path
                subprocess.Popen(chrome_cmd)
                self.options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
                self.driver = webdriver.Chrome(options=self.options, executable_path=self.chrome_driver_path)

    def __repr__(self):
        return f'Chrome Driver in {self.port}'

    def get_url(self, url: str):
        """
        Opens the specified URL in the web browser.

        Args:
            url (str): The URL to open in the web browser.

        Returns:
            None
        """
        self.driver.get(url)

    def make_sure(self, sleep_time=3):
        """
        Waits for a specified duration to ensure elements have time to load.

        Args:
            sleep_time (int, optional): The duration to wait in seconds. Default is 3 seconds.

        Returns:
            None
        """
        self.driver.implicitly_wait(sleep_time)
        time.sleep(sleep_time - 2)

    def get_some_text(self, key: str, single: bool = True):
        """
        Gets the text of the matching element.

         Args:
             key (str): Keyword to match.
             single (bool, optional): Whether to get only the text of a single matching element. Default is True.

         Returns:
             Union[str, List[str]]: If single is True, returns the text of a single element; if single is False, returns a list of element texts.
        """
        if single:
            return traverse(self.driver, key).text
        else:
            elements_list = []
            for matched_element in traverse_all(self.driver, key):
                elements_list.append(matched_element.text)
            return elements_list

    def click_something(self, key: str, single: bool = True):
        """
       Clicks the matching element(s).

       Args:
           key (str): Keyword to match.
           single (bool, optional): Whether to click only a single matching element. Default is True.

       Returns:
           None
       """
        if single:
            traverse(self.driver, key).click()
        else:
            for matched_element in traverse_all(self.driver, key):
                matched_element.click()

    def input_word(self, label: str, input_word: str, multiselect: int = 0, method='CLASS_NAME'):
        """
        Input text into a web page input field.

        Args:
            label (str): The label or identifier to locate the input field.
            input_word (str): The text to be entered into the input field.
            multiselect (int, optional): Index to select among multiple matching input fields (default is 0).
            method (str, optional): The method to locate the input field, either 'CLASS_NAME' (default), 'ID', or other.

        Returns:
            None

        Notes:
            This function locates an input field on a web page using the specified method and label.
            If multiple matching input fields are found, the function selects one based on the 'multiselect' index.
            The 'input_word' is then entered into the selected input field.
        """
        if method == 'CLASS_NAME':
            elements = class_server(self.driver, label)
            if len(elements) > 1:
                if self.debug:
                    print('Match multiple tags, use multiselect')
                elements[multiselect].send_keys(input_word)
            else:
                elements[0].send_keys(input_word)
        elif method == 'ID':
            element = self.driver.find_element(value=label, by=By.ID)
            element.send_keys(input_word)
        else:
            print('wait what?')
            elements = sniffer(self.driver, label)
            if len(elements) > 1:
                if self.debug:
                    print('Match multiple tags, use multiselect')
                elements[multiselect].send_keys(input_word)
            else:
                elements[0].send_keys(input_word)

    def get_soup(self) -> BeautifulSoup:
        """
       Returns a BeautifulSoup object representing the current page's HTML.

       Returns:
           BeautifulSoup: A BeautifulSoup object containing the parsed HTML of the current page.
       """
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        return soup

    def sniff(self, value, by):
        b = self.by_choices.get(by)
        return self.driver.find_element(value=value, by=b)

    def sniffs(self, value, by):
        b = self.by_choices.get(by)
        return self.driver.find_elements(value=value, by=b)

    def enter_iframe(self, index):
        self.driver.switch_to.frame(index)

    def roll(self, direct, level=0):
        self.driver.execute_script(f'window.scrollBy({level},{direct})')

    def roll_to(self, ele_text):
        # scroll_add_crowd_button = driver.find_element_by_xpath(xpath_button_add_crowd)
        ele = self.driver.find_element(By.CSS_SELECTOR,ele_text)
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)

    def bye(self):
        """
        Quits the web browser driver, closing all associated windows.

        Returns:
            None
        """
        self.driver.quit()


