import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class SystemTestCase(unittest.TestCase):
    def setUp(self):
        options = ChromiumOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def tearDown(self):
        self.driver.quit()

    def add_task_to_list(self):
        title_input = self.driver.find_element('css selector', 'input[name="title"]')
        description_input = self.driver.find_element('css selector', 'input[name="description"]')
        submit_button = self.driver.find_element('css selector', 'input[type="submit"]')

        title_input.send_keys('Test Task')
        description_input.send_keys('This is a test task')
        submit_button.click()
        
        time.sleep(2)

    def test_create_task(self):
        self.driver.get('http://127.0.0.1:5000/')
        time.sleep(2)

        self.add_task_to_list()
        
        task_element = self.driver.find_element('css selector', '.list-group-item')
        self.assertTrue(task_element.is_displayed(), 'A nova tarefa não está visível na lista.')

    def test_edit_task(self):
        self.driver.get('http://127.0.0.1:5000/')
        time.sleep(2)

        task_element = self.driver.find_element('css selector', '.list-group-item')

        task_element.click()
        time.sleep(2)

        edit_title_input = self.driver.find_element('xpath', '/html/body/div/div/div[3]/ul/li/form[1]/input[1]')
        edit_description_input = self.driver.find_element('xpath', '/html/body/div/div/div[3]/ul/li/form[1]/input[2]')

        edit_title_input.send_keys(Keys.CONTROL + 'a')
        edit_title_input.send_keys(Keys.DELETE)
        edit_description_input.send_keys(Keys.CONTROL + 'a')
        edit_description_input.send_keys(Keys.DELETE)

        edited_title = 'Edited Task'
        edited_description = 'This task has been edited'
        edit_title_input.send_keys(edited_title)
        edit_description_input.send_keys(edited_description)


        edit_submit_button = self.driver.find_element('xpath', '/html/body/div/div/div[3]/ul/li[1]/form[1]/input[4]')
        edit_submit_button.click()
        time.sleep(2)

        edited_task_element = self.driver.find_element('css selector', '.list-group-item:first-child')
        edited_task_title = edited_task_element.find_element('css selector', 'h5').text
        edited_task_description = edited_task_element.find_element('css selector', 'p.mb-1').text

        self.assertEqual(edited_task_title, edited_title, 'O título da tarefa não foi editado corretamente.')
        self.assertEqual(edited_task_description, edited_description, 'A descrição da tarefa não foi editada corretamente.')

    def test_move_to_bin(self):
        self.driver.get('http://127.0.0.1:5000/')
        time.sleep(2)

        task_id_input = self.driver.find_element('id', 'id')
        task_id = task_id_input.get_attribute('value')

        bin_button = self.driver.find_element('xpath', "//button[contains(text(), 'Move to bin')]")
        bin_button.click()
        time.sleep(2)

        list_elements = self.driver.find_elements('css selector', '.list-group-item')
        list_ids = [element.get_attribute('id') for element in list_elements]
        self.assertNotIn(task_id, list_ids, 'A tarefa não foi removida da lista principal.')

    def test_move_from_bin(self):
        self.driver.get('http://127.0.0.1:5000/')
        time.sleep(2)

        bin_id_input = self.driver.find_element('xpath', '/html/body/div/div/div[5]/ul/li/p[1]')
        bin_id = bin_id_input.get_attribute('value')

        move_from_bin_button = self.driver.find_element('xpath', "//button[contains(text(), 'Move from bin')]")
        move_from_bin_button.click()
        time.sleep(2)

        list_elements = self.driver.find_elements('css selector', '.list-group-item')
        list_ids = [element.get_attribute('id') for element in list_elements]
        self.assertNotIn(bin_id, list_ids, 'A tarefa não foi removida para a lista principal.')

        bin_button = self.driver.find_element('xpath', "//button[contains(text(), 'Move to bin')]")
        bin_button.click()

    def test_delete(self):
        self.driver.get('http://127.0.0.1:5000/')
        time.sleep(2)

        delete_id_input = self.driver.find_element('xpath', '/html/body/div/div/div[5]/ul/li/p[1]')
        delete_id = delete_id_input.get_attribute('value')
        time.sleep(2)

        delete_button = self.driver.find_element('xpath', "//button[contains(text(), 'Delete')]")
        delete_button.click()
        time.sleep(2)

        list_elements = self.driver.find_elements('css selector', '.list-group-item')
        list_ids = [element.get_attribute('id') for element in list_elements]
        self.assertNotIn(delete_id, list_ids, 'O item não foi deletado.')
    
    def test_complete_task(self):
        self.driver.get('http://127.0.0.1:5000/')
        time.sleep(2)

        self.add_task_to_list()

        complete_button = self.driver.find_element('xpath', "//button[contains(text(), 'Complete')]")
        complete_button.click()
        time.sleep(2)

        completed_task_element = self.driver.find_element('css selector', '.list-group-item.completed:first-child')
        self.assertTrue(completed_task_element.is_displayed(), 'The task is not marked as completed.')

    def test_filter_completed_tasks(self):
        self.driver.get('http://127.0.0.1:5000/')
        time.sleep(2)

        self.add_task_to_list()

        complete_button = self.driver.find_element('xpath', "//button[contains(text(), 'Complete')]")
        complete_button.click()
        time.sleep(2)
        completed_filter_button = self.driver.find_element('xpath', "//button[contains(text(), 'Completed Tasks')]")
        completed_filter_button.click()
        time.sleep(2)

        completed_tasks_list = self.driver.find_elements('css selector', '.list-group-item.completed')
        self.assertTrue(completed_tasks_list, 'No completed tasks are displayed in the completed tasks list.')

    def test_clear_completed_tasks(self):
        self.driver.get('http://127.0.0.1:5000/')
        time.sleep(2)

        self.add_task_to_list()

        complete_button = self.driver.find_element('xpath', "//button[contains(text(), 'Complete')]")
        complete_button.click()
        time.sleep(2)

        clear_completed_button = self.driver.find_element('xpath', "//button[contains(text(), 'Clear Completed')]")
        clear_completed_button.click()
        time.sleep(2)

        completed_tasks_list = self.driver.find_elements('css selector', '.list-group-item.completed')
        self.assertFalse(completed_tasks_list, 'Completed tasks are still present in the list after clearing.')


if __name__ == '__main__':
    # Cria uma suíte de testes
    test_suite = unittest.TestSuite()

    # Adiciona os testes à suíte na ordem desejada
    test_suite.addTest(SystemTestCase('test_create_task'))
    test_suite.addTest(SystemTestCase('test_edit_task'))
    test_suite.addTest(SystemTestCase('test_move_to_bin'))
    test_suite.addTest(SystemTestCase('test_move_from_bin'))
    test_suite.addTest(SystemTestCase('test_delete'))

    # Executa a suíte de testes
    unittest.TextTestRunner().run(test_suite)
