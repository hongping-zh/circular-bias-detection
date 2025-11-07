"""
WSGI configuration for PythonAnywhere deployment
"""
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/你的用户名/circular-bias-detection/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import Flask app
from app import app as application

# For PythonAnywhere
if __name__ == "__main__":
    application.run()
