from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()

with open('secret_key.txt', 'w') as f:
    f.write(secret_key)