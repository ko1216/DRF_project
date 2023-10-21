#  Создал суперюзера для проекта, а также в этой команде создал юзера,
#  на котором буду создавать оплаты за курсы и уроки (через шелл дополнительно поставил флаг is_email_verified = True)


from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = {
            'superuser': {
                'email': 'admin@admin.com',
                'first_name': 'admin',
                'last_name': 'django',
                'is_staff': True,
                'is_superuser': True
            },
            1: {
                'email': 'user1@admin.com',
                'first_name': 'user',
                'last_name': '1',
                'is_staff': False,
                'is_superuser': False
            }
        }

        for user in users.values():
            new_user = User.objects.create(
                email=user['email'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                is_staff=user['is_staff'],
                is_superuser=user['is_superuser']
            )

            new_user.set_password('123qwe456rty')
            new_user.save()
