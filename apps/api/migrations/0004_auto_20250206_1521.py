# Generated by Django 3.2.25 on 2025-02-06 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20250206_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Progress', 'Progress'), ('Completed', 'Completed'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
