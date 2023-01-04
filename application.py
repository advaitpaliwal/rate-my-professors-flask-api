from rmpclient import RateMyProfessorsClient
from flask import Flask, request, jsonify, make_response

application = Flask(__name__)

@application.route('/search_school', methods=['GET'])
def search_school():
    try:
        query = request.args.get('query')
        client = RateMyProfessorsClient()
        results = client.search_school(query)
        resp = make_response(jsonify(results))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except Exception as e:
        return jsonify({"error": str(e)})


@application.route('/search_teacher', methods=['GET'])
def search_teacher():
    try:
        name = request.args.get('name')
        school_id = request.args.get('school_id')
        client = RateMyProfessorsClient()
        results = client.search_teacher(name, school_id)
        resp = make_response(jsonify(results))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except Exception as e:
        return jsonify({"error": str(e)})

@application.route('/get_teacher', methods=['GET'])
def get_teacher():
    try:
        teacher_id = request.args.get('teacher_id')
        client = RateMyProfessorsClient()
        results = client.get_teacher(teacher_id)
        resp = make_response(jsonify(results))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    application.run(debug=True)
