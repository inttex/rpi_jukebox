from flask_restful import Resource

class Homepage(Resource):
    def get(self):
        return 'homepage'
