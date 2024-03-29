# Generated by Django 4.2.6 on 2024-01-09 08:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BillSoftwareapp', '0010_creditnote_address_creditnote_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditnote',
            name='cgst',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='creditnote',
            name='description',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='creditnote',
            name='grandtotal',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='creditnote',
            name='gstin',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='creditnote',
            name='igst',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='creditnote',
            name='roundoff',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='creditnote',
            name='sgst',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='creditnote',
            name='subtotal',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='creditnote',
            name='taxamount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateField(default=datetime.date(2024, 1, 9)),
        ),
        migrations.CreateModel(
            name='CreditnoteItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slno', models.IntegerField(blank=True, default=0, null=True)),
                ('product', models.CharField(max_length=50, null=True)),
                ('hsn', models.CharField(max_length=50, null=True)),
                ('qty', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('tax', models.CharField(max_length=50, null=True)),
                ('discount', models.FloatField(blank=True, default=0, null=True)),
                ('total', models.FloatField(blank=True, default=0, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BillSoftwareapp.company')),
                ('credit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BillSoftwareapp.creditnote')),
                ('staff', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='BillSoftwareapp.staff_details')),
            ],
        ),
    ]
