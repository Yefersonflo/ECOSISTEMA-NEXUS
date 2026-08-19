from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("afiliados", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="carpeta",
            name="estado",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="carpeta",
            name="fecha",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="carpeta",
            name="fecha_retiro",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="carpeta",
            name="tipo_identificacion",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
