# Generated by Django 4.2.6 on 2024-02-07 07:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BillSoftwareapp', '0014_creditnoteitem_refno_alter_history_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditnoteitem',
            name='refno',
        ),
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateField(default=datetime.date(2024, 2, 7)),
        ),
    ]
