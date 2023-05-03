from appiumtests.utils import DriverFactory, desired_cap_preset
from appium import webdriver

import unittest
import warnings


class TestUtils(unittest.TestCase):
    driverObj = None

    def setUp(self):
        try:
            self.driver = DriverFactory(desired_cap_preset)
        except Exception as e:
            print(e)
    
    def tearDown(self):
        if self.driverObj != None:
            self.driverObj.quit()
        
        del self.driverObj

    def __get_helper(self, driver):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            return driver.get_new_driver()
        
    def test_Driver_Returns_WebDriver(self):
        arg = self.driver
        self.driverObj = self.__get_helper(arg)
        self.assertIsInstance(self.driverObj, webdriver.webdriver.WebDriver)
    
    @unittest.expectedFailure
    def test_Driver_Returns_Fail_On_Invalid_Capabilities(self):
        # misspelled noReset to force invalid preset
        tmp_cap_preset = {
            'platformVersion': '8.1.0',
            'deviceName': 'LGStylo4',
            'noRest': 'true'
        }
        tmp = DriverFactory(tmp_cap_preset)
        self.driverObj = self.__get_helper(tmp)
        print("Driver is", self.driverObj)
        self.assertIsInstance(self.driverObj, webdriver.webdriver.WebDriver, "Should not be webdriver.")



    
    

if __name__ == '__main__':
    unittest.main(verbosity=2)