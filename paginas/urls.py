
from django.urls import path
from .views import IndexView, SobreView
from .views import CampusCreate, CategoriaCreate, UsuarioCreate, SugestaoCreate, ComentarioCreate, CursoCreate, TipoSolicitacaoCreate

from .views import CampusUpdate, CategoriaUpdate, UsuarioUpdate, SugestaoUpdate, ComentarioUpdate, CursoUpdate, TipoSolicitacaoUpdate
urlpatterns = [

    path("", IndexView.as_view(), name = "index"),
    path("sobre/", SobreView.as_view(), name = "sobre"),

    path("adicionar/campus/", CampusCreate.as_view(), name="inserir-campus"),
    path("adicionar/categoria/", CategoriaCreate.as_view(), name="inserir-categoria"),
    path("adicionar/usuario/", UsuarioCreate.as_view(), name="inserir-usuario"),
    path("adicionar/sugestao/", SugestaoCreate.as_view(), name="inserir-sugestao"),
    path("adicionar/comentario/", ComentarioCreate.as_view(), name="inserir-comentario"),
    path("adicionar/curso/", CursoCreate.as_view(), name="inserir-curso"),
    path("adicionar/tiposolicitacao/", TipoSolicitacaoCreate.as_view(), name="inserir-tiposolicitacao"),


    path("editar/campus/<int:pk>/", CampusUpdate.as_view(), name="editar-campus"),
    path("editar/categoria/<int:pk>/", CategoriaUpdate.as_view(), name="editar-categoria"),
    path("editar/usuario/<int:pk>/", UsuarioUpdate.as_view(), name="editar-usuario"),
    path("editar/sugestao/<int:pk>/", SugestaoUpdate.as_view(), name="editar-sugestao"),
    path("editar/comentario/<int:pk>/", ComentarioUpdate.as_view(), name="editar-comentario"),
    path("editar/curso/<int:pk>/", CursoUpdate.as_view(), name="editar-curso"),
    path("editar/tiposolicitacao/<int:pk>/", TipoSolicitacaoUpdate.as_view(), name="editar-tiposolicitacao"),
]
