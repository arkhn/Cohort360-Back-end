# Generated by Django 2.2.9 on 2021-03-10 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorations', '0002_auto_20210216_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='datedmeasure',
            name='measure_alive',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datedmeasure',
            name='measure_deceased',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datedmeasure',
            name='measure_female',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datedmeasure',
            name='measure_male',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datedmeasure',
            name='measure_unknown',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cohortresult',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cohortresult',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
