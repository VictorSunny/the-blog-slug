# Generated by Django 5.1.5 on 2025-01-26 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userblog',
            options={'ordering': ('-date_created',)},
        ),
        migrations.AddField(
            model_name='userblog',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
