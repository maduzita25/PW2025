from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Campus, Categoria, Usuario, Sugestao, Comentario, Curso, TipoSolicitacao

# Páginas estáticas
class IndexView(TemplateView):
    template_name = "paginas/index.html"

class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'

# CREATE VIEWS
class CampusCreate(CreateView):
    template_name = 'paginas/form.html'
    model = Campus
    fields = ['nome']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Campus'}

class CategoriaCreate(CreateView):
    template_name = 'paginas/form.html'
    model = Categoria
    fields = ['nome']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Categoria'}

class UsuarioCreate(CreateView):
    template_name = 'paginas/form.html'
    model = Usuario
    fields = ['nome', 'email', 'senha']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Usuário'}

class SugestaoCreate(CreateView):
    template_name = 'paginas/form.html'
    model = Sugestao
    fields = ['titulo', 'descricao', 'data_criacao', 'usuario', 'campus', 'categorias']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Sugestão'}

class ComentarioCreate(CreateView):
    template_name = 'paginas/form.html'
    model = Comentario
    fields = ['texto', 'data_comentario', 'usuario', 'sugestao']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Comentário'}

class CursoCreate(CreateView):
    template_name = 'paginas/form.html'
    model = Curso
    fields = ['nome', 'campus']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Curso'}

class TipoSolicitacaoCreate(CreateView):
    template_name = 'paginas/form.html'
    model = TipoSolicitacao
    fields = ['descricao', 'concluido']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Tipo de Solicitação'}

# UPDATE VIEWS
class CampusUpdate(UpdateView):
    template_name = 'paginas/form.html'
    model = Campus
    fields = ['nome']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Campus', 'botao': 'Salvar'}

class CategoriaUpdate(UpdateView):
    template_name = 'paginas/form.html'
    model = Categoria
    fields = ['nome']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Categoria', 'botao': 'Salvar'}

class UsuarioUpdate(UpdateView):
    template_name = 'paginas/form.html'
    model = Usuario
    fields = ['nome', 'email', 'senha']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Usuário', 'botao': 'Salvar'}

class SugestaoUpdate(UpdateView):
    template_name = 'paginas/form.html'
    model = Sugestao
    fields = ['titulo', 'descricao', 'data_criacao', 'usuario', 'campus', 'categorias']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Sugestão', 'botao': 'Salvar'}

class ComentarioUpdate(UpdateView):
    template_name = 'paginas/form.html'
    model = Comentario
    fields = ['texto', 'data_comentario', 'usuario', 'sugestao']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Comentário', 'botao': 'Salvar'}

class CursoUpdate(UpdateView):
    template_name = 'paginas/form.html'
    model = Curso
    fields = ['nome', 'campus']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Curso', 'botao': 'Salvar'}

class TipoSolicitacaoUpdate(UpdateView):
    template_name = 'paginas/form.html'
    model = TipoSolicitacao
    fields = ['descricao', 'concluido']
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Tipo de Solicitação', 'botao': 'Salvar'}
