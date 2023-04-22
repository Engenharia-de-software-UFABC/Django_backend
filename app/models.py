from django.db import models

class Aluno(models.Model):
	ra = models.IntegerField(primary_key=True)
	nome = models.CharField(max_length=255)
	
class Professor(models.Model):
	id = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=255)
	
class Disciplina(models.Model):
	codigo = models.CharField(primary_key=True)
	nome = models.CharField(max_length=255)
	
class Turma(models.Model):
	id = models.AutoField(primary_key=True)
	disciplina = models.Foreingkey(Disciplina)
	professor = models.Foreingkey(Professor)
	quadrimestre = models.IntegerFields()
	ano = models.IntegerFields()
