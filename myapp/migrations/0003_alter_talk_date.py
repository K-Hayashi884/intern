# Generated by Django 3.2 on 2021-05-06 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_talk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='date',
            field=models.CharField(max_length=1000),
        ),
    ]
