# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 11:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backpage', '0002_auto_20170313_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='lessee',
            field=models.OneToOneField(db_column='lessee', default=1, on_delete=django.db.models.deletion.CASCADE, to='backpage.Lessee', verbose_name='货车主id'),
            preserve_default=False,
        ),
    ]