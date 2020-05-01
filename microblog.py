from app import create_app, db, cli
from app.models import User, Cinemas, Facility, M_Category, Reports

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Cinemas': Cinemas, 'Reports': Reports,
            'Facility': Facility, 'M_Category': M_Category}
