# Generated by Django 2.0.4 on 2019-06-26 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_course_is_pay'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'verbose_name_plural': '课程章节表'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('score',), 'verbose_name_plural': '课程表'},
        ),
        migrations.AlterModelOptions(
            name='coursecell',
            options={'verbose_name_plural': '章节小节表'},
        ),
        migrations.AlterModelOptions(
            name='coursetype',
            options={'verbose_name_plural': '分类表'},
        ),
        migrations.AddField(
            model_name='course',
            name='coursetype',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.CourseType', verbose_name='分类'),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='chapter',
            table='chapter',
        ),
        migrations.AlterModelTable(
            name='coursecell',
            table='coursecell',
        ),
        migrations.AlterModelTable(
            name='coursetype',
            table='coursetype',
        ),
    ]