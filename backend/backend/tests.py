from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


def test_password_hash_is_argon2():
    plain_password = 'raduguifire'

    hashed_password = make_password(plain_password)
    assert hashed_password.startswith('argon2')

    user = User.objects.create_user(username='username', password=plain_password, email='alguem@host.com')
    assert hashed_password == user.password
