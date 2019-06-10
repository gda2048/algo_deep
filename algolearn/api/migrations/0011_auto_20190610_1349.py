# Generated by Django 2.2.1 on 2019-06-10 13:49

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_quiz_theory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='answers',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='questions',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
