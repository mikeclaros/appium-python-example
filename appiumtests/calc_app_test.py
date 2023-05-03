import unittest
from appium import webdriver as Awebdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium import webdriver as Swebdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.common.exceptions import TimeoutException
from utils import DriverFactory, capabs_preset


class TestAppium(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = DriverFactory(capabs_preset).get_new_driver()
        self.operator_test_list = {
            'add': [[1, 'plus', 2, 'equals', '3'], [0, 'plus', 9, 'equals', '9']],
            'sub': [[1, 'minus', 2, 'equals', '-1'], [0, 'minus', 9, 'equals', '-9']],
            'mult': [[1, 'multiply', 2, 'equals', '2'], [0, 'multiply', 9, 'equals', '0']],
            'div': [[1, 'divide', 2, 'equals', '0.5'], [0, 'divide', 9, 'equals', '0']]
        }
        self.syntax_list = [
            ['point', 'plus', '1', 'equals'],
            ['point', 'minus', '1', 'equals'],
            ['point', 'pi','plus','1', 'equals']
        ]

    def tearDown(self) -> None:
        self.reset_calc_state()
        if self.driver:
            self.driver.quit()

    def helper_wait_function(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((AppiumBy.ID, 'com.google.android.calculator:id/formula')))
        except TimeoutException as e:
            print(e)

    def test_ID01_Op_Function_Apply_Op_On_Numbers(self) -> None:
        # 1. press a number
        # 2. press op sign
        # 3. press a number
        # 4. press equal sign
        
        self.helper_wait_function()

        for key in self.operator_test_list:
            test_cases_data = self.operator_test_list[key]
            for test in test_cases_data:
                for index in range(4):
                    value = test[index]
                    self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=str(value)).click()
                with self.subTest(msg="Checking operator functionality of " + key):
                    expected = test[4]
                    actual = self.driver.find_element(by=AppiumBy.ID, value='com.google.android.calculator:id/result_final').text 
                    #calculator minus results return this ascii -> U+2212 need to handle this case
                    if '−' in actual: actual = actual.replace('−', '-')
                    self.assertEqual(actual, expected)
    
    def test_ID02_Syntax_Error_Returns_Error_Message(self) -> None:
        # 1. press dot
        # 2. press an op button
        # 3. press a number
        # 4. press equal
        self.helper_wait_function()
        expected = "Format error"
        for test in self.syntax_list:
            for op in test:
                self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=op).click()
            with self.subTest(msg="Checking syntax error is shown"):
                actual = self.driver.find_element(by=AppiumBy.ID, value="com.google.android.calculator:id/result_preview").text
                self.assertEqual(actual, expected)
            #clear the screen for next test case
            self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='clear').click()

    def test_ID03_History_Is_Listed(self) -> None:
        # 1. input an expr
        # 2. drag history tray down
        # 3. check exp

        self.helper_wait_function()
        data = self.operator_test_list['add']
        expr_list = []
        for seq in data:
            for index in range(4):
                op = str(seq[index])
                self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=op).click()
                if index == 2:
                    expr = self.driver.find_element(by=AppiumBy.ID, value='com.google.android.calculator:id/formula').text
                    output = self.driver.find_element(by=AppiumBy.ID, value='com.google.android.calculator:id/result_preview').text
                    expr_list.append(expr)
                    expr_list.append(output)
        
        self.swipe_helper()
        try:
            container = self.driver.find_elements(by=AppiumBy.ID, value='com.google.android.calculator:id/history_recycler_view')
            linear_layout_list = container[0].find_elements(by= AppiumBy.CLASS_NAME, value='android.widget.LinearLayout')

            index = 0
            for linear_layout in linear_layout_list:
                elements = linear_layout.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')
                for element in elements:
                    if element.text == 'Today':
                        continue
                    with self.subTest('Checking history matches'):
                        actual = element.text
                        expected = expr_list[index]
                        self.assertEqual(actual, expected)
                    index = index + 1         
        except Exception as e:
            print(e)
        
    def test_ID04_Clear_Removes_History(self) -> None:
        # 1. input an expr
        # 2. drag history tray
        # 3. tap on ellipses
        # 4. clear history

        self.helper_wait_function()
        seq = self.operator_test_list['add'][0]

        for index in range(4):
            op = str(seq[index])
            self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=op).click()
        
        # Clear history
        self.swipe_helper()
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='More options').click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.LinearLayout')))
        self.driver.find_element(by=AppiumBy.ID, value='com.google.android.calculator:id/content').click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((AppiumBy.ID, 'android:id/content')))
        self.driver.find_element(by=AppiumBy.ID, value='android:id/button1').click()


        self.swipe_helper()
        empty_history_view = self.driver.find_elements(by=AppiumBy.ID, value='com.google.android.calculator:id/empty_history_view')
        self.assertNotEqual(len(empty_history_view), 0)



        
        
    
    def swipe_helper(self) -> None:
        try:
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((AppiumBy.ID, 'com.google.android.calculator:id/drag_handle_view')))
        except TimeoutException as e:
            print(e)
        handle = self.driver.find_element(by=AppiumBy.ID, value="com.google.android.calculator:id/drag_handle_view")
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "finger"))
        actions.w3c_actions.pointer_action.click_and_hold(handle)

        x = handle.location['x']
        y = 20
        actions.w3c_actions.pointer_action.move_to_location(x,y)
        while y < 1800:
            if y > 1000:
                x = x
            else:
                x = (x*2) - x
            actions.w3c_actions.pointer_action.move_to_location(x,y)
            y = y + 375

        actions.perform()
    

    def reset_calc_state(self) -> None:
         #check that program is not already at the history page
        is_history_bar_present = len(self.driver.find_elements(by=AppiumBy.ID, value='com.google.android.calculator:id/history_layout'))
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='More options').click()       
        if is_history_bar_present == 0:     
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.LinearLayout')))
            container = self.driver.find_element(by=AppiumBy.CLASS_NAME, value='android.widget.ListView')
            list_linear_layout = container.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.LinearLayout')
            list_linear_layout[0].click()

            history_toolbar = self.driver.find_element(by=AppiumBy.ID, value='com.google.android.calculator:id/history_toolbar')
            history_toolbar.find_element(by=AppiumBy.CLASS_NAME, value='android.widget.ImageView').click()

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((AppiumBy.ID, 'com.google.android.calculator:id/title')))
        self.driver.find_element(by=AppiumBy.ID, value='com.google.android.calculator:id/title').click()

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((AppiumBy.ID, 'android:id/content')))
        self.driver.find_element(by=AppiumBy.ID, value='android:id/button1').click()






if __name__ == '__main__':
    unittest.main()
