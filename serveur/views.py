from flask import jsonify, abort, make_response, request, url_for
from .app import app, db
from .models import *

def make_public_questionnaire(questionnaire):
    new_questionnaire = {}
    questionnaire_json = questionnaire.to_json()
    for field in questionnaire_json:
        if field == "id":
            new_questionnaire["uri"] = url_for("get_questionnaire", questionnaire_id=questionnaire_json["id"], _external=True)
        else:
            new_questionnaire[field] = questionnaire_json[field]
    return new_questionnaire

@app.route("/ex9/api/v2.0/questionnaires", methods = ["GET"])
def get_questionnaires():
    questionnaires = get_les_questionnaires()
    return jsonify(questionnaires = [make_public_questionnaire(questionnaire) for questionnaire in questionnaires])

@app.route("/ex9/api/v2.0/questionnaires/<int:questionnaire_id>", methods = ["GET"])
def get_questionnaire(questionnaire_id):
    questionnaire_trouve = get_le_questionnaire(questionnaire_id)
    if questionnaire_trouve is not None:
        les_questions = get_les_questions_questionnaire(questionnaire_id)
        questionnaire_json = questionnaire_trouve.to_json()
        questionnaire_json["questions"] = [question.to_json() for question in les_questions]
        return jsonify(questionnaire = questionnaire_json)
    abort(404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({"error": "Bad request"}), 400)

@app.route("/ex9/api/v2.0/questionnaires", methods=["POST"])
def create_questionnaire():
    questionnaires = get_les_questionnaires()
    if not request.json or not 'name' in request.json:
        abort(404)
    add_questionnaire(request.json["name"])
    return jsonify({"questionnaire": make_public_questionnaire(get_le_questionnaire(questionnaires[-1].id + 1))}), 201

@app.route("/ex9/api/v2.0/questionnaires/<int:questionnaire_id>", methods=["PUT"])
def update_questionnaire(questionnaire_id):
    questionnaire = get_le_questionnaire(questionnaire_id)
    if questionnaire is None:
        abort(404)
    if not request.json:
        abort(400)
    if "name" in request.json and type(request.json["name"]) != str:
        abort(400)
    update_questionnaire(questionnaire_id, request.json.get('name', questionnaire.name))
    return jsonify({'questionnaire': make_public_questionnaire(questionnaire)})