# Generated by Django 2.1.7 on 2019-10-18 14:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cohort', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True)),
                ('favorite', models.BooleanField(default=False)),
                ('fhir_groups_ids', models.TextField(validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('type', models.CharField(choices=[('IMPORT_I2B2', 'Imported from i2b2.'), ('MY_ORGANIZATIONS', 'Organizations in which I work.'), ('MY_PATIENTS', 'Patients that passed by all my organizations.')], max_length=20)),
                ('result_size', models.BigIntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_cohorts', to=settings.AUTH_USER_MODEL)),
                ('perimeter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perimeter_cohorts', to='cohort.Perimeter')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Exploration',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True)),
                ('favorite', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_explorations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True)),
                ('favorite', models.BooleanField(default=False)),
                ('data_type_of_query', models.CharField(choices=[('PATIENT', 'FHIR Patient'), ('ENCOUNTER', 'FHIR Encounter')], max_length=9)),
                ('exploration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='explorations.Exploration')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RequestQueryResult',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('result_size', models.BigIntegerField()),
                ('refresh_every_seconds', models.BigIntegerField(default=0)),
                ('refresh_create_cohort', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_request_query_results', to=settings.AUTH_USER_MODEL)),
                ('perimeter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cohort.Perimeter')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorations.Request')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RequestQuerySnapshot',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('serialized_query', models.TextField(default='{}')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_request_query_snapshots', to=settings.AUTH_USER_MODEL)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorations.Request')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='requestqueryresult',
            name='request_query_snapshot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorations.RequestQuerySnapshot'),
        ),
        migrations.AddField(
            model_name='cohort',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_cohorts', to='explorations.Request'),
        ),
        migrations.AddField(
            model_name='cohort',
            name='request_query_snapshot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explorations.RequestQuerySnapshot'),
        ),
    ]
