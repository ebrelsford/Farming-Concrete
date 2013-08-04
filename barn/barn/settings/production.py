from .base import *


DEBUG = False
TEMPLATE_DEBUG = False

EMAIL_HOST = get_env_variable('FARMING_CONCRETE_EMAIL_HOST')
EMAIL_HOST_USER = get_env_variable('FARMING_CONCRETE_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('FARMING_CONCRETE_EMAIL_HOST_PASSWORD')

ALLOWED_HOSTS = [
    '.farmingconcrete.org',
]
