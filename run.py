# run.py

from app import create_app, db
from app.models import Event, Package

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Event': Event, 'Package': Package}

if __name__ == '__main__':
    app.run(debug=True)
