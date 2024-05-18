# Generated by Django 5.0.6 on 2024-05-17 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodbot', '0004_alter_first_id_alter_month_id_alter_seven_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='first',
            name='id',
            field=models.CharField(default='8313d353ce304eea997ca993337b4161', max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='main',
            name='lineid',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='month',
            name='id',
            field=models.CharField(default='9236df7585f64b818ab778191661fdb0', max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='seven',
            name='id',
            field=models.CharField(default='728886cdde4f46b984d58e68f1f707b8', max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='threemonth',
            name='id',
            field=models.CharField(default='2cc03261ac08457b8ee0ac9ab4a4f510', max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='twomonth',
            name='id',
            field=models.CharField(default='eafe46d93bf94eb29036775ebf11bd63', max_length=32, primary_key=True, serialize=False),
        ),
    ]
