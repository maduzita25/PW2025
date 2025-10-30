from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q

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
class CampusCreate(GroupRequiredMixin, SuccessMessageMixin, CreateView):
    group_required = ["Administrador"]
    model = Campus
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-campus')
    extra_context = {'titulo': 'Cadastro de Campus', 'botao': 'Cadastrar'}
    success_message = "Campus criado com sucesso!"


class CategoriaCreate(GroupRequiredMixin, SuccessMessageMixin, CreateView):
    group_required = ["Administrador"]
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


class CursoCreate(GroupRequiredMixin, SuccessMessageMixin, CreateView):
    group_required = ["Administrador"]
    model = Curso
    fields = ['nome', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-curso')
    extra_context = {'titulo': 'Cadastro de Curso', 'botao': 'Cadastrar'}
    success_message = "Curso criado com sucesso!"


class TipoSolicitacaoCreate(GroupRequiredMixin, SuccessMessageMixin, CreateView):
    group_required = ["Administrador"]
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

    # Se receber o pk da sugestão na URL, pré-seleciona no formulário
    def get_initial(self):
        initial = super().get_initial()
        sugestao_id = self.kwargs.get('sugestao_id')
        if sugestao_id:
            initial['sugestao'] = get_object_or_404(Sugestao, pk=sugestao_id)
        return initial

    def form_valid(self, form):

        # se o usuario ja votou nesta sugestao apresente uma mensagem de erro
        if Voto.objects.filter(usuario=self.request.user, sugestao=form.instance.sugestao).exists():
            form.add_error(None, "Você já votou nesta sugestão.")
            return self.form_invalid(form)

        form.instance.usuario = self.request.user
        return super().form_valid(form)


# UPDATE VIEWS
class CampusUpdate(GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    group_required = ["Administrador"]
    model = Campus
    fields = ['nome']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-campus')
    extra_context = {'titulo': 'Atualização de Campus', 'botao': 'Salvar'}
    success_message = "Campus atualizado com sucesso!"


class CategoriaUpdate(GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    group_required = ["Administrador"]
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


class CursoUpdate(GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    group_required = ["Administrador"]
    model = Curso
    fields = ['nome', 'campus']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-curso')
    extra_context = {'titulo': 'Atualização de Curso', 'botao': 'Salvar'}
    success_message = "Curso atualizado com sucesso!"


class TipoSolicitacaoUpdate(GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    group_required = ["Administrador"]
    model = TipoSolicitacao
    fields = ['descricao', 'concluido']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-tiposolicitacao')
    extra_context = {'titulo': 'Atualização de Tipo de Solicitação', 'botao': 'Salvar'}
    success_message = "Tipo de Solicitação atualizado com sucesso!"


class PerfilUpdate(GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    group_required = ["Administrador"]
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
    paginate_by = 20


class CategoriaList(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'paginas/listas/categoria.html'
    paginate_by = 20


class SugestaoList(LoginRequiredMixin, ListView):
    model = Sugestao
    template_name = 'paginas/listas/sugestao.html'
    paginate_by = 15
    
    def get_queryset(self):
        return Sugestao.objects.select_related(
            'usuario',
            'campus',
            'categoria'
        ).prefetch_related(
            'votos',
            'comentarios'
        ).order_by('-data_criacao')


class SugestaoDetail(LoginRequiredMixin, DetailView):
    model = Sugestao
    template_name = 'paginas/sugestao_detail.html'
    context_object_name = 'sugestao'

    def get_queryset(self):
        return Sugestao.objects.select_related(
            'usuario',
            'campus',
            'categoria'
        ).prefetch_related('comentarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sugestao = self.get_object()
        
        # Comentários organizados por data (mais recentes primeiro)
        context['comentarios'] = sugestao.comentarios.all()
        
        # Otimizado: Uma única query com agregação para votos
        voto_usuario = sugestao.votos.filter(usuario=self.request.user).first()
        context['usuario_votou'] = voto_usuario is not None
        context['voto_usuario'] = voto_usuario
        
        # Agregação de votos em uma única query
        votos_agg = sugestao.votos.aggregate(
            total=Count('id'),
            sim=Count('id', filter=Q(escolha=True)),
            nao=Count('id', filter=Q(escolha=False))
        )
        context['total_votos'] = votos_agg['total']
        context['votos_sim'] = votos_agg['sim']
        context['votos_nao'] = votos_agg['nao']
        
        # Calcular porcentagem
        if context['total_votos'] > 0:
            context['porcentagem_sim'] = (context['votos_sim'] / context['total_votos']) * 100
            context['porcentagem_nao'] = (context['votos_nao'] / context['total_votos']) * 100
        else:
            context['porcentagem_sim'] = 0
            context['porcentagem_nao'] = 0
        
        # Verificar se é o autor
        context['eh_autor'] = sugestao.usuario == self.request.user
        
        return context



class ComentarioList(LoginRequiredMixin, ListView):
    model = Comentario
    template_name = 'paginas/listas/comentario.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Comentario.objects.select_related(
            'usuario',
            'sugestao'
        ).order_by('-data_comentario')


class CursoList(LoginRequiredMixin, ListView):
    model = Curso
    template_name = 'paginas/listas/curso.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Curso.objects.select_related('campus').order_by('nome')


class TipoSolicitacaoList(LoginRequiredMixin, ListView):
    model = TipoSolicitacao
    template_name = 'paginas/listas/tiposolicitacao.html'
    paginate_by = 20

#fazer uma herança para ter tudo que tem na solicitaçãolist
class MinhasSolicitacoes(TipoSolicitacaoList):
    paginate_by = 20

    def get_queryset(self):
        qs = TipoSolicitacao.objects.filter(solicitado_por=self.request.user).order_by('-id')
        return qs

class PerfilList(LoginRequiredMixin, ListView):
    model = Perfil
    template_name = 'paginas/listas/perfil.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Perfil.objects.select_related(
            'usuario',
            'campus'
        ).order_by('nome')


class VotoList(LoginRequiredMixin, ListView):
    model = Voto
    template_name = 'paginas/listas/voto.html'
    paginate_by = 20
    context_object_name = 'votos'

    def get_queryset(self):
        # Otimizar com select_related para evitar N+1 queries
        return Voto.objects.select_related(
            'usuario',
            'sugestao',
            'sugestao__usuario',
            'sugestao__campus',
            'sugestao__categoria'
        ).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Verificar se é administrador (cacheado no usuário)
        context['eh_admin'] = self.request.user.groups.filter(name='Administrador').exists()
        
        # Otimizado: Uma única query de agregação ao invés de 3 queries separadas
        votos_stats = Voto.objects.aggregate(
            total=Count('id'),
            concordam=Count('id', filter=Q(escolha=True)),
            discordam=Count('id', filter=Q(escolha=False))
        )
        context['total_votos'] = votos_stats['total']
        context['votos_concordam'] = votos_stats['concordam']
        context['votos_discordam'] = votos_stats['discordam']
        
        return context


# DELETE VIEWS
class CampusDelete(GroupRequiredMixin, SuccessMessageMixin, DeleteView):
    group_required = ["Administrador"]
    model = Campus
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-campus')
    extra_context = {'titulo': 'Excluir Campus', 'botao': 'Excluir'}
    success_message = "Campus excluído com sucesso!"


class CategoriaDelete(GroupRequiredMixin, SuccessMessageMixin, DeleteView):
    group_required = ["Administrador"]
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


class CursoDelete(GroupRequiredMixin, SuccessMessageMixin, DeleteView):
    group_required = ["Administrador"]
    model = Curso
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-curso')
    extra_context = {'titulo': 'Excluir Curso', 'botao': 'Excluir'}
    success_message = "Curso excluído com sucesso!"


class TipoSolicitacaoDelete(GroupRequiredMixin, SuccessMessageMixin, DeleteView):
    group_required = ["Administrador"]
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
