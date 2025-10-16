import re


def validation(email, first_name, last_name, phone_number, password1, password2, data_entry):

    errors = []

    if password1 != password2:
        errors.append(('password2', 'Пароль не совпадает'))

    if len(password1) <= 5:
        errors.append(('password1', 'Короткий пароль'))

    if sum([password1.count(i) for i in '0123456789']) == 0:
        errors.append(('password1', 'Используйте цифры'))

    if not re.fullmatch("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", phone_number):
        errors.append(('phone_number', 'Не верый номер телефона'))

    if not data_entry:
        errors.append(('data_entry', 'Нет согласия'))

    return errors


