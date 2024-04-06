from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

from config import config

#Blueprints
from blueprints.NotesBlueprint import notesBlueprint
from blueprints.UsersBlueprint import usersBlueprint


app = Flask(__name__)
CORS(app)
connection = MySQL(app)

# Le pasamos la conexión de la base de datos a los blueprints
notesBlueprint.connection = connection
usersBlueprint.connection = connection

def NotFound(error):
    return jsonify({'success': False, 'message': 'Ruta no encontrada'}), 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, NotFound)

    #Registrar los blueprints
    app.register_blueprint(notesBlueprint)
    app.register_blueprint(usersBlueprint)
    app.run()
