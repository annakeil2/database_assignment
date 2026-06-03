from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__, template_folder='../html', static_url_path='', static_folder='../static')
print("Hello!")

#app.config.from_object("config.Config")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://app:mystrongPW26A!@localhost/database_assignment"

db.init_app(app)
    
with app.app_context():
    import routes  

    db.create_all()  

if __name__ == '__main__':
    app.run(debug=True)

