from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required


from .models import Campus, Categoria, Sugestao, Comentario, Curso, TipoSolicitacao, Perfil, Voto
from django.contrib.auth.models import User, Group
from .forms import UsuarioCadastroForm, VotoForm


# @login_required
# def votacao_list(request):
#     sugestoes = Sugestao.objects.all()

#     if request.method == 'POST':
#         form = VotoForm(request.POST)
#         if form.is_valid():
#             sugestao_id = form.cleaned_data['sugestao_id']
#             escolha = form.cleaned_data['escolha']
#             sugestao = get_object_or_404(Sugestao, id=sugestao_id)

#             voto, created = Voto.objects.get_or_create(
#                 usuario=request.user,
#                 sugestao=sugestao,
#                 defaults={'escolha': escolha}
#             )
#             if not created:
#                 voto.escolha = escolha
#                 voto.save()
#                 messages.success(request, "Seu voto foi atualizado com sucesso!")
#             else:
#                 messages.success(request, "Seu voto foi registrado com sucesso!")
#             return redirect('votacao')

#     else:
#         form = VotoForm()

#     votos = Voto.objects.filter(usuario=request.user)
#     context = {
#         'sugestoes': sugestoes,
#         'form': form,
#         'votos_usuario': votos,
#     }
#     return render(request, 'paginas/votacao.html', context)


# Suas outras views abaixo, sem alterações

class CadastroUsuarioView(CreateView):
    model = User
    form_class = UsuarioCadastroForm
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('login')
    extra_context = {'titulo': 'Registro de usuários', 'botao': 'Registrar'}

    def form_valid(self, form):

        url = super().form_valid(form)
        grupo, criado = Group.objects.get_or_create(name='Visitante')
        self.object.groups.add(grupo)

        try:
            perfil = Perfil.objects.create(
                usuario=self.object
            )
        except Exception as e:
            form.add_error(None, "Erro ao criar perfil: " + str(e))
            self.object.delete()  # Remove o usuário se o perfil não for criado
            return self.form_invalid(form)
            
        return url


class IndexView(TemplateView):
    template_name = "paginas/index.html"


class SobreView(TemplateView):
    template_name = "paginas/sobre.html"


class SugestoesView(TemplateView):
    template_name = "paginas/sugestoes.html"


# CREATE VIEWS
class CampusCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Campus
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-campus')
    extra_context = {'titulo': 'Cadastro de Campus', 'botao': 'Cadastrar'}
    success_message = "Campus criado com sucesso!"


class CategoriaCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Categoria
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-categoria')
    extra_context = {'titulo': 'Cadastro de Categoria', 'botao': 'Cadastrar'}
    success_message = "Categoria criada com sucesso!"


class SugestaoCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Sugestao
    fields = ['titulo', 'descricao', 'campus', 'categoria', 'prioridade', 'anexos']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-sugestao')
    extra_context = {'titulo': 'Cadastro de Sugestão', 'botao': 'Cadastrar'}
    success_message = "Sugestão criada com sucesso!"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ComentarioCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Comentario
    fields = ['texto', 'sugestao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-comentario')
    extra_context = {'titulo': 'Cadastro de Comentário', 'botao': 'Cadastrar'}
    success_message = "Comentário criado com sucesso!"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class CursoCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Curso
    fields = ['nome', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-curso')
    extra_context = {'titulo': 'Cadastro de Curso', 'botao': 'Cadastrar'}
    success_message = "Curso criado com sucesso!"


class TipoSolicitacaoCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TipoSolicitacao
    fields = ['descricao', 'concluido']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-tiposolicitacao')
    extra_context = {'titulo': 'Cadastro de Tipo de Solicitação', 'botao': 'Cadastrar'}
    success_message = "Tipo de Solicitação criado com sucesso!"

    def form_valid(self, form):
        form.instance.solicitado_por = self.request.user
        return super().form_valid(form)


class PerfilCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Perfil
    fields = ['nome', 'telefone', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-perfil')
    extra_context = {'titulo': 'Cadastro de Perfil', 'botao': 'Cadastrar'}
    success_message = "Perfil criado com sucesso!"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class VotoCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Voto
    form_class = VotoForm
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-voto')
    extra_context = {'titulo': 'Votar em Sugestão', 'botao': 'Votar'}
    success_message = "Voto registrado com sucesso!"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


# UPDATE VIEWS
class CampusUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Campus
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-campus')
    extra_context = {'titulo': 'Atualização de Campus', 'botao': 'Salvar'}
    success_message = "Campus atualizado com sucesso!"


class CategoriaUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Categoria
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-categoria')
    extra_context = {'titulo': 'Atualização de Categoria', 'botao': 'Salvar'}
    success_message = "Categoria atualizada com sucesso!"


class SugestaoUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Sugestao
    fields = ['titulo', 'descricao', 'campus', 'categoria', 'prioridade', 'anexos']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-sugestao')
    extra_context = {'titulo': 'Atualização de Sugestão', 'botao': 'Salvar'}
    success_message = "Sugestão atualizada com sucesso!"

    def get_object(self, queryset=None):
        return get_object_or_404(Sugestao, pk=self.kwargs['pk'], usuario=self.request.user) 


class ComentarioUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Comentario
    fields = ['texto', 'sugestao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-comentario')
    extra_context = {'titulo': 'Atualização de Comentário', 'botao': 'Salvar'}
    success_message = "Comentário atualizado com sucesso!"

    def get_object(self, queryset=None):
        return get_object_or_404(Comentario, pk=self.kwargs['pk'], usuario=self.request.user)


class CursoUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Curso
    fields = ['nome', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-curso')
    extra_context = {'titulo': 'Atualização de Curso', 'botao': 'Salvar'}
    success_message = "Curso atualizado com sucesso!"


class TipoSolicitacaoUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TipoSolicitacao
    fields = ['descricao', 'concluido']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-tiposolicitacao')
    extra_context = {'titulo': 'Atualização de Tipo de Solicitação', 'botao': 'Salvar'}
    success_message = "Tipo de Solicitação atualizado com sucesso!"


class PerfilUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Perfil
    fields = ['nome', 'telefone', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-perfil')
    extra_context = {'titulo': 'Atualização de Perfil', 'botao': 'Salvar'}
    success_message = "Perfil atualizado com sucesso!"


class MeuPerfilUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Perfil
    fields = ['nome', 'telefone', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-perfil')
    extra_context = {'titulo': 'Atualização de Perfil', 'botao': 'Salvar'}
    success_message = "Perfil atualizado com sucesso!"

    def get_object(self, queryset=None):
        return get_object_or_404(Perfil, usuario=self.request.user) 


class VotoUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Voto
    form_class = VotoForm
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-voto')
    extra_context = {'titulo': 'Atualização de Voto', 'botao': 'Salvar'}
    success_message = "Voto atualizado com sucesso!"



# LIST VIEWS
class CampusList(LoginRequiredMixin, ListView):
    model = Campus
    template_name = 'paginas/listas/campus.html'


class CategoriaList(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'paginas/listas/categoria.html'


class SugestaoList(LoginRequiredMixin, ListView):
    model = Sugestao
    template_name = 'paginas/listas/sugestao.html'


class ComentarioList(LoginRequiredMixin, ListView):
    model = Comentario
    template_name = 'paginas/listas/comentario.html'


class CursoList(LoginRequiredMixin, ListView):
    model = Curso
    template_name = 'paginas/listas/curso.html'


class TipoSolicitacaoList(LoginRequiredMixin, ListView):
    model = TipoSolicitacao
    template_name = 'paginas/listas/tiposolicitacao.html'

#fazer uma herança para ter tudo que tem na solicitaçãolist
class MinhasSolicitacoes(TipoSolicitacaoList):

    def get_queryset(self):
        qs = TipoSolicitacao.objects.filter(solicitado_por=self.request.user)
        return qs

class PerfilList(LoginRequiredMixin, ListView):
    model = Perfil
    template_name = 'paginas/listas/perfil.html'


class VotoList(LoginRequiredMixin, ListView):
    model = Voto
    template_name = 'paginas/listas/voto.html'


# DELETE VIEWS
class CampusDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Campus
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-campus')
    extra_context = {'titulo': 'Excluir Campus', 'botao': 'Excluir'}
    success_message = "Campus excluído com sucesso!"


class CategoriaDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Categoria
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-categoria')
    extra_context = {'titulo': 'Excluir Categoria', 'botao': 'Excluir'}
    success_message = "Categoria excluída com sucesso!"


class SugestaoDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Sugestao
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-sugestao')
    extra_context = {'titulo': 'Excluir Sugestão', 'botao': 'Excluir'}
    success_message = "Sugestão excluída com sucesso!"

    def get_object(self, queryset=None):
        return get_object_or_404(Sugestao, pk=self.kwargs['pk'], usuario=self.request.user)


class ComentarioDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Comentario
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-comentario')
    extra_context = {'titulo': 'Excluir Comentário', 'botao': 'Excluir'}
    success_message = "Comentário excluído com sucesso!"

    def get_object(self, queryset=None):
        return get_object_or_404(Comentario, pk=self.kwargs['pk'], usuario=self.request.user)


class CursoDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Curso
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-curso')
    extra_context = {'titulo': 'Excluir Curso', 'botao': 'Excluir'}
    success_message = "Curso excluído com sucesso!"


class TipoSolicitacaoDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TipoSolicitacao
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-tiposolicitacao')
    extra_context = {'titulo': 'Excluir Tipo de Solicitação', 'botao': 'Excluir'}
    success_message = "Tipo de Solicitação excluído com sucesso!"


class PerfilDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Perfil
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-perfil')
    extra_context = {'titulo': 'Excluir Perfil', 'botao': 'Excluir'}
    success_message = "Perfil excluído com sucesso!"


class VotoDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Voto
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-voto')
    extra_context = {'titulo': 'Excluir Voto', 'botao': 'Excluir'}
    success_message = "Voto excluído com sucesso!"


# VOTOS: removido a view separada, agora o método está dentro da função votacao_list

# Se precisar da view JSON para votos (opcional)
# from django.http import JsonResponse
# class SugestaoVotosView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         sugestao_id = self.kwargs.get('sugestao_id')
#         sugestao = get_object_or_404(Sugestao, id=sugestao_id)
#         total_votos = sugestao.votos_sim() + sugestao.votos_nao()
#         porcentagem_sim = (sugestao.votos_sim() / total_votos * 100) if total_votos > 0 else 0
#         porcentagem_nao = (sugestao.votos_nao() / total_votos * 100) if total_votos > 0 else 0
#         data = {
#             'total_votos': total_votos,
#             'votos_sim': sugestao.votos_sim(),
#             'votos_nao': sugestao.votos_nao(),
#             'porcentagem_sim': porcentagem_sim,
#             'porcentagem_nao': porcentagem_nao,
#         }
#         return JsonResponse(data)
