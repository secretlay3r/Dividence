import random
import string

def generate_random_title(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))