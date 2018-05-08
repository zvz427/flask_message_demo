from flask import Flask,request,url_for,make_response,redirect,abort,render_template,session,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from datetime import datetime
import os
import json
# import pymysql
# pymysql.install_as_MySQLdb()

basedir = os.path.abspath(os.path.join(__file__))

app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'SKFJ347FY4H3FER0D03##@&3R4FNIFWF'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zz@localhost/messageboard'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

#表单
class NameForm(FlaskForm):
    name = StringField("what's your name?",validators=[Required()])
    submit = SubmitField('Submit')
   
class MessageForm(FlaskForm):
    name = StringField('姓名')
    address = StringField('地址')
    email = StringField('邮件')
    content = StringField('留言内容')
    submit = SubmitField('提交')


#模型,扩展常用的字段类型！！！
class Message(db.Model):
    __tablename__ = 'message_flask'
    id = db.Column(db.INTEGER,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    address = db.Column(db.String(200))
    email = db.Column(db.String(50))
    content = db.Column(db.String(400))
    
    def __repr__(self):
        return '<message %r>' % self.name

#使用flask自带的form表单进行验证
@app.route('/message',methods=['GET','POST'])
def message():
    form = MessageForm()
    if form.validate_on_submit():
        name = form.name.data
        address = form.address.data
        email = form.email.data
        content = form.content.data

        message1 = Message(name=name,address=address,email=email,content=content)
        db.session.add(message1)
        db.session.commit()
        flash('留言成功')
        return redirect(url_for('message'))
    return render_template('messageboard.html',form=form,)

@app.route('/newmessage',methods=['GET','POST'])
def newmessage():

    if request.method == 'GET':
        return render_template('newmessage.html')
    elif request.method == 'POST':
        # data = json.loads(request.get_data().decode('utf-8'))
        data = request.get_json()
        name = data['name']
        address = data['address']
        email = data['email']
        content = data['content']

        message1 = Message(name=name,address=address,email=email,content=content)
        db.session.add(message1)
        db.session.commit()
        flash('留言成功')
        return json.dumps({'errcode':200})
        # return redirect(url_for('message'))
    # return render_template('messageboard.html',form=form,)

    
# @app.route('/index',methods=['GET','POST'])
# def index():
#     name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ''
#     return render_template('index.html',form=form,name=name)

#优化解决重定向刷新丢失数据问题
@app.route('/index',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('你名字好像变了')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),400

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

@app.route('/auser/<name>')
def user(name):
    return render_template('user.html', name=name)

#时间模块显示错误？？？
@app.route('/index0')
def index0():
    return render_template('hello.html',current_time=datetime.utcnow())

def load_user(id):
    if id == 0:
        return None

@app.route('/users/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return 'hello %s' %user.name

@app.route('/user_agent')
def index_user_agent():
    user_agent = request.headers.get('User-Agent')
    return '<p>your brower is %s</p>' % user_agent

@app.route('/')
def hello_world():
    return 'hello nerd,bad request',400

@app.route('/1')
def index2():
    response = make_response('we carry a cookies')
    #报错？？？
    # response.set_cookie({'answer':'666','name':'zxy','age':23})
    # response.set_cookie('answer','666','qza','zxy')
    response.set_cookie('answer','666')
    return response

#302重定向
@app.route('/2')
def index3():
    return redirect('http://www.baidu.com')

@app.route('/user/<username>/')
def show_user_profile(username):
    return 'user is {}'.format(username)

@app.route('/post/<int:post_id>/')
def show_post(post_id):
    return 'post is %s' % post_id

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return 'post'
    else:
        return 'not post'
    

if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()