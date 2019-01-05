1. install python 3.7  
In project directory:  
1. $ python3.7 -m venv venv
1. $ source venv/bin/activate
1. $ pip install -r requirements.txt
1. if its development or testing conf: $ export FLASK_CONFIGURATION={conf_name} 
1. python3
1. \>>> from bamboo import create_app, db
1. \>>> app = create_app()
1. \>>> app.app_context().push()
1. \>>> db.create_all()
