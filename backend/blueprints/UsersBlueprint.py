from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from models.UserModel import UserModel
from helpers import *

USERNAME_MAX, USERNAME_MIN = 50, 4
PASSWORD_MAX, PASSWORD_MIN = 40, 8
EMAIL_MAX, EMAIL_MIN = 100, 4

usersBlueprint = Blueprint('users', __name__)

def initModels():
    connection = getattr(usersBlueprint, 'connection', None)
    if connection is None:
        raise Exception('No se pudo obtener la conexión desde el Blueprint Notes')
    
    return UserModel(connection)


@usersBlueprint.route('/users', methods=['GET'])
def GetUserData():
    userModel = initModels()
    response = {}
    statusCode = 200
    error = ''
    token = GetTokenOfRequest(request)
    if token == None:
        error = 'Acceso denegado. Autenticación requerida'
        statusCode = 401
    
    if error == '':
        targetUser = userModel.GetUserByToken(token)
        if targetUser == None:
            error = 'Usuario no encontrado'
            statusCode = 401
    
    if error == '':
        publicData = userModel.GetUserPublicData(token)
        response = {'success': True, 'data': publicData}
    else:
        response = {'success': False, 'message': error}

    return jsonify(response), statusCode


@usersBlueprint.route('/users', methods=['POST'])
def RegisterUser():
    userModel = initModels()
    statusCode = 201
    error = ''
    try:
        recievedData = request.json
    except Exception as err:
        error = 'JSON no encontrado'
        statusCode = 400

    if error == '':
        token = GetTokenOfRequest(request)
        if token is not None:
            error = 'Usted ya está autenticado'
            statusCode = 401  # Unauthorized

    if error == '':
        requiredFields = [
            'username',
            'password',
            'email'
        ]
        dataOK = HasEmptyFields(requiredFields, recievedData)
        if dataOK is not False:
            error = dataOK
            statusCode = 400  # Bad request

    if error == '':
        lengthValidator = {
            'username': {'max': USERNAME_MAX, 'min':USERNAME_MIN},
            'password': {'max': PASSWORD_MAX, 'min':PASSWORD_MIN},
            'email': {'max': EMAIL_MAX, 'min':EMAIL_MIN}
        }

        lengthOK = ValidateLength(lengthValidator, recievedData)
        if lengthOK is not True:
            error = lengthOK
            statusCode = 400

    if error == '':
        suspicious = HasSuspiciousCharacters(['username'], recievedData)
        if suspicious is not False:
            error = 'El usuario contiene caracteres sospechosos'
            statusCode = 400

    if error == '':
        emailOK = EmailIsOK(recievedData['email'])
        if emailOK == False:
            error = 'Correo inválido'
            statusCode = 400
        
    if error == '':
        if userModel.EmailExists(recievedData['email']) is True:
            error = 'Correo ya registrado'
            statusCode = 400

    if error == '':
        if userModel.UsernameExists(recievedData['username']) is True:
            error = 'Usuario ya registrado'
            statusCode = 400
    
    if error == '':
        created = userModel.CreateUser(recievedData)
        if created:
            message = 'Usuario creado correctamente'
        else:
            error = 'Hubo un error al crear al usuario'
            statusCode = 500

    if error != '':
        message = error

    success = error == ''
    return jsonify({'success': success, 'message': message}), statusCode

@usersBlueprint.route('/login', methods=['POST'])
def TryLogin():
    userModel = initModels()
    statusCode = 200
    error = ''
    try:
        recievedData = request.json
    except Exception as err:
        error = 'JSON no encontrado'
        statusCode = 400

    if error == '':
        token = GetTokenOfRequest(request)
        if token is not None:
            error = 'Usted ya está autenticado'
            statusCode = 401  # Unauthorized

    if error == '':
        requiredFields = [
            'username',
            'password'
        ]
        dataOK = HasEmptyFields(requiredFields, recievedData)
        if type(dataOK) is str:
            error = dataOK
            statusCode = 400  # Bad request

    if error == '':
        lengthValidator = {
            'username': {'max': USERNAME_MAX, 'min':USERNAME_MIN},
            'password': {'max': PASSWORD_MAX, 'min':PASSWORD_MIN}
        }

        lengthOK = ValidateLength(lengthValidator, recievedData)
        if lengthOK is not True:
            error = lengthOK
            statusCode = 400
            
    if error == '':
        suspicious = HasSuspiciousCharacters(['username'], recievedData)
        if suspicious is not False:
            error = 'El usuario contiene caracteres sospechosos'
            statusCode = 400
    
    if error == '':
        loginResult = userModel.TryLogin(recievedData['username'], recievedData['password'])
        if loginResult is False:
            error = 'Credenciales inválidas'
        else:
            userData = userModel.GetUserPublicData(loginResult)
            message = loginResult
            
    if error != '':
        message = error
    
    success = error == ''
    response = {'success': success}

    if error == '':
        response['token'] = message
        response['userData'] = userData
    else:
        response['message'] = message
    
    return jsonify(response), statusCode
