# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 03:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import fitting.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fitting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=fitting.models.user_directory_path, verbose_name='File Model')),
                ('time_added', models.DateTimeField(auto_now_add=True, verbose_name='Time File Added')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User who added the file')),
            ],
        ),
        migrations.CreateModel(
            name='FloatValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='IntValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('wall', models.TextField()),
                ('descriptions', models.ManyToManyField(to='fitting.Description')),
                ('groups', models.ManyToManyField(to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='pyMeasureKnowledgeSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property', models.CharField(max_length=500)),
                ('units', models.CharField(max_length=500)),
                ('property_description', models.CharField(max_length=500)),
                ('property_type', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='TextValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='description',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitting.Entity'),
        ),
        migrations.AddField(
            model_name='description',
            name='float_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitting.FloatValue'),
        ),
        migrations.AddField(
            model_name='description',
            name='int_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitting.IntValue'),
        ),
        migrations.AddField(
            model_name='description',
            name='pyMeasure_ks',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitting.pyMeasureKnowledgeSystem'),
        ),
        migrations.AddField(
            model_name='description',
            name='text_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitting.TextValue'),
        ),
    ]
