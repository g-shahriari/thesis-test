# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-26 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllShoppingFromTaleqaniToFatemi',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('long', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('type', models.CharField(blank=True, max_length=254, null=True)),
                ('name', models.CharField(blank=True, max_length=254, null=True)),
                ('geom', models.TextField(blank=True, null=True)),
                ('first_category', models.BigIntegerField(blank=True, null=True)),
                ('second_category', models.IntegerField(blank=True, null=True)),
                ('third_category', models.IntegerField(blank=True, null=True)),
                ('product_code', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'all_shopping_from_taleqani_to__fatemi',
                'managed': False,
            },
        ),
    ]
