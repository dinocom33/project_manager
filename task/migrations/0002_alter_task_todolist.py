# Generated by Django 5.0.4 on 2024-06-03 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
        ('todolist', '0003_remove_todolist_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='todolist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='todolist.todolist'),
        ),
    ]