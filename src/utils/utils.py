from email_validator import validate_email, EmailNotValidError
import phonenumbers

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