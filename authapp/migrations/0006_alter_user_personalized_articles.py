# Generated by Django 5.1.4 on 2025-04-10 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_alter_user_about_alter_user_followers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='personalized_articles',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
