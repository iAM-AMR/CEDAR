# Generated by Django 3.1.7 on 2022-03-08 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0080_auto_20220308_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='v2_fk_m_reference_history_id',
            field=models.ForeignKey(blank=True, help_text='The ID of the m_reference_history table for the latest action entry', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.reference_join_reference_history'),
        ),
        migrations.AddField(
            model_name='reference',
            name='v2_fk_reference_history_last_action',
            field=models.ForeignKey(blank=True, help_text='The ID of the last action associated with the reference in the v2 reference_history scheme. This is for migration to CW reference history and status.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.reference_history_action'),
        ),
        migrations.AddField(
            model_name='reference',
            name='v2_fk_user_reference_history_last_action',
            field=models.ForeignKey(blank=True, help_text='The ID of the user who was associated with the last action in the v2 reference_history scheme. This is for migration to CW reference history and status', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.legacy_user'),
        ),
    ]
