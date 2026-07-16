from email_validator import validate_email, EmailNotValidError
import phonenumbers

from uuid import uuid4
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

load_dotenv()

def validar_email(email: str):
    try:
        email_valido = validate_email(email)
        print(email_valido)
        if email_valido:
            return email
    
    except EmailNotValidError as e:
        print(e)
        return e

def validar_telefone(telefone: str, ddd_default="11"):
    telefone = telefone.strip()

    # remove espaços, parenteses e traços
    digits = "".join(filter(str.isdigit, telefone))

    # se só vier número de celular (9 dígitos), adiciona DDD padrão
    if len(digits) == 9:
        digits = ddd_default + digits

    try:
        parsed = phonenumbers.parse(digits, "BR")

        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.NATIONAL
            )

        return "Número inválido."

    except phonenumbers.NumberParseException as e:
        return f"Erro: {e}"
    

## Funções utils para uploads de vídeos e img:

def allowed_file(filename, allowed_extensions=None):
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    if allowed_extensions is None:
        allowed_extensions = os.getenv(
            "ALLOWED_EXTENSIONS",
            "png,jpg,jpeg,webp,mp4,mov,avi,mkv"
        )

    if isinstance(allowed_extensions, str):
        allowed_extensions = {
            item.strip().lower().lstrip(".")
            for item in allowed_extensions.split(",")
            if item.strip()
        }

    return extension in allowed_extensions

def get_file_type(filename):
    extension = filename.rsplit(".", 1)[1].lower()

    if extension in ["png", "jpg", "jpeg", "webp"]:
        return "image"

    if extension in ["mp4", "mov", "avi", "mkv"]:
        return "video"

    return "unknown"

def generate_unique_filename(filename):
    extension = filename.rsplit(".", 1)[1].lower()
    safe_name = secure_filename(filename)

    unique_name = f"{uuid4().hex}_{safe_name}"

    return unique_name
