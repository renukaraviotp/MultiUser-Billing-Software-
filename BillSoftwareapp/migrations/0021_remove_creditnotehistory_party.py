# Generated by Django 4.2.6 on 2024-02-16 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BillSoftwareapp', '0020_creditnotehistory_party_alter_history_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditnotehistory',
            name='party',
        ),
    ]
