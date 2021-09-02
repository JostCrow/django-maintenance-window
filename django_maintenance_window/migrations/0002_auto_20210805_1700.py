# Generated by Django 3.2 on 2021-08-05 15:00

from django.db import migrations, models
import django.db.models.deletion
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django_maintenance_window', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenancemode',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recurrences', recurrence.fields.RecurrenceField()),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('stop_time', models.TimeField(blank=True, null=True)),
                ('mode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='django_maintenance_window.maintenancemode')),
            ],
        ),
    ]
