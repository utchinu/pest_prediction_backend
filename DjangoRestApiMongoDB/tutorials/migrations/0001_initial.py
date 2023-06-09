# Generated by Django 3.0.5 on 2020-10-15 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('crop', models.CharField(default='', max_length=200)),
                ('pest', models.CharField(default='', max_length=200)),
                ('state_name', models.CharField(default='', max_length=200)),
                ('district_name', models.CharField(default='', max_length=200)),
                ('lattitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('count', models.IntegerField()),
            ],
        ),
    ]
