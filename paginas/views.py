from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Campus, Categoria, Usuario

from django.urls import reverse_lazy

class IndexView(TemplateView):
    template_name = "paginas/index.html"

class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'

class CampusCreate(CreateView):
    template_name = 'paginas/form.html'
    model = Campus
    fields = ['nome']
    success_url = reverse_lazy('index')
    extra_context = {'titulo' : 'Cadastro de Campus'}

class CategoriaCreate(CreateView):
    template_name = 'paginas/form.html'
    model = Categoria
    fields = ['nome']
    success_url = reverse_lazy('index')
    extra_context = {'título' : 'Cadastro De Categoria'}

class UsuarioCreate(CreateView):
    template_name = 'paginas/form.html'
    model = Usuario
    fields = ['nome', 'email', 'senha']
    success_url = reverse_lazy('index')
    extra_context = {'título' : 'Cadastro de Usuário'}


