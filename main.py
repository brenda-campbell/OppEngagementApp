from flask.cli import FlaskGroup
from website import construct_app

app = construct_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()