# wsgi.py (Common Loader for Render/Gunicorn)
import sys
from main import create_app
application = create_app()
