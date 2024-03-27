from .app import app, db

@app.cli.command()
def loaddb():
    '''Creates the tables and populates them with data. '''
    # création de toutes les tables
    db.create_all()
    # chargement de notre jeu de données
    from .models import Questionnaire, QuestionSimple, QuestionMultiple
    questionnaire_1 = Questionnaire("Questionnaire simple")
    questionnaire_2 = Questionnaire("Questionnaire dur")
    question_capitale_france = QuestionSimple("Quelle est la capitale de la France ?", "Paris", "questionsimple", "Paris", "Marseille", 1)
    question_capitale_espagne = QuestionMultiple("Quelle est la capitale de l'Espagne ?", "Madrid", "questionmultiple", "Almeria", "Barcelone", "Madrid", "Listenbourg", 1)
    question_tracteur = QuestionSimple("Est-ce qu'il faut tout détruire avec les tracteurs ?", "Oui", "questionsimple", "Oui", "Non", 2)
    question_attal = QuestionMultiple("Est-ce que Attal affirme son homosexualité ?", "Oui", "questionmultiple", "Non", "Oui", "Aujourd'hui uniquement", "Suivant son humeur", 2)
    db.session.add(questionnaire_1)
    db.session.add(questionnaire_2)
    db.session.add(question_capitale_france)
    db.session.add(question_capitale_espagne)
    db.session.add(question_tracteur)
    db.session.add(question_attal)
    db.session.commit()

@app.cli.command()
def syncdb():
    '''Creates all missing tables.'''
    db.create_all()

@app.cli.command()
def dropdb():
    '''Drops all tables.'''
    db.drop_all()