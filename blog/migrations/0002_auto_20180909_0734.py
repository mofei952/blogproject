# Generated by Django 2.1.1 on 2018-09-09 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='follow_users',
            field=models.ManyToManyField(related_name='_user_follow_users_+', to='blog.User'),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
