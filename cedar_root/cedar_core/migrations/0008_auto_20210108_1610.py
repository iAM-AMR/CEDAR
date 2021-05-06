# Generated by Django 3.1.2 on 2021-01-08 21:10

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0007_auto_20201216_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='factor_title',
            field=models.CharField(blank=True, help_text='A title that describes the factor, in title case. Factors including antimicrobial use should be formatted as "AntiX Use" where AntiX is the antimicrobial(s) administered (e.g. Bambermycin Use, Ceftiofur Use). Factors comparing organic / no antimicrobial use / free-range / conventional production should be titled "Production Type"', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='factor',
            name='group_exposed',
            field=models.CharField(blank=True, help_text='A brief description of the exposed group, in title case. Comparison groups are allocated as described in the literature. Factors including antimicrobial use are always given with "AntiX Use" for the exposed group, where AntiX is the antimicrobial(s) administered. The dose should be provided in the main factor description, unless the factor is a comparison of two doses', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='factor',
            name='group_referent',
            field=models.CharField(blank=True, help_text='A brief description of the referent (unexposed) group, in title case. Comparison groups are allocated as described in the literature. If no allocation is provided, the less interventionist (or default practice) should be used as the referent. Factors including antimicrobial use are always given with the less interventionist as the referent (i.e. with "No Use" as the referent group or the lower dose as the referent). The dose should be provided in the main factor description, unless the factor is a comparison of two doses', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='factor',
            name='host_01',
            field=models.ForeignKey(blank=True, help_text='The host animal from which the microbe was isolated', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.host_01'),
        ),
        migrations.AlterField(
            model_name='factor',
            name='host_02',
            field=models.ForeignKey(blank=True, help_text='The host subtype from which the microbe was isolated', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.host_02'),
        ),
        migrations.AlterField(
            model_name='factor',
            name='microbe_01',
            field=models.ForeignKey(blank=True, help_text='The microbe assayed for resistance', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.microbe_01'),
        ),
        migrations.AlterField(
            model_name='factor',
            name='microbe_02',
            field=models.ForeignKey(blank=True, help_text='The subtype of the microbe assayed for resistance', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.microbe_02'),
        ),
        migrations.AlterField(
            model_name='factor',
            name='moa_type',
            field=models.ForeignKey(blank=True, help_text='The type of measure of association reported for the factor', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.moa_type'),
        ),
        migrations.AlterField(
            model_name='factor',
            name='moa_unit',
            field=models.ForeignKey(blank=True, help_text='The experimental unit or level of analysis for which the measure of association is presented', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.moa_unit'),
        ),
        migrations.AlterField(
            model_name='factor',
            name='odds_ratio_lo',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The lower (usually 95%) confidence interval of the odds ratio that describes the factor, up to 2 decimal places.', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='factor',
            name='odds_ratio_up',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The upper (usually 95%) confidence interval of the odds ratio that describes the factor, up to 2 decimal places.', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='factor',
            name='place_in_text',
            field=models.CharField(blank=True, help_text='The location of the factor data in-text, i.e. "Table 2". If the data is from the body of the text, use the page and paragraph numbers (Pg. and Para.)', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='factor',
            name='prod_stage_group_allocate',
            field=models.ForeignKey(blank=True, help_text='The production stage at which the groups were allocated (i.e. factor applied)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factors_a', to='cedar_core.production_stage'),
        ),
        migrations.AlterField(
            model_name='factor',
            name='prod_stage_group_observe',
            field=models.ForeignKey(blank=True, help_text='The production stage at which the observations were recorded (i.e. factor observed)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factors_o', to='cedar_core.production_stage'),
        ),
        migrations.AlterField(
            model_name='factor',
            name='resistance',
            field=models.ForeignKey(blank=True, help_text='The antimicrobial for which resistance was assayed.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factors_resistance', to='cedar_core.atc_vet'),
        ),
    ]