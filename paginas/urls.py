
from django.urls import path
from .views import (
    IndexView, SobreView, SugestoesView,
    CampusCreate, CategoriaCreate, SugestaoCreate, ComentarioCreate, CursoCreate, TipoSolicitacaoCreate, PerfilCreate,
    CampusUpdate, CategoriaUpdate, SugestaoUpdate, ComentarioUpdate, CursoUpdate, TipoSolicitacaoUpdate, PerfilUpdate,
    CampusList, CategoriaList, SugestaoList, ComentarioList, CursoList, TipoSolicitacaoList, PerfilList,
    CampusDelete, CategoriaDelete, SugestaoDelete, ComentarioDelete, CursoDelete, TipoSolicitacaoDelete, PerfilDelete,
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
    path("listar/categoria/", CategoriaList.as_view(), name="listar-categoria"),
    path("listar/sugestao/", SugestaoList.as_view(), name="listar-sugestao"),
    path("listar/comentario/", ComentarioList.as_view(), name="listar-comentario"),
    path("listar/curso/", CursoList.as_view(), name="listar-curso"),
    path("listar/tiposolicitacao/", TipoSolicitacaoList.as_view(), name="listar-tiposolicitacao"),
    path("listar/perfil/", PerfilList.as_view(), name="listar-perfil"),



    # ROTA DE EXCLUSÃO
    path("excluir/campus/<int:pk>/", CampusDelete.as_view(), name="excluir-campus"),
    path("excluir/categoria/<int:pk>/", CategoriaDelete.as_view(), name="excluir-categoria"),
    path("excluir/sugestao/<int:pk>/", SugestaoDelete.as_view(), name="excluir-sugestao"),
    path("excluir/comentario/<int:pk>/", ComentarioDelete.as_view(), name="excluir-comentario"),
    path("excluir/curso/<int:pk>/", CursoDelete.as_view(), name="excluir-curso"),
    path("excluir/tiposolicitacao/<int:pk>/", TipoSolicitacaoDelete.as_view(), name="excluir-tiposolicitacao"),
    path("excluir/perfil/<int:pk>/", PerfilDelete.as_view(), name="excluir-perfil"),
]
