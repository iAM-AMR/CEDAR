# Generated by Django 3.1.7 on 2022-03-04 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0077_auto_20220304_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reference',
            name='dep_topic_tab_has_topic',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='dep_topic_tab_host_free',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='dep_topic_tab_microbe_free',
        ),
    ]