from unittest import mock
from unittest.mock import MagicMock
import pytest
import datetime
from taskList.ext.site.task_list import *

def test_task_created_sucess(task_list):
    """ Test inserting a task operation success"""
    task_list.create_id = MagicMock(return_value=0)
    task_list.create_task("test", "testing")
    assert task_list.get_tasks() == {0:{"completed":False,"description":"testing","title":"test","deadline":None}}
    
def test_multiples_tasks_created_sucess(task_list):
    """ Test inserting a task operation success"""
    task_list.create_id = MagicMock(return_value=0)
    task_list.create_task("test1", "testing")
    task_list.create_id = MagicMock(return_value=1)
    task_list.create_task("test1", "testing")
    assert task_list.get_tasks() == {
        0:{
            "completed":False,
            "description":"testing",
            "title":"test1",
            "deadline":None
        },
        1:{
            "completed":False,
            "description":"testing",
            "title":"test1",
            "deadline":None
        },}
    
def test_unique_id_created_with_new_task(task_list):
    """ test the tasks creation of a Id """
    task_list.create_task("test1", "testing")
    task_list.create_task("test2", "testing")
    tasks = task_list.get_tasks()
    assert len(tasks.keys()) == 2
    
def test_complete_task_succesfully(task_list):
    """ test the completion of a task """
    task_list.create_id = MagicMock(return_value=0)
    task_list.create_task("test1", "testing")
    task_list.create_id = MagicMock(return_value=1)
    task_list.create_task("test2", "testing")
    task_list.complete_task(1)
    assert task_list.get_tasks() == { 
        0:{
            "completed":False,
            "description":"testing",
            "title":"test1",
            "deadline":None
        },
        1:{
           "completed":True,
            "description":"testing",
            "title":"test2",
            "deadline":None
        }
    }
    
def test_complete_multiple_task_succesfully(task_list):
    """ test the completion of a task """
    task_list.create_id = MagicMock(return_value=0)
    task_list.create_task("test1", "testing")
    task_list.create_id = MagicMock(return_value=1)
    task_list.create_task("test2", "testing")
    task_list.complete_task(1)
    task_list.complete_task(0)
    assert task_list.get_tasks() == { 
        0:{
            "completed":True,
            "description":"testing",
            "title":"test1",
            "deadline":None
        },
        1:{
           "completed":True,
            "description":"testing",
            "title":"test2",
            "deadline":None
        }
    }

    
def test_get_completed_tasks_only(task_list):
    """ test the completion of a task """
    task_list.create_id = MagicMock(return_value=0)
    task_list.create_task("test1", "testing")
    task_list.create_id = MagicMock(return_value=1)
    task_list.create_task("test2", "testing")
    task_list.create_id = MagicMock(return_value=2)
    task_list.create_task("test3", "testing")
    task_list.complete_task(1)
    task_list.complete_task(2)
    assert task_list.get_completed_task() == { 
        1:{
           "completed":True,
            "description":"testing",
            "title":"test2",
            "deadline":None
        },
        2:{
           "completed":True,
            "description":"testing",
            "title":"test3",
            "deadline":None
        }
    }
    
def test_get_uncompleted_tasks(task_list):
    """ test the completion of a task """
    task_list.create_id = MagicMock(return_value=0)
    task_list.create_task("test1", "testing")
    task_list.create_id = MagicMock(return_value=1)
    task_list.create_task("test2", "testing")
    task_list.create_id = MagicMock(return_value=2)
    task_list.create_task("test3", "testing")
    task_list.complete_task(1)
    task_list.complete_task(2)
    assert task_list.get_uncompleted_tasks() == { 
        0:{
            "completed":False,
            "description":"testing",
            "title":"test1",
            "deadline":None
        }
    }

def test_get_empty_list(task_list):
    assert task_list.get_tasks() == {}
    
def test_get_empty_list_completed(task_list):
    task_list.create_id = MagicMock(return_value=0)
    task_list.create_task("test1", "testing")
    assert task_list.get_completed_task() == {}
    
def test_get_empty_list_uncompleted(task_list):
    task_list.create_id = MagicMock(return_value=0)
    task_list.create_task("test1", "testing")
    task_list.complete_task(0)
    assert task_list.get_uncompleted_tasks() == {}

def test_task_should_update_title_when_it_is_edited(task_list):
    old_title:str = "test1"
    new_title:str = "new" + old_title
    task_list.create_id = MagicMock(return_value=0)

    task_list.create_task(old_title, "testing")
    task_list.edit_task(0, title=new_title)

    task = task_list.get_task_by_id(id=0)

    assert task["title"] == new_title

def test_task_should_not_update_title_when_it_is_not_edited(task_list):
    title:str = "test1"
    task_list.create_id = MagicMock(return_value=0)

    task_list.create_task(title, "testing")
    task_list.edit_task(0)

    task = task_list.get_task_by_id(id=0)

    assert task["title"] == title

def test_task_should_update_description_when_it_is_edited(task_list):
    old_description:str = "testing"
    new_description:str = "new" + old_description
    task_list.create_id = MagicMock(return_value=0)

    task_list.create_task("test1", old_description)
    task_list.edit_task(0, description=new_description)

    task = task_list.get_task_by_id(id=0)

    assert task["description"] == new_description

def test_task_should_not_update_description_when_it_is_not_edited(task_list):
    description:str = "testing"
    task_list.create_id = MagicMock(return_value=0)

    task_list.create_task("test1", description)
    task_list.edit_task(0)

    task = task_list.get_task_by_id(id=0)

    assert task["description"] == description

def test_task_should_update_completion_status_when_it_is_edited(task_list):
    task_list.create_id = MagicMock(return_value=0)

    task_list.create_task("test1", "testing")
    task_list.edit_task(0, completed=True)

    task = task_list.get_task_by_id(id=0)

    assert task["completed"] == True

def test_task_should_not_update_title_when_title_is_not_edited(task_list):
    task_list.create_id = MagicMock(return_value=0)

    task_list.create_task("test1", "testing")
    task_list.edit_task(0)

    task = task_list.get_task_by_id(id=0)

    assert task["completed"] == False

def test_editing_fails_when_title_is_empty(task_list):
    with pytest.raises(EmptyTitleException) as e_info:
            old_title:str = "test1"
            new_title:str = ""
            task_list.create_id = MagicMock(return_value=0)

            task_list.create_task(old_title, "testing")
            task_list.edit_task(0, title=new_title)

def test_task_without_deadline_has_no_urgency(task_list):
    task_list.create_id = MagicMock(return_value=0)

    task_list.create_task("test1", "testing")

    assert task_list.deadline_status(0) == "No time urgency"

def test_task_with_deadline_a_week_away_has_low_urgency(task_list):
    task_list.create_id = MagicMock(return_value=0)
    delta = datetime.timedelta(days=8)
    deadline = datetime.datetime.today() + delta

    task_list.create_task("test1", "testing", deadline)

    assert task_list.deadline_status(0) == "Low time urgency"

def test_task_with_deadline_three_days_away_has_medium_urgency(task_list):
    task_list.create_id = MagicMock(return_value=0)
    delta = datetime.timedelta(days=4)
    deadline = datetime.datetime.today() + delta

    task_list.create_task("test1", "testing", deadline)

    assert task_list.deadline_status(0) == "Medium time urgency"

def test_task_with_deadline_a_day_away_has_high_urgency(task_list):
    task_list.create_id = MagicMock(return_value=0)
    delta = datetime.timedelta(days=2)
    deadline = datetime.datetime.today() + delta

    task_list.create_task("test1", "testing", deadline)

    assert task_list.deadline_status(0) == "High time urgency"

def test_task_with_deadline_for_today_has_extreme_urgency(task_list):
    task_list.create_id = MagicMock(return_value=0)
    delta = datetime.timedelta(hours=12)
    deadline = datetime.datetime.today() + delta

    task_list.create_task("test1", "testing", deadline)

    assert task_list.deadline_status(0) == "Extreme time urgency"

def test_get_task_by_id_unknown_id_fail(task_list):
    task_id = task_list.create_task("Task 1", "Description")
    with pytest.raises(UnknownIdException):
        task_list.get_task_by_id("unknown_id")

def test_edit_task_unknown_id_multiple_fields_fail(task_list):
    task_id = task_list.create_task("Task 1", "Description")
    with pytest.raises(UnknownIdException):
        task_list.edit_task("unknown_id", title="Updated Title", description="Updated Description", completed=True)

def test_has_deadline(task_list):
    task_id = task_list.create_task("Task with Deadline", "Description", datetime.datetime(2023, 5, 31))
    assert task_list.has_deadline(task_id) == True

def test_dont_have_deadline(task_list):
    task_id2 = task_list.create_task("Task without Deadline", "Description")
    assert task_list.has_deadline(task_id2) == False


def test_task_past_deadline_is_delayed(task_list):
    task_list.create_id = MagicMock(return_value=0)
    delta = datetime.timedelta(hours=-12)
    deadline = datetime.datetime.today() + delta
    task_list.create_task("test1", "testing", deadline)
    assert task_list.deadline_status(0) == "Delayed"
    
def test_success_move_task_bin(task_list):
    task_list.create_id = MagicMock(return_value=0)
    task_list.create_task("test1", "testing")
    task_list.move_bin(0)
    assert task_list.get_tasks() == {}
    assert task_list.get_bin() == {0:{"completed":False,"description":"testing","title":"test1","deadline":None}} 

def test_raise_exception_move_empty_to_bin(task_list):
    with pytest.raises(EmptyListException) as e_info:
        task_list.move_bin(0)

def test_get_bin(task_list):
    task_list.create_id = MagicMock(return_value=0)
    task_list.create_task("test1", "testing")
    task_list.move_bin(0)
    assert task_list.get_bin() == {0:{"completed":False,"description":"testing","title":"test1","deadline":None}} 
    
def test_get_empty_bin(task_list):
    assert task_list.get_bin() == {}

def test_raise_exception_move_to_bin_id_not_found(task_list):
    with pytest.raises(UnknownIdException) as e_info:
        task_list.create_id = MagicMock(return_value=0)
        task_list.create_task("test1", "testing")
        task_list.move_bin(1)
        
def test_raises_has_deadline_unknown_id_failure(task_list):
    task_id = task_list.create_task("Task 1", "Description", deadline="2023-05-31")
    with pytest.raises(UnknownIdException):
        task_list.has_deadline("unknown_id")
        
def test_raises_has_deadline_empty_failure(task_list):
    with pytest.raises(EmptyListException):
        task_list.has_deadline("unknown_id")

def test_move_to_list_from_bin_fail_empty_bin(task_list):
    with pytest.raises(EmptyListException) as e_info:
        task_list.move_from_bin(1)

def test_move_to_list_from_bin_id_not_found(task_list):
    with pytest.raises(UnknownIdException) as e_info:
        task_list.create_id = MagicMock(return_value=0)
        task_list.create_task("test1", "testing")
        task_list.move_bin(0)
        task_list.move_from_bin(1)

def test_move_to_list_from_bin_success(task_list):
    task_list.create_id = MagicMock(return_value=0)
    task_list.create_task("test1", "testing")
    task_list.move_bin(0)
    task_list.move_from_bin(0)
    
def test_move_from_bin_unknown_id_empty_list(task_list):
    with pytest.raises(EmptyListException):
        task_list.move_from_bin("unknown_id")
    task_id = task_list.create_task("Task 1", "Description")
    task_list.move_bin(task_id)

    with pytest.raises(UnknownIdException):
        task_list.move_from_bin("unknown_id")
        

def test_delete_task_success(task_list):
    task_list.create_id = MagicMock(return_value=0)
    task_list.create_task("test1", "testing")
    task_list.move_bin(0)
    task_list.delete_task(0)
    assert task_list.get_bin() == {}

def test_raise_excepction_delete_task_empty_bin(task_list):
    with pytest.raises(EmptyListException) as e_info:
        task_list.delete_task(1)
        
def test_raise_excepction_delete_task_id_not_found(task_list):
    with pytest.raises(UnknownIdException) as e_info:
        task_list.create_id = MagicMock(return_value=0)
        task_list.create_task("test1", "testing")
        task_list.move_bin(0)
        task_list.delete_task(1)

def test_delete_task_from_bin(task_list):
    task_id = task_list.create_task("Task 1", "Description")
    task_list.move_bin(task_id)
    task_list.delete_task(task_id)
    assert task_list.get_bin() == {}
        
def test_edit_task_unknown_id_single_field_fail(task_list):
    task_id = task_list.create_task("Task 1", "Description")
    with pytest.raises(UnknownIdException):
        task_list.edit_task("unknown_id", title="Updated Title")

def test_get_task_by_id_success(task_list):
    task_id = task_list.create_task("Task 1", "Description")
    task = task_list.get_task_by_id(task_id)
    assert task['title'] == "Task 1"
    assert task['description'] == "Description"

