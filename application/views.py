from flask import Blueprint, flash, render_template, request, url_for, redirect
from . import db
from .models import Expenses,Users
from .forms import EditExpense
from flask_login import current_user, login_required
from datetime import date
from .forms import SignUp

views = Blueprint('views', __name__)





@views.route('/success')
@login_required
def success():
    name = Users.query.filter_by(get_id=current_user.phonenumber).first()
    return render_template('success.html',user=current_user.phonenumber,name=current_user.name)


@views.route('/profile/<int:phonenumber>')
@login_required
def profile(phonenumber):
    user = Users.query.filter_by(phonenumber=current_user.phonenumber).first()
    return render_template('profile.html',user=current_user.phonenumber,name=current_user.name)

@views.route('/update/<int:phonenumber>',methods=['GET', 'POST'])
@login_required
def update(phonenumber):
    user = Users.query.filter(phonenumber == current_user.phonenumber).first()
    form = SignUp(request.form)
    print(user.phonenumber)
    if form.validate_on_submit():
        user.name = form.name.data
        user.phonenumber = form.phonenumber.data
        user.password = user.password
        user.date_joined = user.date_joined
        db.session.commit()
        return redirect(url_for("views.success"))

    else:
        if request.method == 'GET':
            form = SignUp(
                data={
                    "phonenumber": user.phonenumber,
                    "name": user.name,
                    "password": user.password,
                    "date_joined": user.date_joined
                }
            )
        return render_template('update.html',form=form)

@views.route('/adminhome')
@login_required
def admin():
    # insert code here
    return render_template("adminhome.html")