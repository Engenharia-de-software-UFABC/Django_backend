from django.db import models
from django.core.exceptions import ValidationError


# class Professor(models.Model):
# 	nome = models.CharField(primary_key=True, max_length=255)

# class Disciplina(models.Model):
#      codigo = models.CharField(primary_key=True, max_length=255)
# class Turma(models.Model):
#     codigo = models.CharField(primary_key=True, max_length=255)
#     campus = models.CharField(max_length=255)
#     horarios_salas = models.CharField(max_length=255)
#     professor = models.ForeignKey(Professor)
#     is_teoria = models.BooleanField(default=True)

# class AlunoTurma(models.Model):
#     aluno = models.IntergerField()
#     turma = models.ForeignKey(Turma)
#     class Meta:
#         unique_together = ('aluno', 'turma')

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
    tipo_semanal = models.CharField(max_length=255)

class RelacaoAlunoMateria(models.Model):
    codigo_turma = models.ForeignKey(Materia, on_delete=models.CASCADE)
    ra = models.CharField(max_length=255)
