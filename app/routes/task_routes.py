from flask import Blueprint, abort, make_response, request, current_app
import os
from app import db
from app.models.task import Task
from flask import Response
from datetime import datetime

from app.routes.route_utilities import create_model, get_models_with_filters, validate_model

# Config from environment
SLACKBOT_TOKEN = os.getenv("SLACKBOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict(), 200

@bp.patch("/<task_id>/mark_complete")
def patch_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()

    db.session.commit()

    send_slack_message(SLACK_CHANNEL, f"OMG task '{task.title}' has been completed. Congrats!", SLACKBOT_TOKEN)

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def patch_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return Response(status=204, mimetype="application/json")
    
def send_slack_message(channel, text, token):
    request.post(
        "https://slack.com/api/chat.postMessage", 
        headers={"Authorization": f"Bearer {token}"}, 
        json={
            "channel": channel,
            "text": text
        }
    )