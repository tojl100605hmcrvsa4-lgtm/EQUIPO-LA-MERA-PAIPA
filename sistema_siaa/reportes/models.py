from django.db import models

class Alumno(models.Model):
    matricula = models.CharField(max_length=20, unique=True)
    nombre_completo = models.CharField(max_length=150)
    grupo = models.CharField(max_length=10)
    semestre = models.IntegerField()

    def __str__(self):
        return f"{self.matricula} - {self.nombre_completo}"


class Reporte(models.Model):
    TIPOS_REPORTE = [
        ('INASISTENCIA', 'Inasistencia'),
        ('ACTITUDINAL', 'Actitudinal'),
        ('ACADEMICO', 'Académico'),
    ]

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='reportes')
    tipo = models.CharField(max_length=15, choices=TIPOS_REPORTE)
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    registrado_por = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tipo} - {self.alumno.nombre_completo} ({self.fecha})"
