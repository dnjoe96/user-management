from . import create_app, db
from .user.models.user_model import User

app = create_app()


@app.route('/')
def index():
    return 'I work'


# The following function in microblog.py creates a shell context
# that adds the database instance and models to the shell session:
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
