"""
网页页面的跳转逻辑,视图
"""
from nowstagram import app, db
from nowstagram.models import Image, User
from flask import render_template, redirect, request, flash, get_flashed_messages, url_for, send_from_directory
import random
import hashlib
import json
from flask_login import login_user, logout_user, current_user, login_required
import os
from werkzeug import secure_filename
import uuid


def redirect_massage(target, msg, category):
    if msg is not None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/')
def index():
    image = Image.query.order_by('id_ desc').limit(5).all()

    return render_template('index.html', images=image)


@app.route('/image/<int:image_id>')
def image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return redirect('/')
    return render_template('pageDetail.html', image=image)


@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=1, per_page=3, error_out=False)
    return render_template('profile.html', user=user, images=paginate.items, has_next=paginate.has_next)


@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    map_ = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        imgvo = {'id': image.id_, 'url': image.url, 'comment_count': len(image.comments)}
        images.append(imgvo)

    map_['images'] = images
    return json.dumps(map_)


@app.route('/reloginpage')
def reloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['relogin']):
        msg = msg + m
    return render_template('login.html', msg=msg, next=request.args.get('next'))


# 用户注册流程
@app.route('/reg', methods={'post', 'get'})
def reg():
    username = request.form['username'].strip()
    password = request.form['password'].strip()

    if username == "" or password == "":
        return redirect_massage('/reloginpage', '用户名/密码不能为空', category='relogin')

    user = User.query.filter_by(username=username).first()
    if user is not None:
        return redirect_massage('/reloginpage', '用户名已存在', category='relogin')

    salt = '.'.join(random.sample('0123456789abcdefgABCDEFG', k=3))
    m = hashlib.md5()
    m.update((password + salt).encode('utf8'))
    password = m.hexdigest()

    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()

    # 用户登陆记录
    login_user(user)

    return redirect('/')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


@app.route('/login', methods={'post', 'get'})
def login():
    username = request.form['username'].strip()
    password = request.form['password'].strip()

    if username == "" or password == "":
        return redirect_massage('/reloginpage', '用户名/密码不能为空', category='relogin')

    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect_massage('/reloginpage', '用户名不存在', category='relogin')

    m = hashlib.md5()
    m.update((password + user.salt).encode('utf8'))
    if (m.hexdigest() != user.password):
        return redirect_massage('/reloginpage', '密码错误', category='relogin')

    login_user(user)

    next_page = request.form['next']
    print(next_page)
    if next_page is not None:
        return redirect(next_page)

    return redirect('/')


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXT']


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     file = request.files['file']
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
#         return redirect('/profile/%d' % current_user.id_)
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form action="" method=post enctype=multipart/form-data>
#       <p><input type=file name=file>
#          <input type=submit value=Upload>
#     </form>
#     '''


def save_to_local(file, filename):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir, filename))
    return '/image/' + filename


@app.route('/image/<image_name>')
def view_image(image_name):
    return send_from_directory(app.config['UPLOAD_DIR'], image_name)


@app.route('/upload', methods={'post'})
def upload():
    file = request.files['file']
    file_ext = ""
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
    if file_ext in app.config['ALLOWED_EXT']:
        file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
        url = save_to_local(file, file_name)
        if url is not None:
            db.session.add(Image(url, current_user.id_))
            db.session.commit()

    return redirect('/profile/%d' % current_user.id_)
