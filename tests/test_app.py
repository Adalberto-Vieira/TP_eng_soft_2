import pytest

# Fixture de setup para criar o aplicativo e o cliente
@pytest.fixture(scope="module")
def app_client():
    from taskList.app import create_app
    app = create_app()
    with app.test_client() as client:
        yield app, client

# Fixture de teardown para limpar recursos após os testes
@pytest.fixture(scope="module")
def cleanup(app_client):
    app, _ = app_client
    yield
    # Adicione qualquer lógica de limpeza necessária após os testes, se aplicável.

def test_app_created(app_client):
    app, _ = app_client
    assert app.name == "taskList.app"

def test_request_returns_404(app_client):
    _, client = app_client
    response = client.get("/non_existing_url")
    assert response.status_code == 404

def test_request_returns_200(app_client):
    _, client = app_client
    response = client.get("/")
    assert response.status_code == 200

def test_index(app_client):
    _, client = app_client
    response = client.get('/')
    assert response.status_code == 200

def test_create_task(app_client):
    _, client = app_client
    response = client.post('/create_task', data={'title': 'Task 1', 'description': 'Description 1'})
    assert response.status_code == 200

def test_get_tasks(app_client):
    _, client = app_client
    response = client.get('/get_tasks')
    assert response.status_code == 200
