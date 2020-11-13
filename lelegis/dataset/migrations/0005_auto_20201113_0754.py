# Generated by Django 3.1.3 on 2020-11-13 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0004_auto_20201111_0954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pesquisanode',
            old_name='restritivo',
            new_name='ping_restritivo',
        ),
        migrations.AddField(
            model_name='pesquisanode',
            name='result_restritivo',
            field=models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False, verbose_name='Restrige aprofundamento da árvore em caso de erro'),
        ),
    ]