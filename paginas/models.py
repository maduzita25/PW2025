from django.db import models

# Todas as classes DEVEM ter herança de models.Model
# Create your models here.

class Campus(models.Model):
    nome = models.CharField(max_length=100)
    
    class Categoria(models.Model):
nome = models.CharField(max_length=100)


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    
    
class Sugestao(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='sugestoes')
    campus = models.ForeignKey(
        Campus, on_delete=models.CASCADE, related_name='sugestoes')
    categorias = models.ManyToManyField(Categoria, related_name='sugestoes')
    
    
class Comentario(models.Model):
    texto = models.TextField()
    data_comentario = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='comentarios')
    sugestao = models.ForeignKey(
        Sugestao, on_delete=models.CASCADE, related_name='comentarios')
    
          

class Curso(models.Model):
    nome = models.CharField(max_length=150)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT)

class TipoSolicitacao(models.Model):
    descricao = models.CharField(max_length=250)
    ...
    concluido = models.BooleanField(default=False)
