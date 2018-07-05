"""
脚本管理,初始化一系列任务
"""
from flask_script import Manager
from nowstagram import app, db
from nowstagram.models import User, Image, Comment
import random
import unittest


manager = Manager(app)


@manager.command
def run_test():
    """
    .discover会寻找指定目录下所有'test*.py'的文件
    """
    tests = unittest.TestLoader().discover('./')
    unittest.TextTestRunner.run(self=None, test=tests)

    pass


@manager.command
def init_database():
    """
    初始化数据库
    """
    db.drop_all()
    db.create_all()
    for i in range(100):
        db.session.add(User('User' + str(i), 'a' + str(i), 'http://jira.internal.hyperchain.cn/secure/useravatar?avatarId=' + str(random.randint(10344, 10352))))
        db.session.add(Image('http://08.imgmini.eastday.com/mobile/20171211/20171211181930_917f4f40b9fbaf2e06769b8fc77eefb2_1.jpeg', i + 1))
        for j in range(5):
            db.session.add(Image('http://jira.internal.hyperchain.cn/secure/useravatar?avatarId=10352' + str(random.randint(10344, 10352)), i + 1))
            for k in range(3):
                db.session.add(Comment('This is a comment {0}'.format(k + 1), i + 1, i + 1))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
