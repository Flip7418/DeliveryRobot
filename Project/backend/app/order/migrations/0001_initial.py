# Generated by Django 4.0.4 on 2022-05-15 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pill', '0002_simptom_pills'),
        ('student', '0002_alter_student_allergy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.CharField(choices=[('pill', 'С таблеткой'), ('simptom', 'С симптомом')], max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('on_moderation', 'В модерации'), ('declined', 'Отклонено'), ('approved_and_on_queue', 'Подтвержден и в очереди'), ('going_to_client', 'На пути к клиенту'), ('at_client', 'У клиента'), ('delivered', 'Доставлено')], default='on_moderation', max_length=128)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_type', models.CharField(choices=[('source', 'Источник'), ('destination', 'Назначение')], max_length=64)),
                ('longitude', models.IntegerField()),
                ('latitude', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Point',
                'verbose_name_plural': 'Points',
            },
        ),
        migrations.CreateModel(
            name='OrderSimptom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('simptom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pill.simptom')),
            ],
            options={
                'verbose_name': 'Order simptom',
                'verbose_name_plural': 'Order simptoms',
            },
        ),
        migrations.CreateModel(
            name='OrderPill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('pill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pill.pill')),
            ],
            options={
                'verbose_name': 'Order pill',
                'verbose_name_plural': 'Order pills',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='destination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='order.point'),
        ),
        migrations.AddField(
            model_name='order',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
    ]
