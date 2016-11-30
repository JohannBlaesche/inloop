# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-02 13:17
from __future__ import unicode_literals

from django.db import migrations, models
import inloop.accounts.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_dj10_usernamevalidator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mat_num',
            field=models.IntegerField(help_text='Matriculation number', null=True, validators=[inloop.accounts.validators.validate_mat_num]),
        ),
    ]