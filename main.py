from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask import Flask, jsonify, render_template, request,redirect, url_for
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
    map_url = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(250), nullable=True)
    seats = db.Column(db.String(250), nullable=True)
    has_toilet = db.Column(db.Boolean, nullable=True)
    has_wifi = db.Column(db.Boolean, nullable=True)
    has_sockets = db.Column(db.Boolean, nullable=True)
    can_take_calls = db.Column(db.Boolean, nullable=True)
    coffee_price = db.Column(db.String(250), nullable=True)


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Cafe Location on Gooogle Maps (URL)', validators=[DataRequired()])
    img_url = StringField('Cafe Image (URL)', validators=[DataRequired()])
    location = StringField('Cafe Address', validators=[DataRequired()])
    seats = StringField('How many seats', validators=[DataRequired()])
    has_toilet = BooleanField('Has Coffee ', validators=[DataRequired()],default=False)
    has_wifi = BooleanField('Has WIFI ', validators=[DataRequired()],default=False)
    has_sockets = BooleanField('has Power Socket ', validators=[DataRequired()],default=False)
    can_take_calls = BooleanField('Can make calls', validators=[DataRequired()],default=False)
    coffee_price = StringField('Coffee Price ', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")

# @app.route('/add',methods=['GET','POST'])
# def add_cafe():
#     form = CafeForm()
#     if form.validate_on_submit():
#         # Specify the data for the new row
#         new_row_data = [form.cafe.data, form.location.data, form.open.data,form.close.data]
#     return render_template('add.html', form=form)

@app.route('/add',methods=['GET','POST'])
def add_cafe():

    form = CafeForm()
    if request.method == 'POST':
        name = form.name.data
        map_url = form.map_url.data
        img_url = form.img_url.data
        location = form.location.data
        seats = form.seats.data
        coffee_price = form.coffee_price.data
        has_wifi = form.has_wifi.data
        has_sockets = form.has_sockets.data
        has_toilet = form.has_toilet.data
        can_take_calls = form.can_take_calls.data
        new_cafe = Cafe(name=name, map_url=map_url,location=location,\
                    seats=seats,coffee_price=coffee_price,img_url=img_url,\
                    has_toilet=has_toilet,has_sockets=has_sockets,has_wifi=has_wifi,\
                    can_take_calls=can_take_calls)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))

    return render_template('add.html',form=form)


@app.route('/cafes')
def cafes():
    all_cafes = db.session.query(Cafe).all()
    return render_template('cafes.html',cafes = all_cafes)
    
if __name__=='__main__':
   app.run(debug=True)   