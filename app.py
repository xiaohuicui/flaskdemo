import os
import sys
import pandas as pd
from flask import Flask,render_template,flash
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, IntegerField, SubmitField,FloatField
from flask_wtf.file import FileField, FileAllowed
import sqlite3

app = Flask(__name__)
bootstrap = Bootstrap(app)
root_path = os.path.abspath(os.path.dirname(__file__))

# Configurations
app.config['SECRET_KEY'] = 'blah blah blah blah'


class NameForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Submit')


class UploadForm(FlaskForm):
    file = FileField('Upload File', validators=[FileAllowed(['csv'])])
    submit = SubmitField('Submit')


@app.route('/showtable', methods=['GET', 'POST'])
def showtable():
    form = UploadForm()
    if form.validate_on_submit():
        if form.submit.data:
            file = form.file.data
            form.file.data.save(root_path + '/static/'+file.filename)
            flash(u'success upload file', 'success')

        # return redirect(request.url)
    # if not os.path.isfile(root_path + '/static/sp.csv'):
    #     return render_template('showtable.html', form=form, name=None)
        data = pd.read_csv(root_path + '/static/'+file.filename)
        # ��������
        con = sqlite3.connect(root_path+"/people.db")
        data.to_sql(name='test2', con=con, if_exists='replace', index=False)
        print(data.columns)
        print(data.values)
        return render_template('showtable.html', form=form, name=None, cols=data.columns, rows=data.values)
    return render_template('showtable.html', form=form, name=None)


class SearchbyNameForm(FlaskForm):
    name = StringField('Search by Name')
    submit = SubmitField('Submit')


class SearchbySalaryForm(FlaskForm):
    salary = StringField('Search by Salary')
    submit = SubmitField('Submit')


@app.route('/search', methods=['GET', 'POST'])
def search():
    form1 = SearchbyNameForm()
    form2 = SearchbySalaryForm()
    if form1.validate_on_submit():
        name = form1.name.data
        df = sqlite3.connect(root_path + "/people.db")
        cu = df.cursor()
        sql = "select * from test2 where Name = '" + name + "'"
        print(sql)
        cu.execute(sql)
        results = cu.fetchall ()
        print(results)
        return render_template('search.html', form1=form1, form2=form2, rows=results)
    if form2.validate_on_submit():
        salary = form2.salary.data
        df = sqlite3.connect(root_path + "/people.db")
        cu = df.cursor()
        sql = "select * from test2 where Salary < '" + salary + "'"
        print(sql)
        cu.execute(sql)
        results = cu.fetchall ()
        print(results)
        return render_template('search.html',form1=form1, form2=form2, rows=results)
    return render_template('search.html', form1=form1, form2=form2)


class RemovebyNameForm(FlaskForm):
    name = StringField('Remove by Name')
    submit = SubmitField('Submit')


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    form = RemovebyNameForm()
    if form.validate_on_submit():
        name = form.name.data
        df = sqlite3.connect(root_path + "/people.db")
        cu = df.cursor()
        sql = "delete from test2 where Name = '" + name + "'"
        cu.execute(sql)
        sql = "select * from test2"
        cu.execute(sql)
        print(sql)
        results = cu.fetchall()
        print(results)
        return render_template('delete.html', form=form, rows=results)
    return render_template('delete.html', form=form)


class ChangeKeywordsbyNameForm(FlaskForm):
    name = StringField('Change by Name')
    keywords = StringField('Input new keywords')
    submit1 = SubmitField('Submit')


class ChangeSalarybyNameForm(FlaskForm):
    name = StringField('Change by Name')
    keywords = StringField('Input new salary')
    submit2 = SubmitField('Submit')


@app.route('/change', methods=['GET', 'POST'])
def change():
    form1 = ChangeKeywordsbyNameForm()
    form2 = ChangeSalarybyNameForm ()
    if form1.validate_on_submit():
        name = form1.name.data
        keywords = form1.keywords.data
        df = sqlite3.connect(root_path + "/people.db")
        cu = df.cursor ()
        sql = "update test2 set Keywords = '" + keywords + "' where Name = '" + name + "'"
        cu.execute(sql)
        sql = "select * from test2 where Name = '" + name + "'"
        cu.execute(sql)
        print(sql)
        results = cu.fetchall()
        print(results)
        return render_template('change.html', form1=form1, form2=form2, rows=results)
    if form2.validate_on_submit():
        name = form2.name.data
        salary = form2.salary.data
        df = sqlite3.connect(root_path + "/people.db")
        cu = df.cursor()
        sql = "update test2 set Salary = '" + salary + "' where Name = '" + name + "'"
        print(sql)
        cu.execute(sql)
        sql = "select * from test2 where Name = '" + name + "'"
        cu.execute(sql)
        print(sql)
        results = cu.fetchall ()
        print(results)
        return render_template('change.html', form1=form1, form2=form2, rows=results)
    return render_template('change.html', form1=form1, form2=form2)


@app.route("/", methods=['GET', 'POST'])
def index():
    # return "helloworld"
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        return render_template('index.html', form=form, name=name)
    return render_template('index.html', form=form, name=None)


@app.route('/help')
def help():
    text_list = []
    # Python Version
    text_list.append({
        'label': 'Python Version',
        'value': str(sys.version)})
    # os.path.abspath(os.path.dirname(__file__))
    text_list.append({
        'label': 'os.path.abspath(os.path.dirname(__file__))',
        'value': str(os.path.abspath(os.path.dirname(__file__)))
    })
    # OS Current Working Directory
    text_list.append({
        'label': 'OS CWD',
        'value': str(os.getcwd())})
    # OS CWD Contents
    label = 'OS CWD Contents'
    value = ''
    text_list.append({
        'label': label,
        'value': value})
    return render_template('help.html', text_list=text_list, title='help')


if __name__ == '__main__':
    app.run()
