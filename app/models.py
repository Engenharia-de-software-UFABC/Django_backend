from django.db import models

class Professor(models.Model):
    nome = models.CharField(primary_key=True, max_length=255)

class Materia(models.Model):
    codigo_turma = models.CharField(primary_key=True, max_length=255)
    turma = models.CharField(max_length=255)
    campus = models.CharField(max_length=255)

class RelacaoMateriaHorarioProfessor(models.Model):
    codigo_turma = models.ForeignKey(Materia, on_delete=models.CASCADE)
    id_professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=255)
    horario = models.CharField(max_length=255)
    sala = models.CharField(max_length=255)
    tipo_recorrencia = models.CharField(max_length=255)

class RelacaoAlunoMateria(models.Model):
    codigo_turma = models.ForeignKey(Materia, on_delete=models.CASCADE)
    ra = models.CharField(max_length=255)
