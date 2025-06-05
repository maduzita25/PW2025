
from django.urls import path
from .views import (
    IndexView, SobreView, SugestoesView,
    CampusCreate, CategoriaCreate, SugestaoCreate, ComentarioCreate, CursoCreate, TipoSolicitacaoCreate, PerfilCreate,
    CampusUpdate, CategoriaUpdate, SugestaoUpdate, ComentarioUpdate, CursoUpdate, TipoSolicitacaoUpdate, PerfilUpdate,
    CursoList, CampusList, CursoDelete
)

urlpatterns = [
    # PÁGINAS ESTÁTICAS
    path("", IndexView.as_view(), name="index"),
    path("sobre/", SobreView.as_view(), name="sobre"),
    path("sugestoes/", SugestoesView.as_view(), name="sugestoes"),

    # ROTAS DE CRIAÇÃO
    path("adicionar/campus/", CampusCreate.as_view(), name="inserir-campus"),
    path("adicionar/categoria/", CategoriaCreate.as_view(), name="inserir-categoria"),
    path("adicionar/sugestao/", SugestaoCreate.as_view(), name="inserir-sugestao"),
    path("adicionar/comentario/", ComentarioCreate.as_view(), name="inserir-comentario"),
    path("adicionar/curso/", CursoCreate.as_view(), name="inserir-curso"),
    path("adicionar/tiposolicitacao/", TipoSolicitacaoCreate.as_view(), name="inserir-tiposolicitacao"),
    path("adicionar/usuario/", PerfilCreate.as_view(), name="inserir-perfil"),

    # ROTAS DE EDIÇÃO
    path("editar/campus/<int:pk>/", CampusUpdate.as_view(), name="editar-campus"),
    path("editar/categoria/<int:pk>/", CategoriaUpdate.as_view(), name="editar-categoria"),
    path("editar/sugestao/<int:pk>/", SugestaoUpdate.as_view(), name="editar-sugestao"),
    path("editar/comentario/<int:pk>/", ComentarioUpdate.as_view(), name="editar-comentario"),
    path("editar/curso/<int:pk>/", CursoUpdate.as_view(), name="editar-curso"),
    path("editar/tiposolicitacao/<int:pk>/", TipoSolicitacaoUpdate.as_view(), name="editar-tiposolicitacao"),
    path("editar/usuario/<int:pk>/", PerfilUpdate.as_view(), name="editar-perfil"),

    # ROTAS DE LISTAGEM
    path("listar/campi/", CampusList.as_view(), name="listar-campus"),
    path("listar/cursos/", CursoList.as_view(), name="listar-curso"),

    # ROTA DE EXCLUSÃO
    path("excluir/curso/<int:pk>/", CursoDelete.as_view(), name="excluir-curso"),
]