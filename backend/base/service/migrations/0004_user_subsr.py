# Generated by Django 4.2.6 on 2023-11-07 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0003_alter_user_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="subsr",
            field=models.CharField(default=200, max_length=15),
            preserve_default=False,
        ),
    ]