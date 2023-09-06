from flask import Blueprint, flash, render_template, request, url_for, redirect
from . import db
from .models import Users,staffs
from .forms import SignUp, Login, staffLogin
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)




# TODO: insert root url ('/') codes here

@auth.route('/')
def home():
    print(current_user)
    if current_user.is_active:
        return redirect(url_for("views.success"))
    return render_template("home.html",current_user=current_user)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    # insert code here
    # if current_user.is_active:
    #     return redirect(url_for("views.success"))

    form = SignUp(request.form)
    if form.validate_on_submit():
        name = form.name.data.strip() if form.name.data.strip() else ''
        new_user = Users(name=name, phonenumber=form.phonenumber.data,
                         password=generate_password_hash(form.password.data, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        flash('Account created!', category='success')
        return redirect(url_for('auth.login'))

    return render_template("signup.html", form=form)


@auth.route('/login', methods=['GET','POST'])
def login():
    # insert code here
    if current_user.is_active:
        return redirect(url_for("views.success"))

    form = Login(request.form)
    if form.validate_on_submit():
        user = Users.query.filter_by(phonenumber=form.phonenumber.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                flash('Logged in successfully', category='success')
                login_user(user)
                return redirect(url_for('views.success'))

            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('No account with that email address.', category='error')

    return render_template('login.html', form=form)


@auth.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))


@auth.route('/stafflogin', methods=['GET','POST'])
def staff_login():
    # insert code here
    stafflist = {'staffid': 'Azrul', 'password': '123Azrul!'}

    if current_user.is_active:
        return redirect(url_for("views.adminhome"))

    forms = staffLogin(request.form)

    if forms.validate_on_submit():
        staffid = forms.staffid.data
        password = forms.password.data
        print(staffid)
        print(password)
        new_user = staffs(staffid=stafflist['staffid'], password=stafflist['password'])
        db.session.add(new_user)
        db.session.commit()


        # Check if staffid exists in stafflist
        if staffid == stafflist['staffid']:
            # Check if the password matches (you should use Flask-Bcrypt here)
            if password == stafflist['password']:
                flash('Logged in successfully', category='success')

                # Assuming 'staff' is your User model and 'staffverify' is the user to be logged in
                staff = staffs.query.filter_by(staffid=staffid).first()
                login_user(staff)
                return redirect(url_for('views.adminhome'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('No account with that staff ID.', category='error')

    return render_template('stafflogin.html', form=forms)



