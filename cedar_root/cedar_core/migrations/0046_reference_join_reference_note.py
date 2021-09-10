# Generated by Django 3.1.7 on 2021-09-09 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0045_delete_reference_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='reference_join_reference_note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, help_text='Notes', null=True)),
                ('resolved', models.BooleanField(default=False, help_text='Specifies whether or not the note was resolved or addressed')),
                ('is_apply_factor', models.BooleanField(default=False, help_text='The note relates to factor-level information, and should be included as a note with all factors')),
                ('fk_note_ref_id', models.ForeignKey(blank=True, help_text='The reference that this note refers to', null=True, on_delete=django.db.models.deletion.CASCADE, to='cedar_core.reference', to_field='other_reference_id')),
                ('fk_user_id', models.ForeignKey(blank=True, help_text='The user who made the note', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.legacy_user')),
            ],
        ),
    ]
