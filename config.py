import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB

ALLOWED_EXTENSIONS = {"apk"}
