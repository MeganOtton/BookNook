# Generated by Django 4.2.19 on 2025-03-19 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0010_alter_profile_hidden_books'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomShelf',
        ),
    ]
