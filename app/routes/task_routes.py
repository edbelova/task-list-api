import os
import requests

from app import db
from app.models.task import Task
from datetime import datetime
from flask import Blueprint, Response, request, current_app
from app.routes.route_utilities import create_model, get_models_with_filters, validate_model

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

    response = send_slack_message(None, f"Someone just completed the task {task.title}")

    if response is None:
        try:
            current_app.logger.error("Slack request failed with an exception; no response returned")
        except Exception:
            pass
        return Response(status=500, mimetype="application/json")

    # Slack may return 200 but contain { "ok": false } in the JSON body.
    try:
        ok = response.json().get("ok", False)
    except ValueError:
        ok = False

    if response.status_code != 200 or not ok:
        try:
            current_app.logger.error(
                "Slack post failed: status=%s, body=%s",
                response.status_code,
                response.text,
            )
        except Exception:
            pass
        return Response(status=500, mimetype="application/json")

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def patch_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return Response(status=204, mimetype="application/json")
    
def send_slack_message(channel, text):

    token = os.environ.get("SLACKBOT_TOKEN")
    if not token:
        try:
            current_app.logger.error("SLACKBOT_TOKEN is missing or empty")
        except Exception:
            pass

    if channel is None:
        channel = os.environ.get("SLACK_CHANNEL")

    try:
        return requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
            },
            json={
                "channel": channel,
                "text": text,
            },
        )
    except requests.RequestException:
        return None