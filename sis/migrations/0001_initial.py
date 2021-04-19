# Generated by Django 3.1.2 on 2021-04-19 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('code', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('credit', models.FloatField(null=True)),
                ('theoretical', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('tutorial', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('lab', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('is_compulsary', models.BooleanField()),
                ('ects', models.FloatField(default=0, null=True)),
                ('prerequisites', models.CharField(max_length=1000)),
                ('class_restrictions', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('full_name', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('code', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('parsed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('code', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('num', models.PositiveSmallIntegerField()),
                ('code', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sis.curriculum')),
            ],
        ),
        migrations.CreateModel(
            name='SemesterCourseSlot',
            fields=[
                ('code', models.CharField(max_length=35, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('courses', models.ManyToManyField(to='sis.Course')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sis.semester')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=200)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sis.faculty')),
            ],
        ),
        migrations.AddField(
            model_name='curriculum',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sis.program'),
        ),
    ]