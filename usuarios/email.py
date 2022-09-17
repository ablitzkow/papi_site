from django.db.models import F, Func, Value
if '@gmail.com' in email:
    email_gmail_spam = email.replace('.', '')
    user = User.objects.annotate(
        fixed_email=Func(
            F('email'),
            Value('.'), Value(''),
            function='replace',
        )
    ).filter(fixed_email=email_gmail_spam)

    if user.exists():
        message.error("Ja existe um usuário com este email cadastrado.")