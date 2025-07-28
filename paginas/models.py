from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = [
    ('aberta', 'Aberta'),
    ('analise', 'Em análise'),
    ('andamento', 'Em andamento'),
    ('concluida', 'Concluída'),
    ('rejeitada', 'Rejeitada'),
]

PRIORIDADE_CHOICES = [
    ('baixa', 'Baixa'),
    ('media', 'Média'),
    ('alta', 'Alta'),
]



class Campus(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Perfil(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, blank=True)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT)

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')

    def __str__(self):
        return self.nome


class Sugestao(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, blank=True, null=True)
    anexos = models.FileField(upload_to='anexos/', blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    texto = models.TextField()
    data_comentario = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    sugestao = models.ForeignKey(Sugestao, on_delete=models.CASCADE, related_name='comentarios')

    def __str__(self):
        return f"Comentário por {self.usuario.username} em {self.sugestao.titulo}"


class Curso(models.Model):
    nome = models.CharField(max_length=150)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome


class TipoSolicitacao(models.Model):
    descricao = models.CharField(max_length=250)
    concluido = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao
