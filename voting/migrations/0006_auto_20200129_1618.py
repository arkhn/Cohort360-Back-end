# Generated by Django 2.2.9 on 2020-01-29 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0005_auto_20200129_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='vote',
            field=models.IntegerField(choices=[(1, 'Positive vote'), (0, 'Neutral vote'), (-1, 'Negative vote')], default=0),
        ),
    ]
