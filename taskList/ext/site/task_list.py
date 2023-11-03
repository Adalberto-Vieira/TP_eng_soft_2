import uuid
import datetime

class EmptyTitleException(Exception):
    pass

class UnknownIdException(Exception):
    pass

class EmptyListException(Exception):
    pass

class TaskList:
    def __init__(self):
        self.task_list = {}
        self.task_bin = {}

    def create_task(self, title: str, description: str, deadline=None):
        if not title:
            raise EmptyTitleException("Missing title for task")
        
        task_id = self.create_id()
        self.task_list[task_id] = {
            'title': title,
            'description': description,
            'completed': False,
            'deadline': deadline
        }
        return task_id

    def create_id(self):
        return str(uuid.uuid4())
    
    def edit_task(self, id, title:str, description:str, completed:bool) -> None:
        """ Alters task data """
        try:
            if title is not None:
                if title == "":
                    raise EmptyTitleException("Task must have a title")
                self.task_list[id]['title'] = title

            self.task_list[id]['description'] = description

            self.task_list[id]['completed'] = completed
        except KeyError:
            print(self.task_list)
            raise UnknownIdException()
            
    def get_task_by_id(self, id):
        """ Return task by id """
        try:
            return self.task_list[id]
        except KeyError:
            raise UnknownIdException()

        task = self.task_list[task_id]

        if title is not None and title.strip() == "":
            raise EmptyTitleException("Task must have a title")

        if title is not None:
            task['title'] = title
        if description is not None:
            task['description'] = description
        if completed is not None:
            task['completed'] = completed

    def get_task_by_id(self, task_id):
        if task_id not in self.task_list:
            raise UnknownIdException()
        return self.task_list[task_id]

    def complete_task(self, task_id):
        if task_id not in self.task_list:
            raise UnknownIdException()
        self.task_list[task_id]['completed'] = True

    def get_tasks(self):
        return self.task_list

    def get_uncompleted_tasks(self):
        return {task_id: task for task_id, task in self.task_list.items() if not task['completed']}

    def get_completed_tasks(self):
        return {task_id: task for task_id, task in self.task_list.items() if task['completed']}

    def has_deadline(self, task_id):
        if not self.task_list:
            raise EmptyListException()
        if task_id not in self.task_list:
            raise UnknownIdException()
        return self.task_list[task_id]["deadline"] is not None

    def deadline_status(self, task_id):
        if task_id not in self.task_list:
            raise UnknownIdException()

        task = self.task_list[task_id]

        if not self.has_deadline(task_id):
            return "No time urgency"

        settings = [
            (datetime.timedelta(days=7), "Low time urgency"),
            (datetime.timedelta(days=3), "Medium time urgency"),
            (datetime.timedelta(hours=24), "High time urgency"),
            (datetime.timedelta(), "Extreme time urgency")
        ]

        now = datetime.datetime.today()
        ret = None

        for k, v in settings:
            ret = v
            if task["deadline"] - now >= k:
                return ret

        return "Delayed"

    def delete_task(self, task_id):
        if not self.task_bin:
            raise EmptyListException()

        if task_id not in self.task_bin:
            raise UnknownIdException()

        self.task_bin.pop(task_id)

    def move_bin(self, task_id):
        if not self.task_list:
            raise EmptyListException()

        if task_id not in self.task_list:
            raise UnknownIdException()

        self.task_bin[task_id] = self.task_list[task_id]
        self.task_list.pop(task_id)

    def get_bin(self):
        return self.task_bin

    def move_from_bin(self, task_id):
        if not self.task_bin:
            raise EmptyListException()

        if task_id not in self.task_bin:
            raise UnknownIdException()

        self.task_list[task_id] = self.task_bin[task_id]
        self.task_bin.pop(task_id)
