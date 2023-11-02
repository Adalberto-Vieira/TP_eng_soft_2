import pytest
import sys
import os

# Adds module path to env var
# TODO change this to a instalable module (setup.py)
myPath = os.path.dirname(os.path.abspath(__file__))
print(myPath)
sys.path.append( myPath + '/../taskList/')

from taskList.app import create_app
from taskList.ext.site.task_list import TaskList

@pytest.fixture(scope="module")
def app():
    """ Returns a instance of the main app """
    return create_app()

@pytest.fixture(scope="function")
def task_list():
    """ Returns a task list """
    return TaskList()