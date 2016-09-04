#!/usr/bin/env python
#
#  This implements the website logic, this is where you would do any dynamic
#  programming for the site pages and render them from templaes.
#
#  NOTE: This file will need heavy customizations.  Search for "XXX".
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

#  XXX Remove these two lines if you aren't using a database
from bottledbwrap import dbwrap
import model
import bottle
#  XXX Remove these lines and the next section if you aren't processing forms
from wtforms import (Form, TextField, SelectField, PasswordField, DateField, BooleanField, DateTimeField, FileField, validators)

#  XXX Form validation example
class NewUserFormProcessor(Form):
    
    name = TextField('Username', [validators.Length(min=4, max=25)])
    sex = SelectField('Sex', choices=[('m','Male'), ('f', 'Female')])
    full_name = TextField('Full Name', [validators.Length(min=4, max=60)])
    email_address = TextField('Email Address', [validators.Email()])
    #email_address = TextField('Email Address', [validators.Length(min=4, max=60)])
    password = PasswordField(
            'New Password',
            [validators.Required(),
                validators.EqualTo('confirm',
                    message='Passwords must match')
            ])
    confirm = PasswordField('Repeat Password~')

    birthday = DateField(u'Your birthday')
    now = DateTimeField(u'Current time', description='...for no particular reason')
    sample_file = FileField(u'Your favorite file')
    eula = BooleanField(u'I did not read the terms and conditions',
                       validators=[validators.Required('You must agree to not agree!')])

def build_application():
    from bottle import (view, TEMPLATE_PATH, Bottle, static_file, request,
        redirect, BaseTemplate, template)

    #  XXX Define application routes in this class

    app = Bottle()

    #  Pretty much this entire function needs to be written for your

    BaseTemplate.defaults['app'] = app  # XXX Template global variable
    TEMPLATE_PATH.insert(0, 'views')    # XXX Location of HTML templates

    #  XXX Routes to static content
    #@app.route('/<path:re:favicon.ico>')
    @app.route('/static/<path:path>')
    def static(path):
        'Serve static content.'
        return static_file(path, root='static/')

    # bootstrap test
    ##################################################
    @app.route('/bootstrap', name='bootstrap')
    @view('bootstrap-starter')
    def bootstrap():
        return locals()

    @app.route('/bootstrap/hello', name='bootstrap_hello')
    @view('bootstrap-hello')
    def bootstrap_hello():
        return locals()

    @app.route('/bootstrap/theme', name='bootstrap_theme')
    @view('bootstrap-theme')
    def bootstrap_theme():
        return locals()

    @app.route('/bootstrap/starter', name='bootstrap_starter')
    #@view('bootstrap-starter')
    def bootstrap_starter():
        return template('bootstrap-starter')
    ####################################################
    
    #  XXX Index page
    @app.route('/', name='index')                  # XXX URL to page
    @view('index')                                 # XXX Name of template
    def index():
        'A simple form that shows the date'

        import datetime
        now = datetime.datetime.now()

        #  any local variables can be used in the template
        return locals()

    @app.route('/question/all', name='question_list')
    @view('question-list')
    def question_list():
        'A simple page from a dabase.'

        db = dbwrap.session()

        questions = db.query(model.ChoiceQuestion).order_by(model.ChoiceQuestion.id)

        #  any local variables can be used in the template
        return locals()
    
    @app.route('/question/<qid>', name='question')  # XXX URL to page
    @view('question')                                 # XXX Name of template
    def question_info(qid):
        'A simple page from a dabase.'

        q = model.question_by_id(qid)

        #  any local variables can be used in the template
        return locals()

    @app.get('/question/new-choice', name='new_choice')
    @app.post('/question/new-choice')
    @view('new-choice')
    def new_choice():
        'input choice question'

        if request.method == 'POST':
            db = dbwrap.session()

            choice_list = request.POST.itema.strip() \
                + '@' + request.POST.itemb.strip() \
                + '@' + request.POST.itemc.strip() \
                + '@' + request.POST.itemd.strip()
            q = model.ChoiceQuestion(
                    type=request.POST.type.strip(), choice_list=choice_list,
                    note=request.POST.note.strip())
            db.add(q)
            db.commit()

            redirect(app.get_url('question', qid=q.id))

        #  any local variables can be used in the template
        return locals()

    @app.get('/question/new-essay', name='new_essay')
    @app.post('/question/new-essay')
    @view('new-essay')
    def new_essay():
        'input essay question'

        if request.method == 'POST':
            db = dbwrap.session()

            descr = request.POST.descr.strip()
            q = model.EssayQuestion(
                    descr=descr,
                    note=request.POST.note.strip())
            db.add(q)
            db.commit()

        #  any local variables can be used in the template
        return locals()

    @app.get('/question/new-truefalse', name='new_truefalse')
    @app.post('/question/new-truefalse')
    @view('new-truefalse')
    def new_truefalse():
        'input true-false question'

        if request.method == 'POST':
            db = dbwrap.session()

        #  any local variables can be used in the template
        return locals()

    @app.get('/question/new-snapshot', name='new_snapshot')
    @app.post('/question/new-snapshot')
    @view('new-snapshot')
    def new_snapshot():
        'input snapshot question'

        if request.method == 'POST':
            db = dbwrap.session()

        #  any local variables can be used in the template
        return locals()

    #  XXX User list page
    @app.route('/users', name='user_list')        # XXX URL to page
    @view('users')                                # XXX Name of template
    def user_list():
        'A simple page from a dabase.'

        db = dbwrap.session()

        users = db.query(model.User).order_by(model.User.name)

        #  any local variables can be used in the template
        return locals()

    #  XXX User list page
    @app.route('/users/all', name='user_table')
    @view('user-table')
    def user_table():
        'A simple page from a dabase.'

        db = dbwrap.session()

        users = db.query(model.User).order_by(model.User.id)

        #  any local variables can be used in the template
        return locals()

    #  XXX User details dynamically-generated URL
    @app.route('/users/<username>', name='user')  # XXX URL to page
    @view('user')                                 # XXX Name of template
    def user_info(username):
        'A simple page from a dabase.'

        user = model.user_by_name(username)

        #  any local variables can be used in the template
        return locals()

    #  XXX A simple form example, not used on the demo site
    @app.get('/form', name='form')                # XXX URL to page
    @app.post('/form')  
    @view('form')                                 # XXX Name of template
    def form():
        'A simple form processing example'

        form = NewUserFormProcessor(request.forms.decode())
        if request.method == 'POST' and form.validate():
            #  XXX Do something with form fields here

            #  if successful
            redirect('/users/%s' % form.name.data)

        #  any local variables can be used in the template
        return locals()

    #  XXX Create a new user, form processing, including GET and POST
    @app.get('/new-user', name='user_new')        # XXX GET URL to page
    @app.post('/new-user')                        # XXX POST URL to page
    @view('user-new')                             # XXX Name of template
    def new_user():
        'A sample of interacting with a form and a database.'

        form = NewUserFormProcessor(request.forms.decode())

        if request.method == 'POST' and form.validate():
            db = dbwrap.session()

            sean = model.User(
                    full_name=form.full_name.data, name=form.name.data,
                    email_address=form.email_address.data)
            db.add(sean)
            db.commit()

            redirect(app.get_url('user', username=form.name.data))

        #  any local variables can be used in the template
        return locals()

    #  REQUIRED: return the application handle herre
    return app
