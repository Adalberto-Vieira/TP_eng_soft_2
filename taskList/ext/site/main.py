from flask import Blueprint, render_template, make_response, jsonify, request
from .task_list import TaskList

bp = Blueprint("site", __name)
task_list = TaskList()

def render_index(warning=False):
    return render_template("index.html", 
                            uncompleted_tasks=task_list.get_uncompleted_tasks(),
                            completed_task=task_list.get_completed_task(),
                            bin=task_list.get_bin(),
                            warning=warning)

@bp.route("/")
def index():
    return render_index()

@bp.route("/create_task", methods=['POST'])
def create_task():
    warning = False
    try:
        task_list.create_task(request.form.get('title'), request.form.get('description'))
    except:
        warning = True
    return render_index(warning)

@bp.route("/get_tasks")
def get_tasks():
    tasks = task_list.get_tasks()
    if tasks:
        return make_response(jsonify(tasks), 200)
    else:
        return make_response("No tasks added", 204)

@bp.route("/edit_task/", methods=['POST'])
def edit_task():
    try:
        task_list.edit_task(request.form.get("id"), request.form.get("title"),
                            request.form.get("description"), bool(int(request.form.get("status"))
                            ))
    except:
        pass
    return render_index()

@bp.route("/move_bin/<id>", methods=['POST'])
def move_bin(id):
    task_list.move_bin(id)
    return render_index()

@bp.route("/move_from_bin/<id>", methods=['POST'])
def move_from_bin(id):
    task_list.move_from_bin(id)
    return render_index()

@bp.route("/delete/<id>", methods=['POST'])
def delete(id):
    task_list.delete_task(id)
    return render_index()

@bp.route("/set_date_time/<id>", methods=['POST'])
def set_date_time(id):
    return render_index()
