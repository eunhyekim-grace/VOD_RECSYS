# Generated by Django 4.2.6 on 2023-10-20 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0002_alter_user_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]
