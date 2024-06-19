# <a id="chapter-1"></a>Visão Geral

O Sistema de Gestão Hospitalar é uma aplicação web desenvolvida para gerenciar pacientes, médicos e suas consultas de forma 
eficiente. Ele é construído usando Flask, SQLAlchemy e Bootstrap, fornecendo uma interface robusta e fácil de usar para a equipe do hospital.

# Índeces

- [Visão Geral](chapter-1)
- [Características](chapter-2)
- [Instalação](chapter-3)
    - [Pré-requisitos](chapter-3.1)
    - [Configurar](chapter-3.2)
- [Uso](chapter-4)
- [Esquema de banco de dados](chapter-5)
- [Rotas](chapter-6)
- [Tecnologias Utilizadas](chapter-7)


## <a id="chapter-2"></a>Características

- Autenticação de usuário (registro, login, logout)
- Operações CRUD para pacientes
- Operações CRUD para Médicos
- Agende e gerencie consultas
- Funcionalidade de pesquisa para pacientes
- Design responsivo com Bootstrap

## <a id="chapter-3"></a>Instalação

<a id="chapter-3.1"></a>Pré-requisitos
- Python 3.7+
- pip (instalador do pacote Python)
- SQLite (ou qualquer outro banco de dados preferido, embora possa ser necessária configuração adicional)
- Git (para clonar o repositório)

## <a id="chapter-3.2"></a>Configurações

### 1. Clone o repositório:
~~~
git clone https://github.com/yourusername/Sistema_Gestao_Clinica.git
cd Sistema-Gestao-Clinica
~~~~

### 2. Crie e ative um ambiente virtual:

~~~
python3 -m venv venv
source venv/bin/activate  # Ou Windows use `venv\Scripts\activate`
~~~

### 3. Instale os pacotes necessários:

~~~
pip install -r requirements.txt
~~~

### 4. Configure o banco de dados:

Inicialize o banco de dados e aplique as migrações:

~~~
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
~~~

### 5. Execute o sistema:

~~~
flask run
~~~

O sistema estará disponível em http://127.0.0.1:5000.

## <a id="chapter-4"></a>Uso

- Registre um novo usuário: Navegue até a página de registro (/register) e crie uma nova conta.
- Login: Use a página de login (/login) para autenticar.
- Dashboard: Após o login, você será redirecionado para o dashboard onde poderá gerenciar pacientes, médicos e consultas.
- Adicionar um Paciente: Navegue até /novo_paciente para adicionar um novo paciente.
- um Médico: Navegue até /cadastro_medico para adicionar um novo médico.
- Agendar uma consulta: Use a página de agendamento disponível na visualização de detalhes do paciente para agendar uma nova consulta.
- Pesquisar Pacientes: Utilize a funcionalidade de busca para encontrar pacientes por nome, CPF, telefone ou e-mail.

## <a id="chapter-5"></a>Database Schema
### User

- 'id': Integer, primary key
- 'username': String, unique, not null
- 'password': String, not null

### Pacientes 

- 'id': Integer, primary key
- 'nome': String, not null
- 'idade': Integer
- 'sexo': String
- 'cpf': String, unique, not null
- 'endereco': String
- 'telefone': String
- 'email': String

### Médicos

- 'id': Integer, primary key
- 'nome': String, not null
- 'idade': Integer
- 'sexo': String
- 'crm': String, not null
- 'especialidades': String
- 'telefone': String
- 'email': String

### Consultas

- 'id': Integer, primary key
- 'paciente_id': Integer, foreign key to Patient
- 'medico_id': Integer, foreign key to Doctor
- 'especialidade': String, not null
- 'data_hora': String', not null
- 'descricao': String

## <a id="chapter-6"></a>Rotas
### Autenticação

- 'GET /register': Registration page
- 'POST /register': Handle user registration
- 'GET /login': Login page
- 'POST /login': Handle user login
- 'GET /logout': Logout user

### Pacientes 

- GET /novo_paciente: Adicionar novo formulário de paciente
- POST /novo_paciente: Lidar com a criação de novos pacientes
- GET /excluir_paciente/<int:paciente_id>: Excluir paciente
- GET /pesquisar_pacientes: Formulário de busca de pacientes
- POST /pesquisar_pacientes: Tratar busca de pacientes

### Médicos

- GET /cadastro_medico: Adicionar novo formulário médico
- POST /cadastro_medico: Lidar com criação de novo médico

### Consultas

- GET /agendar/<int:paciente_id>: Formulário de agendamento de consulta
- POST /agendar/<int:paciente_id>: Trata do agendamento de uma nova consulta

### Em geral

- GET/: Dashboard mostrando consultas e pacientes de hoje

## <a id="chapter-7"></a>Tecnologias utilizadas:

- [Python](https://www.python.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Bootstrap](https://getbootstrap.com/)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
