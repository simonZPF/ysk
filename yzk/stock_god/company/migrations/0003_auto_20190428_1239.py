# Generated by Django 2.2 on 2019-04-28 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20190427_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='relation_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('table_name', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(null=True)),
            ],
            options={
                'db_table': 'relation_info',
            },
        ),
        migrations.AlterField(
            model_name='block_trade',
            name='closing_price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='block_trade',
            name='folding_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='block_trade',
            name='transaction_price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='block_trade',
            name='transaction_time',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='block_trade',
            name='turnover',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='block_trade',
            name='turnover_divide_market',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='block_trade',
            name='volume',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='company.industry'),
        ),
        migrations.AlterField(
            model_name='major_contract',
            name='body_relation',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='body_relation', to='company.relation_info'),
        ),
        migrations.AlterField(
            model_name='major_contract',
            name='income_rate',
            field=models.FloatField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='major_contract',
            name='others_relation',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='others_relation', to='company.relation_info'),
        ),
        migrations.AlterField(
            model_name='major_contract',
            name='signing_others',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='signing_others', to='company.company'),
        ),
        migrations.AlterField(
            model_name='major_contract',
            name='up_and_down',
            field=models.FloatField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='merge_reorganization',
            name='transfer_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='merge_reorganization',
            name='turnover',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='ages',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='app_time',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='introduction',
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name='com_relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=20, null=True)),
                ('gmt_date', models.DateField(null=True)),
                ('company_one', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='company_one', to='company.company')),
                ('company_two', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='company_two', to='company.company')),
                ('relation_name', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='relation_name', to='company.relation_info', to_field='name')),
            ],
            options={
                'db_table': 'com_relation',
            },
        ),
    ]
