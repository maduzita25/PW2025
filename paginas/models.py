from django.db import models

class Campus(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Sugestao(models.Model):
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


    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    nome = models.CharField(max_length=100)  # Agora é campo de texto
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    categorias = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, blank=True, null=True)
    anexos = models.FileField(upload_to='anexos/', blank=True, null=True)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    texto = models.TextField()
    data_comentario = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(max_length=100)
    sugestao = models.ForeignKey(Sugestao, on_delete=models.CASCADE, related_name='comentarios')

    def __str__(self):
        return f"Comentário por {self.nome} em {self.sugestao.titulo}"


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