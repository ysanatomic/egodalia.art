# Generated by Django 4.0.2 on 2022-02-07 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_category_visualart_categories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-created_at'], 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='visualart',
            options={'ordering': ['-created_at'], 'verbose_name': 'art', 'verbose_name_plural': 'arts'},
        ),
        migrations.AddField(
            model_name='visualart',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
