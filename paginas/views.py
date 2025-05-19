from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Campus, Categoria, Sugestao, Comentario, Curso, TipoSolicitacao

# PÁGINAS ESTÁTICAS
class IndexView(TemplateView):
    template_name = "paginas/index.html"

class SobreView(TemplateView):
    template_name = "paginas/sobre.html"

class SugestoesView(TemplateView):
    template_name = "paginas/sugestoes.html"

# CREATE VIEWS
class CampusCreate(CreateView):
    model = Campus
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Campus'}

class CategoriaCreate(CreateView):
    model = Categoria
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Categoria'}



class SugestaoCreate(CreateView):
    model = Sugestao
    fields = ['titulo', 'descricao', 'nome', 'campus', 'categorias',  'prioridade', 'anexos']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Sugestão'}

class ComentarioCreate(CreateView):
    model = Comentario
    fields = ['texto', 'nome', 'sugestao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Comentário'}

class CursoCreate(CreateView):
    model = Curso
    fields = ['nome', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Curso'}

class TipoSolicitacaoCreate(CreateView):
    model = TipoSolicitacao
    fields = ['descricao', 'concluido']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Tipo de Solicitação'}

# UPDATE VIEWS
class CampusUpdate(UpdateView):
    model = Campus
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Campus', 'botao': 'Salvar'}

class CategoriaUpdate(UpdateView):
    model = Categoria
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Categoria', 'botao': 'Salvar'}


class SugestaoUpdate(UpdateView):
    model = Sugestao
    fields = ['titulo', 'descricao', 'nome', 'campus', 'categorias', 'status', 'prioridade', 'anexos']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Sugestão', 'botao': 'Salvar'}

class ComentarioUpdate(UpdateView):
    model = Comentario
    fields = ['texto', 'nome', 'sugestao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Comentário', 'botao': 'Salvar'}

class CursoUpdate(UpdateView):
    model = Curso
    fields = ['nome', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Curso', 'botao': 'Salvar'}

class TipoSolicitacaoUpdate(UpdateView):
    model = TipoSolicitacao
    fields = ['descricao', 'concluido']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Tipo de Solicitação', 'botao': 'Salvar'}