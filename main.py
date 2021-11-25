import os
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)

# sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL1", "sqlite:///restaurants.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    food_status = db.Column(db.String(10), nullable=False)

    map_url = db.Column(db.String(500))
    img_url = db.Column(db.String(500))
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    working_hours = db.Column(db.String(50))
    created_time = db.Column(db.String(50))


# db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search')
def search_data():
    search = request.args.get('search-result')
    if search:
        all_data = Restaurant.query.filter(Restaurant.name.contains(search)
                                           | Restaurant.city.contains(search)
                                           | Restaurant.address.contains(search)
                                           | Restaurant.food_status.contains(search))
    else:
        all_data = Restaurant.query.all()
    return render_template('all-restaurants.html', restaurants=all_data)


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        date_time = datetime.now().strftime('%c')
        new_restaurant = Restaurant(
            name=request.form['restaurant_name'],
            food_status=request.form['status'],
            map_url=request.form['map_url'],
            img_url=request.form['img_url'],
            city=request.form['city_name'].title(),
            address=request.form['address'],
            working_hours=request.form['working-hours'],
            created_time=date_time
        )
        db.session.add(new_restaurant)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/show-all-restaurants')
def show_all():
    all_data = Restaurant.query.all()
    return render_template('all-restaurants.html', restaurants=all_data)


@app.route('/edit-restaurants', methods=['POST', 'GET'])
def edit():
    restaurants = Restaurant.query.all()
    if request.method == 'POST':
        restaurant_id = request.args.get('res_id')
        res_to_edit = Restaurant.query.filter_by(id=restaurant_id).first()
        res_to_edit.name = request.form['restaurant_name']
        res_to_edit.food_status = request.form['restaurant_food_status'].title()
        res_to_edit.map_url = request.form['restaurant_map_url']
        res_to_edit.img_url = request.form['restaurant_img_url']
        res_to_edit.city = request.form['restaurant_city']
        res_to_edit.address = request.form['restaurant_address']
        res_to_edit.working_hours = request.form['restaurant_working_time']
        db.session.commit()
        return redirect(url_for('edit'))
    return render_template('edit.html', restaurants=restaurants)


@app.route('/delete_restaurant')
def delete():
    res_id = request.args.get('res_id')
    restaurant_to_delete = Restaurant.query.filter_by(id=res_id).first()
    db.session.delete(restaurant_to_delete)
    db.session.commit()
    return redirect(url_for('edit'))


if __name__ == "__main__":
    app.run(debug=True)
