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

        # Localize uma tarefa existente na lista
        task_element = self.driver.find_element('css selector', '.list-group-item')


        # Clique na tarefa para abrir o formulário de edição
        task_element.click()
        time.sleep(2)

        # Localize os campos de texto de edição
        edit_title_input = self.driver.find_element('xpath', '/html/body/div/div/div[3]/ul/li/form[1]/input[1]')
        edit_description_input = self.driver.find_element('xpath', '/html/body/div/div/div[3]/ul/li/form[1]/input[2]')


        # Selecione o texto existente e exclua-o
        edit_title_input.send_keys(Keys.CONTROL + 'a')
        edit_title_input.send_keys(Keys.DELETE)
        edit_description_input.send_keys(Keys.CONTROL + 'a')
        edit_description_input.send_keys(Keys.DELETE)

        # Insira os novos valores nos campos de texto
        edited_title = 'Edited Task'
        edited_description = 'This task has been edited'
        edit_title_input.send_keys(edited_title)
        edit_description_input.send_keys(edited_description)

        # Envie o formulário de edição

        edit_submit_button = self.driver.find_element('xpath', '/html/body/div/div/div[3]/ul/li[1]/form[1]/input[4]')
        edit_submit_button.click()
        time.sleep(2)

        # Verifique se a tarefa foi editada corretamente
        edited_task_element = self.driver.find_element('css selector', '.list-group-item:first-child')
        edited_task_title = edited_task_element.find_element('css selector', 'h5').text
        edited_task_description = edited_task_element.find_element('css selector', 'p.mb-1').text

        self.assertEqual(edited_task_title, edited_title, 'O título da tarefa não foi editado corretamente.')
        self.assertEqual(edited_task_description, edited_description, 'A descrição da tarefa não foi editada corretamente.')

    def test_move_to_bin(self):
        # Abrir a página inicial do aplicativo
        self.driver.get('http://127.0.0.1:5000/')
        time.sleep(2)


         # Obter o ID da tarefa antes de movê-la para a lixeira
        task_id_input = self.driver.find_element('id', 'id')
        task_id = task_id_input.get_attribute('value')

        # Clicar no botão "Move to bin"
        bin_button = self.driver.find_element('xpath', "//button[contains(text(), 'Move to bin')]")
        bin_button.click()
        time.sleep(2)

        # Verificar se a tarefa foi removida da lista principal
        list_elements = self.driver.find_elements('css selector', '.list-group-item')
        list_ids = [element.get_attribute('id') for element in list_elements]
        self.assertNotIn(task_id, list_ids, 'A tarefa não foi removida da lista principal.')

    def test_move_from_bin(self):
        # Abrir a página inicial do aplicativo
        self.driver.get('http://127.0.0.1:5000/')
        time.sleep(2)

        # Obter o ID da tarefa antes de voltar para uncompleted
        bin_id_input = self.driver.find_element('xpath', '/html/body/div/div/div[5]/ul/li/p[1]')
        bin_id = bin_id_input.get_attribute('value')

        # Clicar no botão "Move from bin"
        move_from_bin_button = self.driver.find_element('xpath', "//button[contains(text(), 'Move from bin')]")
        move_from_bin_button.click()
        time.sleep(2)

        # Verificar se a tarefa foi retornada para a lista principal
        list_elements = self.driver.find_elements('css selector', '.list-group-item')
        list_ids = [element.get_attribute('id') for element in list_elements]
        self.assertNotIn(bin_id, list_ids, 'A tarefa não foi removida para a lista principal.')

        #move de volta pra lixeira
        bin_button = self.driver.find_element('xpath', "//button[contains(text(), 'Move to bin')]")
        bin_button.click()

    def test_delete(self):
        # Abrir a página inicial do aplicativo
        self.driver.get('http://127.0.0.1:5000/')
        time.sleep(2)

        # Obter o ID do item antes de deleta-lo
        delete_id_input = self.driver.find_element('xpath', '/html/body/div/div/div[5]/ul/li/p[1]')
        delete_id = delete_id_input.get_attribute('value')
        time.sleep(2)

        # Clicar no botão "Delete"
        delete_button = self.driver.find_element('xpath', "//button[contains(text(), 'Delete')]")
        delete_button.click()
        time.sleep(2)

        # Verificar se o ID do item foi deletado
        list_elements = self.driver.find_elements('css selector', '.list-group-item')
        list_ids = [element.get_attribute('id') for element in list_elements]
        self.assertNotIn(delete_id, list_ids, 'O item não foi deletado.')


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
