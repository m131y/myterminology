# Generated by Django 3.2.10 on 2024-05-26 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultword', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(blank=True, max_length=70)),
                ('word_type', models.CharField(blank=True, max_length=70)),
                ('definition', models.TextField(blank=True)),
                ('pos', models.CharField(blank=True, max_length=70)),
            ],
            options={
                'db_table': 'word',
            },
        ),
    ]
