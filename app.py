from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_bcrypt import Bcrypt
import re
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    sexo = db.Column(db.String(10))
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    especialidade = db.Column(db.String(200), nullable=False)
    data_hora = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(200))
    paciente = db.relationship('Paciente', backref=db.backref('consultas', lazy=True))
    medico = db.relationship('Medico', backref=db.backref('consultas', lazy=True))

class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    sexo = db.Column(db.String(10))
    crm = db.Column(db.String(6), nullable=False)
    especialidades = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))

with app.app_context():
    db.create_all()

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    if cpf == cpf[0] * len(cpf):
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

@app.route('/')
@login_required
def index():
    pacientes = Paciente.query.all()
    hoje = datetime.now().strftime('%Y-%m-%d')
    consultas = Consulta.query.filter(Consulta.data_hora.startswith(hoje)).all()
    pacientes_dict = [
        {
            'id': paciente.id,
            'nome': paciente.nome,
            'idade': paciente.idade,
            'sexo': paciente.sexo,
            'cpf': paciente.cpf,
            'endereco': paciente.endereco,
            'telefone': paciente.telefone,
            'email': paciente.email
        } for paciente in pacientes
    ]
    consultas_dict = [
        {
            'id': consulta.id,
            'paciente_nome': consulta.paciente.nome,
            'medico_nome': consulta.medico.nome,
            'especialidade': consulta.especialidade,
            'data_hora': consulta.data_hora,
            'descricao': consulta.descricao
        } for consulta in consultas
    ]
    return render_template('index.html', pacientes=pacientes_dict, consultas=consultas_dict)

@app.route('/novo_paciente', methods=['GET', 'POST'])
@login_required
def novo_paciente():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        sexo = request.form['sexo']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        email = request.form['email']

        if not validar_cpf(cpf):
            flash('CPF inválido. Por favor, tente novamente.', 'danger')
            return render_template('novo_paciente.html')

        paciente_existente = Paciente.query.filter_by(cpf=cpf).first()
        if paciente_existente:
            flash('Paciente já cadastrado.', 'warning')
            return render_template('novo_paciente.html')

        novo_paciente = Paciente(nome=nome, idade=idade, sexo=sexo, cpf=cpf, endereco=endereco, telefone=telefone, email=email)
        db.session.add(novo_paciente)
        db.session.commit()
        flash('Paciente cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('novo_paciente.html')

@app.route('/excluir_paciente/<int:paciente_id>', methods=['GET'])
@login_required
def excluir_paciente(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    db.session.delete(paciente)
    db.session.commit()
    flash('Paciente excluído com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/pesquisar_pacientes', methods=['GET', 'POST'])
@login_required
def pesquisar_pacientes():
    if request.method == 'POST':
        termo_pesquisa = request.form['termo_pesquisa']
        filtro = request.form['filtro']
        if filtro == 'nome':
            pacientes = Paciente.query.filter(Paciente.nome.like(f'%{termo_pesquisa}%')).all()
        elif filtro == 'cpf':
            pacientes = Paciente.query.filter(Paciente.cpf.like(f'%{termo_pesquisa}%')).all()
        pacientes_dict = [
            {
                'id': paciente.id,
                'nome': paciente.nome,
                'idade': paciente.idade,
                'sexo': paciente.sexo,
                'cpf': paciente.cpf,
                'endereco': paciente.endereco,
                'telefone': paciente.telefone,
                'email': paciente.email
            } for paciente in pacientes
        ]
        return render_template('pesquisar_pacientes.html', pacientes=pacientes_dict)
    return render_template('pesquisar_pacientes.html', pacientes=[])

@app.route('/cadastro_medico', methods=['GET', 'POST'])
@login_required
def novo_medico():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        sexo = request.form['sexo']
        crm = request.form['crm']
        especialidades = request.form['especialidades']
        telefone = request.form['telefone']
        email = request.form['email']

        novo_medico = Medico(nome=nome, idade=idade, sexo=sexo, crm=crm, especialidades=especialidades, telefone=telefone, email=email)
        db.session.add(novo_medico)
        db.session.commit()
        flash('Médico cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('cadastro_medico.html')

@app.route('/nova_consulta', methods=['GET', 'POST'])
@login_required
def nova_consulta():
    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        data_hora = request.form['data_hora']
        descricao = request.form['descricao']

        nova_consulta = Consulta(paciente_id=paciente_id, data_hora=data_hora, descricao=descricao)
        db.session.add(nova_consulta)
        db.session.commit()
        flash('Consulta agendada com sucesso!', 'success')
        return redirect(url_for('index'))
    pacientes = Paciente.query.all()
    return render_template('nova_consulta.html', pacientes=pacientes)

@app.route('/cadastro_medico_page', methods=['GET', 'POST'])
@login_required
def cadastro_medico_page():
    return render_template('cadastro_medico_page.html')

@app.route('/agendar/<int:paciente_id>', methods=['GET', 'POST'])
@login_required
def agendar(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    medicos = Medico.query.all()
    if request.method == 'POST':
        medico_id = request.form['medico_id']
        especialidade = request.form['especialidade']
        data_hora = request.form['data_hora']
        descricao = request.form['descricao']
        nova_consulta = Consulta(
            paciente_id=paciente_id,
            medico_id=medico_id,
            especialidade=especialidade,
            data_hora=data_hora,
            descricao=descricao
        )
        db.session.add(nova_consulta)
        db.session.commit()
        flash('Consulta agendada com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('agendar.html', paciente=paciente, medicos=medicos)

if __name__ == '__main__':
    app.run(debug=True)