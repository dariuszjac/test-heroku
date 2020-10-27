from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/sample_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'lakes'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '%s/%s' % (self.id, self.name)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/data', methods=['POST', 'GET'])
def data():

    # POST a data to database
    if request.method == 'POST':
        body = request.json
        name = body['name']

        data = User(name)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
            'name': name
        })

    # GET all data from database & sort by id
    if request.method == 'GET':
        # data = User.query.all()
        data = User.query.order_by(User.id).all()
        print(data)
        dataJson = []
        for i in range(len(data)):
            # print(str(data[i]).split('/'))
            dataDict = {
                'id': str(data[i]).split('/')[0],
                'name': str(data[i]).split('/')[1],
            }
            dataJson.append(dataDict)
        return jsonify(dataJson)


if __name__ == '__main__':
    app.debug = True
    app.run()