# Generated by Django 3.2.25 on 2025-02-06 10:38

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=255)),
                ('status', models.CharField(choices=[('Cancelled', 'Completed'), ('Pending', 'Pending'), ('Progress', 'Progress'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('due_date', models.DateField(blank=True)),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
        ),
    ]
