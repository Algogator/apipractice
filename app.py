#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

students = [
    {
        'roll_no': 2011503039,
        'name': "Anna",
        'gpa': 7.6

    }
]

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({"students": students})

@app.route('/students/<int:roll_no>', methods=['GET'])
def get_student(roll_no):
    student = filter(lambda s: s['roll_no'] == roll_no, students)
    if len(student) == 0:
        abort(404)
    return jsonify({'student': student[0]})

@app.route('/students', methods=["POST"])
def new_student():
    if not request.json or not 'roll_no' in request.json:
        abort(404)
    student = {
        'roll_no': request.json['roll_no'],
        'name': request.json.get('name', ""),
        'gpa': request.json['gpa']

    }
    students.append(student)
    return jsonify({'student': student}), 201

@app.route('/students/<int:roll_no>', methods=['PUT'])
def update_student(roll_no):
    if not request.json or not 'new_roll_no' in request.json:
        abort(404)
    student = filter(lambda s: s['roll_no'] == roll_no, students)
    if len(student) == 0:
        abort(404)
    student[0]['roll_no']=request.json['new_roll_no']
    return jsonify({'student':student[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'ERROR': 'Student not found!'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'ERROR': 'Bad format!'}))

if __name__ == '__main__':
    app.run(debug=True)
