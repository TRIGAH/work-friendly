from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from wtforms import StringField, SubmitField,BooleanField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# db.create_all()

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Gooogle Maps (URL)', validators=[DataRequired()])
    coffee = BooleanField('Has Coffee ', validators=[DataRequired()],default=False)
    wifi = BooleanField('Has WIFI ', validators=[DataRequired()],default=False)
    power = BooleanField('has Power Socket ', validators=[DataRequired()],default=False)
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
        name=form.cafe.data,
        map_url=form.location.data)
        db.session.add(new_cafe)
        db.session.commit()

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    all_cafes = db.session.query(Cafe).all()
    # for cafe in all_cafes:
    #     cafes_list.append({"id":cafe.id,
    #     "name":cafe.name,
    #     "map_url":cafe.map_url,
    #     "img_url":cafe.img_url,
    #     "location":cafe.location,
    #     "seats":cafe.seats,
    #     "has_toilet":cafe.has_toilet,
    #     "has_wifi":cafe.has_wifi,
    #     "has_sockets":cafe.has_sockets,
    #     "can_take_calls":cafe.can_take_calls,
    #     "coffee_price":cafe.coffee_price,
    # })
    return render_template('cafes.html',cafes = all_cafes)
    
if __name__=='__main__':
   app.run(debug=True)   