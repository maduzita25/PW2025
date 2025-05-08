
from django.urls import path
from .views import IndexView, SobreView
from .views import CampusCreate, CategoriaCreate, UsuarioCreate

urlpatterns = [

    path("", IndexView.as_view(), name = "index"),
    path("sobre/", SobreView.as_view(), name = "sobre"),

    path("adicionar/campus/", CampusCreate.as_view(), name="inserir-campus"),
    path("adicionar/categoria/", CategoriaCreate.as_view(), name="inserir-categoria"),
    path("adicionar/usuario/", UsuarioCreate.as_view(), name="inserir-usuario"),

]
