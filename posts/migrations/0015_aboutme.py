# Generated by Django 4.0.2 on 2022-09-15 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_alter_visualart_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutMe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('body', models.TextField()),
            ],
            options={
                'verbose_name': 'About Me',
                'verbose_name_plural': 'About Me',
            },
        ),
    ]
