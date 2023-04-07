from django.core.mail import send_mail


def send_confirmation_email(user, code): #активационный код который приходит на почту
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}'
    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Чтобы активировать Ваш аккаунт, нужно ввести код: \n{full_link}\nНе передавайте этот код никому',
        'manasdyikanov@gmail.com',
        [user],
        fail_silently=False,
    )
