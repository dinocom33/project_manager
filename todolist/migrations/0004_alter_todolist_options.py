# Generated by Django 5.0.4 on 2024-06-05 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_remove_todolist_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todolist',
            options={'ordering': ['-created_at']},
        ),
    ]
