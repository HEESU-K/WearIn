# Generated by Django 4.0.3 on 2024-05-06 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='justTESTtable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=24)),
                ('test_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TESTtableTWO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testCol', models.CharField(max_length=24)),
                ('testRow', models.DateTimeField()),
            ],
        ),
    ]