from django import template

register = template.Library()

@register.filter
def fix_test_type(value):
    # Split the string by ", "
    parts = value.split(", ")
    result = []
    current_word = []
    for part in parts:
        if part != "":
            current_word.append(part)
        else:
            if current_word:
                result.append(''.join(current_word))
                current_word = []
    # Append the last word if there’s anything in current_word
    if current_word:
        result.append(''.join(current_word))
    # Join words with a space
    return ' '.join(result)