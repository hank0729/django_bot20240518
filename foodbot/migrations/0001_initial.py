# Generated by Django 5.0.6 on 2024-05-16 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='First',
            fields=[
                ('id', models.CharField(default='b8a6bd3df8d441f68eb67c56cc9b40b8', max_length=32, primary_key=True, serialize=False)),
                ('lineid', models.TextField()),
                ('q1', models.TextField()),
                ('q2', models.TextField()),
                ('q3', models.TextField()),
                ('q4', models.TextField()),
                ('q5', models.TextField()),
                ('q6', models.TextField()),
                ('q7', models.TextField()),
                ('q8', models.TextField()),
                ('q9', models.TextField()),
                ('q10', models.TextField()),
                ('q11', models.TextField()),
                ('q12', models.TextField()),
                ('q13', models.TextField()),
                ('q14', models.TextField()),
                ('q15', models.TextField()),
                ('q16', models.TextField()),
                ('q17', models.TextField()),
                ('q18', models.TextField()),
                ('q19', models.TextField()),
                ('q20', models.TextField()),
                ('q21', models.TextField()),
                ('q22', models.TextField()),
                ('q23', models.TextField()),
                ('q24', models.TextField()),
                ('q25', models.TextField()),
                ('q26', models.TextField()),
                ('q27', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.CharField(default='46c6ea1974404101b8a5b9d6613f4abc', max_length=32, primary_key=True, serialize=False)),
                ('lineid', models.TextField()),
                ('q1', models.TextField()),
                ('q2', models.TextField()),
                ('q3', models.TextField()),
                ('q4', models.TextField()),
                ('q5', models.TextField()),
                ('q6', models.TextField()),
                ('q7', models.TextField()),
                ('q8', models.TextField()),
                ('q9', models.TextField()),
                ('q10', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Seven',
            fields=[
                ('id', models.CharField(default='27548fdb942443b68497e13d23e411cf', max_length=32, primary_key=True, serialize=False)),
                ('lineid', models.TextField()),
                ('q1', models.TextField()),
                ('q2', models.TextField()),
                ('q3', models.TextField()),
                ('q4', models.TextField()),
                ('q5', models.TextField()),
                ('q6', models.TextField()),
                ('q7', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ThreeMonth',
            fields=[
                ('id', models.CharField(default='6b900d321c4640d29e404626960d85bb', max_length=32, primary_key=True, serialize=False)),
                ('lineid', models.TextField()),
                ('q1', models.TextField()),
                ('q2', models.TextField()),
                ('q3', models.TextField()),
                ('q4', models.TextField()),
                ('q5', models.TextField()),
                ('q6', models.TextField()),
                ('q7', models.TextField()),
                ('q8', models.TextField()),
                ('q9', models.TextField()),
                ('q10', models.TextField()),
                ('q11', models.TextField()),
                ('q12', models.TextField()),
                ('q13', models.TextField()),
                ('q14', models.TextField()),
                ('q15', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TwoMonth',
            fields=[
                ('id', models.CharField(default='0f7f7b7dbe4f4bf8a1b7e992b81b8df0', max_length=32, primary_key=True, serialize=False)),
                ('lineid', models.TextField()),
                ('q1', models.TextField()),
                ('q2', models.TextField()),
                ('q3', models.TextField()),
                ('q4', models.TextField()),
                ('q5', models.TextField()),
                ('q6', models.TextField()),
                ('q7', models.TextField()),
                ('q8', models.TextField()),
                ('q9', models.TextField()),
                ('q10', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_id', models.CharField(max_length=50)),
                ('message_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lineid', models.TextField()),
                ('days', models.IntegerField(default=0)),
                ('first_key', models.TextField()),
                ('seven_key', models.TextField()),
                ('month_key', models.TextField()),
                ('twomonth_key', models.TextField()),
                ('threemonth_key', models.TextField()),
                ('first', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodbot.first')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodbot.month')),
                ('seven', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodbot.seven')),
                ('threemonth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodbot.threemonth')),
                ('twomonth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodbot.twomonth')),
            ],
        ),
    ]
