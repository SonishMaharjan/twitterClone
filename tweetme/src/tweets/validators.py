from django.core.exceptions import ValidationError

def validate_content(value):
    content = value
    if content=="":
        raise ValidationError("can not be a blank content")
    return content
