# Generated by Django 4.0.4 on 2022-06-07 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pill', '0004_remove_pill_text_bodypart_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pharmacotherapeutic_group', models.TextField(default=' ')),
                ('description', models.TextField(default=' ')),
                ('indication', models.TextField(default=' ')),
                ('application_method', models.TextField(default=' ')),
                ('pill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pill.pill')),
            ],
            options={
                'verbose_name': 'Text',
                'verbose_name_plural': 'Texts',
            },
        ),
    ]