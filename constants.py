import os

URL = ""
USER = "TEST"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SCREENSHOT_ROOT = os.path.join(PROJECT_ROOT, 'screenshots')
CERT_ROOT = os.path.join(PROJECT_ROOT, 'cert')
APP_ROOT = os.path.join(PROJECT_ROOT, 'app')
OUTPUT_ROOT = os.path.join(PROJECT_ROOT, 'tests', 'output')
LOGS_ROOT = os.path.join(PROJECT_ROOT, 'logs')