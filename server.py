from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motion_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MotionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    motion_detected = db.Column(db.Boolean, nullable=False)

db.create_all()

@app.route('/upload', methods=['POST'])
def upload():
    motion_detected = request.form.get('motion_detected') == '1'
    new_data = MotionData(motion_detected=motion_detected)
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'Data received'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
