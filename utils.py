from django.utils.crypto import get_random_string

def generate_secret_key(filename):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    key = get_random_string(50, chars)
    key_string = 'SECRET_KEY = \'%s\'' % key
    with open(filename, 'w') as f:
        f.write(key_string)
