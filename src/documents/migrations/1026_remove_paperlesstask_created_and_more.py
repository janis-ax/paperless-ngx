# Generated by Django 4.0.7 on 2022-09-02 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_results', '0011_taskresult_periodic_task_name'),
        ('documents', '1025_alter_savedviewfilterrule_rule_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paperlesstask',
            name='created',
        ),
        migrations.RemoveField(
            model_name='paperlesstask',
            name='name',
        ),
        migrations.RemoveField(
            model_name='paperlesstask',
            name='started',
        ),
        migrations.RemoveField(
            model_name='paperlesstask',
            name='task_id',
        ),
        migrations.AlterField(
            model_name='paperlesstask',
            name='attempted_task',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attempted_task', to='django_celery_results.taskresult'),
        ),
    ]
