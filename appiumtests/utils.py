from appium import webdriver
from appium.options.android import uiautomator2
from dotenv import dotenv_values

config = dotenv_values(".env")
capabs_preset = dict(
    platformName=config["PLATFORM_NAME"],
    automationName="UIAutomator2",
    platformVersion=config["PLATFORM_VERSION"],
    deviceName=config["DEVICE_NAME"],
    appPackage='com.google.android.calculator',
    appActivity='com.android.calculator2.Calculator',
    noReset='true'
)

class DriverFactory:
    DEFAULT_EXECUTOR = '127.0.0.1:4723'
    def __init__(self, desired_capabs):
        self.caps = desired_capabs
            
    def get_new_driver(self)-> webdriver.webdriver.WebDriver:
        #Create a new driver when this is called
        try:
            driver = webdriver.Remote(self.DEFAULT_EXECUTOR, self.caps)
        except Exception as e:
            print('driver not created!!!')
            print(e)
        else:
            #Driver created successfully
            return driver