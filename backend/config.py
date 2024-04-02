class DevelopmentCondfig:
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'vue-authentication'
    MYSQL_CURSORCLASS = 'DictCursor' 

config = {
    'development': DevelopmentCondfig
}