# Generated by Django 4.0.4 on 2022-05-14 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BodyPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique=True)),
            ],
            options={
                'verbose_name': 'Body part',
                'verbose_name_plural': 'Body parts',
            },
        ),
        migrations.CreateModel(
            name='Pill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Pill',
                'verbose_name_plural': 'Pills',
            },
        ),
        migrations.CreateModel(
            name='Simptom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique=True)),
                ('body_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='simptoms', to='pill.bodypart')),
            ],
            options={
                'verbose_name': 'Simptom',
                'verbose_name_plural': 'Simptoms',
            },
        ),
        migrations.CreateModel(
            name='SimptomPill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pill.pill')),
                ('simptom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pill.simptom')),
            ],
            options={
                'verbose_name': 'Simptom pill',
                'verbose_name_plural': 'Simptom pills',
            },
        ),
    ]