# Generated by Django 3.0.5 on 2020-10-17 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
