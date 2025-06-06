# Generated by Django 5.1.4 on 2025-04-10 17:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_user_personalized_articles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.CharField(blank=True, default='Happy to be here!', max_length=755),
        ),
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='personalized_articles',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]
