from flask import Blueprint, Response, request
from app import db
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import create_model, get_models_with_filters, validate_model

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict(), 200

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.post("/<goal_id>/tasks")
def create_task_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    data = request.get_json()
    task_ids = data.get("task_ids")

    goal.tasks = []

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)

    db.session.commit()

    return {"id": goal.id, "task_ids": task_ids}, 200

@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_list = [task.to_dict() for task in goal.tasks]
    return {"id": goal.id, "title": goal.title, "tasks": task_list}, 200