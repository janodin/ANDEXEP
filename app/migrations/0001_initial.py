# Generated by Django 4.2.11 on 2024-03-27 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StressLevelRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('bmi_category', models.CharField(max_length=20)),
                ('phq1', models.IntegerField()),
                ('phq2', models.IntegerField()),
                ('phq3', models.IntegerField()),
                ('phq4', models.IntegerField()),
                ('phq5', models.IntegerField()),
                ('phq6', models.IntegerField()),
                ('phq7', models.IntegerField()),
                ('phq8', models.IntegerField()),
                ('phq9', models.IntegerField()),
                ('phq_score_total', models.IntegerField()),
                ('is_suicide', models.CharField(max_length=10)),
                ('stress_level', models.CharField(max_length=20)),
                ('recommendations', models.TextField()),
            ],
        ),
    ]
