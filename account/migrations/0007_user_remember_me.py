# Generated by Django 5.0.4 on 2024-05-07 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='remember_me',
            field=models.BooleanField(default=False),
        ),
    ]
