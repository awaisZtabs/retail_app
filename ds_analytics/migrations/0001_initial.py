# Generated by Django 3.1.2 on 2021-05-21 11:27

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('measurement_frames', '0001_initial'),
        ('cameras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PLAConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('point_coords_in_ground_frame', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), null=True, size=8)),
                ('point_coords_in_image', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=8)),
                ('camera', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cameras.camera')),
                ('ground_frame', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='measurement_frames.measurementframe')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
