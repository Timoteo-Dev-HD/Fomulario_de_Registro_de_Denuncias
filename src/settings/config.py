from dotenv import load_dotenv
import os

load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
PUBLIC_STATIC_DIRS = (
    os.path.join(PROJECT_ROOT, "src", "views", "static"),
    os.path.join(PROJECT_ROOT, "static"),
)

def _parse_extensions(value):
    return {
        extension.strip().lower().lstrip(".")
        for extension in value.split(",")
        if extension.strip()
    }

def _resolve_upload_folder():
    upload_folder = os.getenv("UPLOAD_FOLDER")

    if not upload_folder:
        resolved = os.path.join(PROJECT_ROOT, "instance", "uploads", "denuncias")
    elif os.path.isabs(upload_folder):
        resolved = upload_folder
    else:
        resolved = os.path.join(PROJECT_ROOT, upload_folder)

    resolved = os.path.abspath(resolved)

    for static_dir in PUBLIC_STATIC_DIRS:
        if os.path.commonpath([resolved, static_dir]) == static_dir:
            raise RuntimeError("UPLOAD_FOLDER cannot be inside a public static directory.")

    return resolved

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = _resolve_upload_folder()
    ALLOWED_EXTENSIONS = _parse_extensions(
        os.getenv("ALLOWED_EXTENSIONS", "png,jpg,jpeg,webp,mp4,mov,avi,mkv")
    )
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
