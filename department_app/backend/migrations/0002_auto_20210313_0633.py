# Generated by Django 3.1.7 on 2021-03-13 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employee",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="second_name",
        ),
        migrations.AddField(
            model_name="employee",
            name="fullname",
            field=models.CharField(default=123, max_length=256),
            preserve_default=False,
        ),
    ]
