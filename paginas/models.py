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
    cadastrado_em = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']


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
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, blank=True, null=True)
    anexos = models.FileField(upload_to='anexos/', blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def votos_sim(self):
        return self.votos.filter(escolha=True).count()

    def votos_nao(self):
        return self.votos.filter(escolha=False).count()

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-data_criacao']


class Voto(models.Model):
    sugestao = models.ForeignKey(Sugestao, on_delete=models.CASCADE, related_name='votos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    escolha = models.BooleanField()  # True = Sim, False = Não

    class Meta:
        unique_together = ('sugestao', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} votou {'Sim' if self.escolha else 'Não'} em {self.sugestao.titulo}"


class Comentario(models.Model):
    texto = models.TextField()
    data_comentario = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    sugestao = models.ForeignKey(Sugestao, on_delete=models.CASCADE, related_name='comentarios')

    def __str__(self):
        return f"Comentário por {self.usuario.username} em {self.sugestao.titulo}"

    class Meta:
        ordering = ['-data_comentario']


class Curso(models.Model):
    nome = models.CharField(max_length=150)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']


class TipoSolicitacao(models.Model):
    descricao = models.CharField(max_length=250)
    concluido = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ['descricao']