from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Campus, Categoria, Sugestao, Comentario, Curso, TipoSolicitacao, Perfil

from django.contrib.auth.mixins import LoginRequiredMixin

# PÁGINAS ESTÁTICAS
class IndexView(TemplateView):
    template_name = "paginas/index.html"

class SobreView(TemplateView):
    template_name = "paginas/sobre.html"

class SugestoesView(TemplateView):
    template_name = "paginas/sugestoes.html"

# CREATE VIEWS
class CampusCreate(LoginRequiredMixin, CreateView):
    model = Campus
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-campus')
    extra_context = {'titulo': 'Cadastro de Campus', 'botao': 'Cadastrar'}

class CategoriaCreate(LoginRequiredMixin, CreateView):
    model = Categoria
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-categoria')
    extra_context = {'titulo': 'Cadastro de Categoria', 'botao': 'Cadastrar'}

class SugestaoCreate(LoginRequiredMixin, CreateView):
    model = Sugestao
    fields = ['titulo', 'descricao', 'usuario', 'campus', 'categoria', 'prioridade', 'anexos']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-sugestao')
    extra_context = {'titulo': 'Cadastro de Sugestão', 'botao': 'Cadastrar'}

class ComentarioCreate(LoginRequiredMixin, CreateView):
    model = Comentario
    fields = ['texto', 'usuario', 'sugestao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-comentario')
    extra_context = {'titulo': 'Cadastro de Comentário', 'botao': 'Cadastrar'}

class CursoCreate(LoginRequiredMixin, CreateView):
    model = Curso
    fields = ['nome', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-curso')
    extra_context = {'titulo': 'Cadastro de Curso', 'botao': 'Cadastrar'}

class TipoSolicitacaoCreate(LoginRequiredMixin, CreateView):
    model = TipoSolicitacao
    fields = ['descricao', 'concluido']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-tiposolicitacao')
    extra_context = {'titulo': 'Cadastro de Tipo de Solicitação', 'botao': 'Cadastrar'}

class PerfilCreate(LoginRequiredMixin, CreateView):
    model = Perfil
    fields = ['nome', 'telefone', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-perfil')
    extra_context = {'titulo': 'Cadastro de Perfil', 'botao': 'Cadastrar'}

# UPDATE VIEWS
class CampusUpdate(UpdateView):
    model = Campus
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-campus')
    extra_context = {'titulo': 'Atualização de Campus', 'botao': 'Salvar'}

class CategoriaUpdate(UpdateView):
    model = Categoria
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-categoria')
    extra_context = {'titulo': 'Atualização de Categoria', 'botao': 'Salvar'}

class SugestaoUpdate(UpdateView):
    model = Sugestao
    fields = ['titulo', 'descricao', 'usuario', 'campus', 'categoria', 'prioridade', 'anexos']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-sugestao')
    extra_context = {'titulo': 'Atualização de Sugestão', 'botao': 'Salvar'}

class ComentarioUpdate(UpdateView):
    model = Comentario
    fields = ['texto', 'usuario', 'sugestao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-comentario')
    extra_context = {'titulo': 'Atualização de Comentário', 'botao': 'Salvar'}

class CursoUpdate(UpdateView):
    model = Curso
    fields = ['nome', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-curso')
    extra_context = {'titulo': 'Atualização de Curso', 'botao': 'Salvar'}

class TipoSolicitacaoUpdate(UpdateView):
    model = TipoSolicitacao
    fields = ['descricao', 'concluido']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-tiposolicitacao')
    extra_context = {'titulo': 'Atualização de Tipo de Solicitação', 'botao': 'Salvar'}

class PerfilUpdate(UpdateView):
    model = Perfil
    fields = ['nome', 'telefone', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-perfil')
    extra_context = {'titulo': 'Atualização de Perfil', 'botao': 'Salvar'}


# LIST VIEWS

class CampusList(ListView):
    model = Campus
    template_name = 'paginas/listas/campus.html'

class CategoriaList(ListView):
    model = Categoria
    template_name = 'paginas/listas/categoria.html'

class SugestaoList(ListView):
    model = Sugestao
    template_name = 'paginas/listas/sugestao.html'

class ComentarioList(ListView):
    model = Comentario
    template_name = 'paginas/listas/comentario.html'

class CursoList(ListView):
    model = Curso
    template_name = 'paginas/listas/curso.html'

class TipoSolicitacaoList(ListView):
    model = TipoSolicitacao
    template_name = 'paginas/listas/tiposolicitacao.html'

class PerfilList(ListView):
    model = Perfil
    template_name = 'paginas/listas/perfil.html'


# DELETE VIEWS: Campus, Categoria, Sugestao, Comentario, Curso, TipoSolicitacao, Perfil

class CampusDelete(DeleteView):
    model = Campus
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-campus')
    extra_context = {'titulo': 'Excluir Campus', 'botao': 'Excluir'}

class CategoriaDelete(DeleteView):
    model = Categoria
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-categoria')
    extra_context = {'titulo': 'Excluir Categoria', 'botao': 'Excluir'}

class SugestaoDelete(DeleteView):
    model = Sugestao
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-sugestao')
    extra_context = {'titulo': 'Excluir Sugestao', 'botao': 'Excluir'}

class ComentarioDelete(DeleteView):
    model = Comentario
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-comentario')
    extra_context = {'titulo': 'Excluir Comenatrio', 'botao': 'Excluir'}

class CursoDelete(DeleteView):
    model = Curso
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-curso')
    extra_context = {'titulo': 'Excluir Curso', 'botao': 'Excluir'}

class TipoSolicitacaoDelete(DeleteView):
    model = TipoSolicitacao
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-tiposolicitacao')
    extra_context = {'titulo': 'Excluir Tipo Solicitacao', 'botao': 'Excluir'}

class PerfilDelete(DeleteView):
    model = Perfil
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-perfil')
    extra_context = {'titulo': 'Excluir Perfil', 'botao': 'Excluir'}


