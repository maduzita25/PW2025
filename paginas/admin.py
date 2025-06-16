from django.contrib import admin
from .models import Campus, Categoria, Perfil, Sugestao, Comentario, Curso, TipoSolicitacao

# Register your models here.
admin.site.register(Campus)
admin.site.register(Categoria)
admin.site.register(Perfil)
admin.site.register(Sugestao)
admin.site.register(Comentario)
admin.site.register(Curso)
admin.site.register(TipoSolicitacao)