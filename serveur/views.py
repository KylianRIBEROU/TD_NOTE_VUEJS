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

# -- questions --
@app.route("/flaskapi/v1.0/questions", methods=["GET"])
def get_questions():
    questions = db.session.query(Question).all()
    return jsonify(questions=[q.to_json() for q in questions])

@app.route("/flaskapi/v1.0/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    question = db.session.query(Question).get(question_id)
    if question is None:
        abort(404)
    return jsonify(question.to_json())

@app.route("/flaskapi/v1.0/questions", methods=["POST"])
def create_question():
    if not request.json or not "title" in request.json or not "type" in request.json:
        abort(400)
    if not "questionnaire_id" in request.json:
        abort(400)

    if not Questionnaire.questionnaire_existe(Questionnaire, request.json["questionnaire_id"]):
        abort(409, "Aucun questionnaire n'existe avec cet id")

    if request.json["type"] == "question_simple":
        question = QuestionSimple(request.json["title"], request.json["answer"], request.json["type"], request.json["questionnaire_id"], request.json["first_answer"], request.json["second_answer"])
        db.session.add(question)
        db.session.commit()
    elif request.json["type"] == "question_multiple":
        question = QuestionMultiple(request.json["title"], request.json["answer"], request.json["type"], request.json["questionnaire_id"],
                                     request.json["first_answer"], request.json["second_answer"], request.json["third_answer"], request.json["fourth_answer"])
        db.session.add(question)
        db.session.commit()
    else:
        abort(409)
    return jsonify(question.to_json()), 201

@app.route("/flaskapi/v1.0/questionnaire/<int:questionnaire_id>/questions", methods=["POST"])
def create_question_questionnaire(questionnaire_id):
    if not request.json or not "title" in request.json or not "question_type" in request.json:
        abort(400)
    if not "questionnaire_id" in request.json:
        abort(400)

    if request.json["question_type"] == "questionsimple":
        question = QuestionSimple(request.json["title"], request.json["answer"], request.json["question_type"], request.json["first_answer"], request.json["second_answer"], questionnaire_id)
        db.session.add(question)
        db.session.commit()
    elif request.json["question_type"] == "questionmultiple":
        question = QuestionMultiple(request.json["title"], request.json["answer"], request.json["question_type"],
                                     request.json["first_answer"], request.json["second_answer"], request.json["third_answer"], request.json["fourth_answer"], questionnaire_id)
        db.session.add(question)
        db.session.commit()
    else:
        abort(409)
    return jsonify(question.to_json()), 201

# @app.route("/flaskapi/v1.0/questions/<int:question_id>", methods=["PUT"])
# def update_question(question_id):
#     question = db.session.query(Question).get(question_id)
#     if question is None:
#         abort(404)
#     if not request.json:
#         abort(400)
#     if "title" in request.json and type(request.json["title"]) != str:
#         abort(400)
#     if "answer" in request.json and type(request.json["answer"]) is not str:
#         abort(400)
#     if "questionnaire_id" in request.json and type(request.json["questionnaire_id"]) is not int:
#         abort(400)
#     question.title = request.json.get("title", question.title)
#     question.answer = request.json.get("answer", question.answer)
#     question.questionnaire_id = request.json.get("questionnaire_id", question.questionnaire_id)
#     db.session.commit()
#     return jsonify(question.to_json())

@app.route("/flaskapi/v1.0/questions/<int:question_id>", methods=["PATCH"])
def update_question(question_id):
    question = db.session.query(Question).get(question_id)
    if question is None:
        abort(404)
    if not request.json:
        abort(400)
    if "title" in request.json and type(request.json["title"]) != str:
        abort(400)
    if "answer" in request.json and type(request.json["answer"]) is not str:
        abort(400)
    if "first_answer" in request.json and type(request.json["first_answer"]) is not str:
        abort(400)
    if "second_answer" in request.json and type(request.json["first_answer"]) is not str:
        abort(400)
    if question.question_type == "questionmultiple":
        if "third_answer" in request.json and type(request.json["third_answer"]) is not str:
            abort(400)
        if "fourth_answer" in request.json and type(request.json["fourth_answer"]) is not str:
            abort(400)
        question.third_answer = request.json.get("third_answer", question.third_answer)
        question.fourth_answer = request.json.get("fourth_answer", question.fourth_answer)
    question.title = request.json.get("title", question.title)
    question.answer = request.json.get("answer", question.answer)
    question.first_answer = request.json.get("first_answer", question.first_answer)
    question.second_answer = request.json.get("second_answer", question.second_answer)
    db.session.commit()
    return jsonify(question.to_json())

@app.route("/flaskapi/v1.0/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    question = db.session.query(Question).get(question_id)
    if question is None:
        abort(404)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"result": True})

# delete questions by questionnaire_id
@app.route("/flaskapi/v1.0/questions/questionnaire/<int:questionnaire_id>", methods=["DELETE"])
def delete_questions(questionnaire_id):
    questions = db.session.query(Question).filter(Question.questionnaire_id == questionnaire_id).all()
    if questions is None:
        abort(404)
    for question in questions:
        db.session.delete(question)
    db.session.commit()
    return jsonify({"result": True})


# -------------------------- Questionnaires --------------------------

@app.route("/flaskapi/v1.0/questionnaires", methods=["GET"])
def get_questionnaires():
    questionnaires = db.session.query(Questionnaire).all()
    return jsonify(questionnaires=[q.to_json() for q in questionnaires])

@app.route("/flaskapi/v1.0/questionnaires/<int:questionnaire_id>", methods=["GET"])
def get_questionnaire(questionnaire_id):
    questionnaire = db.session.query(Questionnaire).get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    return jsonify(questionnaire.to_json())

@app.route("/flaskapi/v1.0/questionnaires", methods=["POST"])
def create_questionnaire():
    if not request.json or not "name" in request.json:
        abort(400)
    questionnaire = Questionnaire(request.json["name"])
    db.session.add(questionnaire)
    db.session.commit()
    return jsonify(questionnaire.to_json()), 201


@app.route("/flaskapi/v1.0/questionnaires/<int:questionnaire_id>", methods=["PUT"])
def update_questionnaire(questionnaire_id):
    questionnaire = db.session.query(Questionnaire).get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    if not request.json:
        abort(400)
    if "name" in request.json and type(request.json["name"]) != str:
        abort(400)
    questionnaire.name = request.json.get("name", questionnaire.name)
    db.session.commit()
    return jsonify(questionnaire.to_json())

@app.route("/flaskapi/v1.0/questionnaires/<int:questionnaire_id>", methods=["DELETE"])
def delete_questionnaire(questionnaire_id):
    questionnaire = db.session.query(Questionnaire).get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    
    delete_questions(questionnaire_id)
    db.session.delete(questionnaire)
    db.session.commit()
    return jsonify({"result": True})


@app.route("/flaskapi/v1.0/questionnaires/<int:questionnaire_id>/questions", methods=["GET"])
def get_questions_by_questionnaire(questionnaire_id):
    questions = db.session.query(Question).filter(Question.questionnaire_id == questionnaire_id).all()
    return jsonify(questions=[q.to_json() for q in questions])



# # répondre à une question
# @app.route("/flaskapi/v1.0/questions/<int:question_id>/reponse", methods=["POST"])
# def repondre_question(question_id):
#     question = db.session.query(Question).get(question_id)
#     if question is None:
#         abort(404)
#     if not request.json or not "reponse" in request.json:
#         abort(400)
#     if question.reponse == request.json["reponse"]:
#         return jsonify({"result": True,
#                         "reponse": question.reponse})
#     else:
#         return jsonify({"result": False,
#                         "reponse": question.reponse})


@app.route("/flaskapi/v1.0/questionnairequestions", methods=["POST"])
def creer_questionnaire_et_questions():
    if not request.json or not "name" in request.json or not "questions" in request.json:
        abort(400)

    print("a")
    # Créer un nouveau questionnaire
    questionnaire = Questionnaire(request.json["name"])
    db.session.add(questionnaire)
    db.session.commit()

    # Récupérer le questionnaire fraîchement ajouté pour obtenir son ID
    questionnaire = db.session.query(Questionnaire).filter(Questionnaire.name == request.json["name"]).first()

    # Parcourir toutes les questions envoyées par le client
    for q in request.json["questions"]:
        # Vérifier si les données de chaque question sont complètes
        if not "title" in q or not "type" in q:
            abort(400)

        # Ajouter la question au questionnaire en fonction de son type
        if q["type"] == "question_simple":
            question = QuestionSimple(q["title"], q["answer"], q["type"], questionnaire.id, q["first_answer"], q["second_answer"])
        elif q["type"] == "question_multiple":
            question = QuestionMultiple(q["title"], q["answer"], q["type"], questionnaire.id,
                                        q["first_answer"], q["second_answer"], q["third_answer"], q["fourth_answer"])
        else:
            abort(400)  # Type de question non pris en charge

        # Ajouter la question à la base de données
        db.session.add(question)
        db.session.commit()

    # Retourner les données JSON du questionnaire créé avec un code de statut 201 (Created)
    return jsonify(questionnaire.to_json()), 201
