from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Campus, Categoria, Sugestao, Comentario, Curso, TipoSolicitacao, Perfil

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
    extra_context = {'titulo': 'Cadastro de Campus', 'botao': 'Cadastrar'}

class CategoriaCreate(CreateView):
    model = Categoria
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Categoria', 'botao': 'Cadastrar'}

class SugestaoCreate(CreateView):
    model = Sugestao
    fields = ['titulo', 'descricao', 'usuario', 'campus', 'categoria', 'prioridade', 'anexos']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Sugestão', 'botao': 'Cadastrar'}

class ComentarioCreate(CreateView):
    model = Comentario
    fields = ['texto', 'usuario', 'sugestao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Comentário', 'botao': 'Cadastrar'}

class CursoCreate(CreateView):
    model = Curso
    fields = ['nome', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Curso', 'botao': 'Cadastrar'}

class TipoSolicitacaoCreate(CreateView):
    model = TipoSolicitacao
    fields = ['descricao', 'concluido']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Tipo de Solicitação', 'botao': 'Cadastrar'}

class PerfilCreate(CreateView):
    model = Perfil
    fields = ['nome', 'telefone', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastro de Perfil', 'botao': 'Cadastrar'}

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
    fields = ['titulo', 'descricao', 'usuario', 'campus', 'categoria', 'prioridade', 'anexos']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Sugestão', 'botao': 'Salvar'}

class ComentarioUpdate(UpdateView):
    model = Comentario
    fields = ['texto', 'usuario', 'sugestao']
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

class PerfilUpdate(UpdateView):
    model = Perfil
    fields = ['nome', 'telefone', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Atualização de Perfil', 'botao': 'Salvar'}

# LIST VIEWS
class CampusList(ListView):
    model = Campus
    template_name = 'paginas/listas/campus.html'
    context_object_name = 'campi'

class CursoList(ListView):
    model = Curso
    template_name = 'paginas/listas/curso.html'
    context_object_name = 'cursos'

# DELETE VIEWS
class CursoDelete(DeleteView):
    model = Curso
    template_name = 'paginas/confirmar_exclusao.html'
    success_url = reverse_lazy('listar-curso')