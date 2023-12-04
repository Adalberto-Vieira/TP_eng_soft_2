# Trabalho Prático 


## Integrantes

- Adalberto Barbosa Vieira - https://github.com/Adalberto-Vieira
- Samai Soares Pereira - https://github.com/samai-s


## Task List APP

TaskList é um sistema de gerenciador de tarefas, uma aplicação web em que o usuário pode criar, visualizar, editar e deletas tarefas, em que cada tarefa possui seu título, sua descrição e seu status de conclusão.

## Tecnologias utilizadas
- Python: Linguagem de programação utilizada para a criação do sistema;
- Flask: Framework web utilizado para construir a aplicação web;
- HTML: Utilizado para a estrutura e o estilo das páginas web;
- pytest & Selenium: Biblioteca utilizada para escrever os testes do sistema;
- Docker: Plataforma de contêineres utilizada para facilitar a implantação e execução do sistema.

## Como rodar o Sistema

1. Certifique-se de ter o Docker instalado em sua máquina;
2. Construa a imagem do Docker com o seguinte comando:<br/>
    <em>'docker build -t flask:latest'<em/>
3. Execute o contâiner do Docker com o comando: <br/>
    <em>'docker run -p 5000:5000 flask'<em/>
4. Acesse a aplicação em seu navegador: http://localhost:5000.

## Como rodar para dev

1. Installe requirements-dev.txt e requirements.txt através do comando:<br/>
    <em>'pip install -r requirements.txt -r requirements-dev.txt'<em/>
2. Configure a variável de ambiente para ativar o modo de depuração do Flask;
3. Execute <em>'flask run'<em/> dentro de task list.

## Como rodar testes

1. Installe requirements-dev.txt e requirements.txt através do comando:<br/>
    <em>'pip install -r requirements.txt -r requirements-dev.txt'<em/>
2. - Rode <em>'run pytest tests/'<em/> dentro da pasta raiz para os testes de unidade.
    - Rode <em>'system_test/test_e2e.py'<em/> dentro da pasta raiz para os testes de sistema.
