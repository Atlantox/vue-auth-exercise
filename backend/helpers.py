import re 

userLengthConfig = {
    'username': {'max': 50, 'min':4},
    'password': {'max': 40, 'min':8},
    'email': {'max': 100, 'min':4}
}

noteLengthConfig = {
    'titulo': {'max': 50, 'min': 4},
    'contenido': {'max': 1000, 'min': 4}
}

def ValidateLength(validations, data):
    lengthOK = True
    for field, value in validations.items():
        fieldLength = len(data[field])
        if fieldLength > value['max'] or fieldLength < value['min']:
            lengthOK = 'El campo {0} incumple el requisito mínimo o máximo de caracteres permitido'.format(field)
            break
    
    return lengthOK


def HasSuspiciousCharacters(indexes, content):
    '''
    Recieves a list of indexes and a dict
    Return True if at least one field has suspiciosu characters
    '''
    suspiciousFound = False
    for index in indexes:
        suspiciousRegex = r'[(){}[\]\\¡!¿?=\-<>|&\'"]'
        if re.findall(suspiciousRegex, content[index]):
            suspiciousFound = 'El campo {0} contiene caracteres sospechosos'.format(index)
            break

    return suspiciousFound

    
def HasEmptyFields(indexes, content):
    '''
    Recieves a list of indexes and a dict
    Check if at least one index is empty or not exists
    Return a dict with the requried indexes and their content

    If optional is True, the function will ignore not found indexes
    '''
    error = ''
    finalData = {}
    for index in indexes:
        if index not in content:
            error = '{0} No encontrado'.format(index)
            break

        if content[index] == '':
            error = '{0} Está vacío'.format(index)
            break

        finalData[index] = content[index]

    return finalData if error == '' else error


def EmailIsOK(email):
    suspiciousRegex = r'[(){}[\]\\¡!¿?=<>|&\'"]'
    emailRegex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    emailOK = False
    if re.findall(emailRegex, email) and not re.findall(suspiciousRegex, email):
        emailOK = True

    return emailOK


def ValidateNoteData(recievedData):
    error = ''
    requiredFields = [
        'titulo',
        'contenido'
    ]

    cleanData = HasEmptyFields(requiredFields, recievedData)
    if type(cleanData) is str:
        error = cleanData

    if error == '':
        lengthOK = ValidateLength(noteLengthConfig, cleanData)
        if lengthOK is not True:
            error = lengthOK

    if error == '':
        suspicious = HasSuspiciousCharacters(['titulo', 'contenido'], cleanData)
        if suspicious is not False:
            error = suspicious
    
    if error == '':
        result = cleanData
    else:
        result = error
    return result

def ValidateUserData(recievedData):
    error = ''
    requiredFields = [
        'username',
        'password',
        'email'
    ]

    cleanData = HasEmptyFields(requiredFields, recievedData)
    if type(cleanData) is str:
        error = cleanData

    if error == '':
        lengthOK = ValidateLength(userLengthConfig, cleanData)
        if lengthOK is not True:
            error = lengthOK

    if error == '':
        suspicious = HasSuspiciousCharacters(['username'], cleanData)
        if suspicious is not False:
            error = suspicious

    if error == '':
        emailOK = EmailIsOK(cleanData['email'])
        if emailOK == False:
            error = 'Correo inválido'
    
    return error

def JsonExists(request):
    recievedData = None
    error = ''
    statusCode = 200
    try:
        recievedData = request.json
    except Exception as err:
        error = 'JSON no encontrado'
        statusCode = 400
    
    return recievedData, error, statusCode

def GetTokenOfRequest(request):
    headers = request.headers
    bearer = headers.get('Authorization')
    if bearer is not None:
        token = bearer.split(' ')[1]
    else:
        token = None
    return token