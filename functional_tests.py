from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase): 

    def setUp(self): 
        self.browser = webdriver.Firefox()

    def tearDown(self): 
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Edith has heard about a coll new online to-do app. She goes
        #to check out its homepage
        self.browser.get('http://localhost:8000')

        #She notices the page tile and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)      
        header_text = self.browser.find_element_by_tag_name('h1').text #1
        self.assertIn('To-Do', header_text)   

        #She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item') #1
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #She types "Buy peacock feathers" into de text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers') #2

        #When she hits entre, the page updates, and now the page lists
        #"1: Buy peacock feathers" as on item in a to-do list
        inputbox.send_keys(Keys.ENTER) #3
        time.sleep(1) #4

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr') #1
        self.assertTrue(
            any(row.text =='1: Buy peacock feathers' for row in rows),
            "New to-do item did not appear in table"
        )

        #There is still a text box inviting her to add another item. She
        #enters "Use peacock feathers to make a fly" (Edith is very methodical)
        self.fail('Finish the test!')

        #The page updates again, and now shows doth items on her list

        #Edith wonders wheter the site will remember her list. Then she sees
        #taht the site has generated a unique URL for her -- ther is some
        #explanatory text to that effect.

        #She visits that URL - her to-do list is still there.

        #Satisfied, she goes back to sleep

if __name__ == '__main__': #6
    unittest.main() #7