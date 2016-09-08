#!/usr/bin/env python
#-*-coding:utf-8 -*-
#
#  SQLAlchemy database model.  This defines your database using SQLAlchemy
#  "declarative" format.  See:
#
#      http://docs.sqlalchemy.org/en/rel_0_8/orm/extensions/declarative.html
#
#  for more information
#
#  See the sections marked with "XXX" to customize for your application.
#  Or remove this file and references to "model" if you aren't using a
#  database.
#
#  See the README.md for more information
#
#  Written by Sean Reifschneider <jafo@jafo.ca>, 2013
#
#  Part of the python-bottle-skeleton project at:
#
#      https://github.com/linsomniac/python-bottle-skeleton
#
#  I hereby place this work, python-bottle-wrapper, into the public domain.

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import event, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.orm import relationship, backref
from sqlalchemy.pool import Pool
from sqlalchemy.sql import func


def initdb():
    '''Populate an empty database with the schema'''
    from bottledbwrap import dbwrap

    dbwrap.connect()
    dbwrap.Base.metadata.create_all()


@event.listens_for(Pool, 'checkout')
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    '''Ping a database connection before using it to make sure it is still
    alive.'''
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute('SELECT 1')
    except:
        # optional - dispose the whole pool instead of invalidating separately
        # connection_proxy._pool.dispose()

        # pool will try connecting again up to three times before raising.
        raise DisconnectionError()
    cursor.close()


#  XXX Your model goes here
class ChoiceQuestion(Base):
    __tablename__ = 'choice_question'
    id = Column(Integer(), primary_key=True)
    descr = Column(String(length=512), nullable=False)
    note = Column(String(length=512), nullable=True)

    #multi choices?
    multi = Column(Integer(), nullable=False)
    choice_list = Column(String(length=512), nullable=False)
    #timestamp = Column(DateTime(), default=func.now)

class TrueFalseQuestion(Base):
    __tablename__ = 'truefalse_question'
    id = Column(Integer(), primary_key=True)
    descr = Column(String(length=512), nullable=False)
    note = Column(String(length=512), nullable=True)

class EssayQuestion(Base):
    __tablename__ = 'essay_question'
    id = Column(Integer(), primary_key=True)
    descr = Column(String(length=512), nullable=False)
    note = Column(String(length=512), nullable=True)

class SnapshotQuestion(Base):
    __tablename__ = 'snapshot_question'
    id = Column(Integer(), primary_key=True)
    descr = Column(String(length=512), nullable=False)
    note = Column(String(length=512), nullable=True)
    
    type = Column(Integer(), nullable=False)
    #snapshot file
    #content = Column(String(length=512), nullable=False)
    

def question_by_id(qid):
    from bottledbwrap import dbwrap
    db = dbwrap.session()
    q = db.query(ChoiceQuestion).filter_by(id=qid).first()
    return q


#################################################
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)

    name = Column(String(length=20), nullable=False)
    full_name = Column(String(length=60), nullable=False)
    email_address = Column(String(length=60), nullable=False)


#  XXX A database-related function
def user_by_name(name):
    from bottledbwrap import dbwrap
    db = dbwrap.session()
    user = db.query(User).filter_by(name=name).first()
    return user


#  XXX Some sample data for testing the site
def create_sample_data():
    from bottledbwrap import dbwrap

    dbwrap.connect()
    dbwrap.Base.metadata.create_all()
    db = dbwrap.session()

    sean = User(
            full_name='Sean Reifschneider', name='sean',
            email_address='jafo@example.com')
    db.add(sean)
    evi = User(
            full_name='Evi Nemeth', name='evi',
            email_address='evi@example.com')
    db.add(evi)
    dmr = User(
            full_name='Dennis Ritchie', name='dmr',
            email_address='dmr@example.com')
    db.add(dmr)

    dmr = User(
            full_name='Peichao Wang', name='pwang',
            email_address='pwang@example.com')
    db.add(dmr)

    db.commit()


    q = TrueFalseQuestion(descr=u'幻想与一般的创造想象区别在于，幻想中所创造的形象总是体现着个人的愿望，并指向未来。',
        note=u'对')

    db.add(q)

    q = ChoiceQuestion(multi=1, descr=u'教育目的就其表述和内容而言具有（ ）特征。',
        choice_list=u'抽象性@理想性@可操作性@终极性', note=u'ABD')
    db.add(q)

    q = ChoiceQuestion(multi=1, descr=u'下列关于复式教学叙述正确的是( )。',
        choice_list=u'复式教学就是对两个以上年级的学生进行教学的一种教学组织形式@复式教学适用于学生多、教室少的情况下教学@复式教学课堂教师的教学和学生的自学或做作业同时进行@复式教学情景下的学生的基本技能和自学能力相对较弱',
        note=u'ABC')
    db.add(q)

    db.commit()
