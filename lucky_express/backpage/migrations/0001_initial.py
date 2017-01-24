# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 12:38
from __future__ import unicode_literals

import backpage.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(max_length=128)),
                ('fee', models.FloatField(default=0)),
                ('time', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'advertisement',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starttime', models.DateField(auto_now=True)),
                ('endtime', models.DateField(null=True)),
                ('startplace', models.CharField(max_length=32, null=True)),
                ('endplace', models.CharField(max_length=32, null=True)),
                ('fee', models.FloatField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('accepttime', models.DateField(null=True)),
                ('finishtime', models.DateField(null=True)),
                ('remark', models.CharField(max_length=256)),
                ('status', backpage.models.TinyIntField(choices=[(0, '保存订单'), (1, '预定订单'), (2, '发起订单'), (3, '订单被接受'), (4, '完成订单'), (5, '订单未完成结束')], default=0)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now=True)),
                ('remark', models.CharField(max_length=512)),
                ('score', models.IntegerField(default=-1)),
            ],
            options={
                'db_table': 'service',
            },
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=18)),
                ('load', models.FloatField(default=0)),
                ('width', models.FloatField(default=0)),
                ('heigth', models.FloatField(default=0)),
                ('length', models.FloatField(default=0)),
                ('ctype', backpage.models.TinyIntField(choices=[(0, '待审核'), (1, '无类型'), (2, '普通货车'), (3, '厢式货车'), (4, '封闭货车'), (5, '罐式货车'), (6, '平板货车'), (7, '集装厢车'), (8, '自卸货车'), (9, '特殊结构货车')], db_column='type', default=0)),
                ('modelinfo', models.CharField(max_length=256, null=True)),
                ('remark', models.CharField(max_length=32, null=True)),
            ],
            options={
                'db_table': 'truck',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', backpage.models.FixedCharField(max_length=11)),
                ('name', models.CharField(default='无名', max_length=128, null=True)),
                ('signup_time', models.DateField(auto_now=True)),
                ('token', models.CharField(max_length=64, null=True)),
                ('u_type', backpage.models.TinyIntField(choices=[(0, '未分组'), (1, '租车人'), (2, '货车司机'), (3, '待审核用户')], db_column='type', default=0)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Lessee',
            fields=[
                ('id', models.OneToOneField(db_column='id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='backpage.User')),
                ('position', models.CharField(max_length=128, null=True)),
                ('score', models.IntegerField(default=0)),
                ('realname', models.CharField(max_length=128)),
                ('ci', models.CharField(max_length=18, null=True)),
            ],
            options={
                'db_table': 'lessee',
            },
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.OneToOneField(db_column='id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='backpage.User')),
                ('position', models.CharField(max_length=128, null=True)),
                ('score', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'rental',
            },
        ),
        migrations.AddField(
            model_name='service',
            name='customer',
            field=models.ForeignKey(db_column='customer', on_delete=django.db.models.deletion.CASCADE, to='backpage.User'),
        ),
        migrations.AddField(
            model_name='service',
            name='offer',
            field=models.ForeignKey(db_column='offer', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='truck',
            name='lessee',
            field=models.ForeignKey(db_column='lessee', on_delete=django.db.models.deletion.CASCADE, to='backpage.Lessee'),
        ),
        migrations.AddField(
            model_name='orders',
            name='lessee',
            field=models.ForeignKey(db_column='lessee', null=True, on_delete=django.db.models.deletion.CASCADE, to='backpage.Lessee'),
        ),
        migrations.AddField(
            model_name='orders',
            name='rental',
            field=models.ForeignKey(db_column='rental', on_delete=django.db.models.deletion.CASCADE, to='backpage.Rental'),
        ),
    ]
