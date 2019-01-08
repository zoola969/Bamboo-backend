from bamboo import db, create_app
from bamboo.utils import create_superuser

app = create_app()
app.app_context().push()
db.create_all()

create_superuser()
