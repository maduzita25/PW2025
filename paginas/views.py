from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Sum, Avg, F
from django.db.models.functions import TruncDate

from .models import Campus, Categoria, Sugestao, Comentario, Curso, TipoSolicitacao, Perfil, Voto
from django.contrib.auth.models import User, Group
from .forms import UsuarioCadastroForm, VotoForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_sugestoes'] = Sugestao.objects.count()
        context['total_votos'] = Voto.objects.count()
        context['total_comentarios'] = Comentario.objects.count()
        context['total_usuarios'] = User.objects.filter(is_active=True).count()
        return context


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


# Endpoint AJAX para registrar voto sem recarregar a página
@login_required
@require_POST
def vote_ajax(request):
    """Recebe POST (sugestao, escolha) e retorna JSON com os novos totais."""
    user = request.user
    sugestao_id = request.POST.get('sugestao')
    escolha = request.POST.get('escolha')

    if not sugestao_id or escolha is None:
        return JsonResponse({'success': False, 'error': 'Parâmetros faltando.'}, status=400)

    try:
        sugestao = get_object_or_404(Sugestao, pk=int(sugestao_id))
    except Exception:
        return JsonResponse({'success': False, 'error': 'Sugestão não encontrada.'}, status=404)

    # Já votou?
    if Voto.objects.filter(usuario=user, sugestao=sugestao).exists():
        return JsonResponse({'success': False, 'error': 'Você já votou nesta sugestão.'}, status=400)

    escolha_bool = str(escolha).lower() in ['true', '1', 'yes']

    voto = Voto.objects.create(usuario=user, sugestao=sugestao, escolha=escolha_bool)

    votos_agg = sugestao.votos.aggregate(
        total=Count('id'),
        sim=Count('id', filter=Q(escolha=True)),
        nao=Count('id', filter=Q(escolha=False))
    )

    total = votos_agg.get('total') or 0
    sim = votos_agg.get('sim') or 0
    nao = votos_agg.get('nao') or 0

    porcentagem_sim = (sim / total) * 100 if total > 0 else 0
    porcentagem_nao = (nao / total) * 100 if total > 0 else 0

    return JsonResponse({
        'success': True,
        'message': 'Voto registrado com sucesso!',
        'total_votos': total,
        'votos_sim': sim,
        'votos_nao': nao,
        'porcentagem_sim': round(porcentagem_sim, 1),
        'porcentagem_nao': round(porcentagem_nao, 1),
        'escolha_usuario': escolha_bool,
    })


# Endpoint AJAX para alterar voto (mudar escolha)
@login_required
@require_POST
def change_vote_ajax(request):
    user = request.user
    sugestao_id = request.POST.get('sugestao')
    escolha = request.POST.get('escolha')

    if not sugestao_id or escolha is None:
        return JsonResponse({'success': False, 'error': 'Parâmetros faltando.'}, status=400)

    try:
        sugestao = get_object_or_404(Sugestao, pk=int(sugestao_id))
    except Exception:
        return JsonResponse({'success': False, 'error': 'Sugestão não encontrada.'}, status=404)

    voto = Voto.objects.filter(usuario=user, sugestao=sugestao).first()
    if not voto:
        return JsonResponse({'success': False, 'error': 'Voto não encontrado para alteração.'}, status=404)

    escolha_bool = str(escolha).lower() in ['true', '1', 'yes']
    voto.escolha = escolha_bool
    voto.save()

    votos_agg = sugestao.votos.aggregate(
        total=Count('id'),
        sim=Count('id', filter=Q(escolha=True)),
        nao=Count('id', filter=Q(escolha=False))
    )

    total = votos_agg.get('total') or 0
    sim = votos_agg.get('sim') or 0
    nao = votos_agg.get('nao') or 0

    porcentagem_sim = (sim / total) * 100 if total > 0 else 0
    porcentagem_nao = (nao / total) * 100 if total > 0 else 0

    return JsonResponse({
        'success': True,
        'message': 'Voto atualizado com sucesso!',
        'total_votos': total,
        'votos_sim': sim,
        'votos_nao': nao,
        'porcentagem_sim': round(porcentagem_sim, 1),
        'porcentagem_nao': round(porcentagem_nao, 1),
        'escolha_usuario': escolha_bool,
    })


# Endpoint AJAX para criar comentário sem reload
@login_required
@require_POST
def comment_ajax(request):
    user = request.user
    sugestao_id = request.POST.get('sugestao')
    texto = request.POST.get('texto')

    if not sugestao_id or not texto:
        return JsonResponse({'success': False, 'error': 'Parâmetros faltando.'}, status=400)

    try:
        sugestao = get_object_or_404(Sugestao, pk=int(sugestao_id))
    except Exception:
        return JsonResponse({'success': False, 'error': 'Sugestão não encontrada.'}, status=404)

    comentario = Comentario.objects.create(
        usuario=user,
        sugestao=sugestao,
        texto=texto
    )

    # montar resposta com dados do comentário criado
    data_str = comentario.data_comentario.strftime('%d/%m/%Y %H:%M') if hasattr(comentario, 'data_comentario') else timezone.now().strftime('%d/%m/%Y %H:%M')
    novo_count = sugestao.comentarios.count()

    return JsonResponse({
        'success': True,
        'comentario': {
            'id': comentario.pk,
            'usuario': user.username,
            'texto': comentario.texto,
            'data': data_str
        },
        'novo_count': novo_count
    })


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


# RELATÓRIO DE VOTAÇÃO
class RelatorioVotacaoView(LoginRequiredMixin, TemplateView):
    """
    View para exibir relatório completo de votações com gráficos.
    """
    template_name = 'paginas/relatorio_votacao.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # ==================== DADOS GERAIS ====================
        total_sugestoes = Sugestao.objects.count()
        total_votos = Voto.objects.count()
        total_comentarios = Comentario.objects.count()
        total_usuarios = User.objects.filter(groups__name='Visitante').count()
        
        # Votos por escolha
        votos_sim = Voto.objects.filter(escolha=True).count()
        votos_nao = Voto.objects.filter(escolha=False).count()
        
        # Calcular porcentagens
        if total_votos > 0:
            pct_sim = (votos_sim / total_votos) * 100
            pct_nao = (votos_nao / total_votos) * 100
        else:
            pct_sim = pct_nao = 0.0
        
        context['total_sugestoes'] = total_sugestoes
        context['total_votos'] = total_votos
        context['total_comentarios'] = total_comentarios
        context['total_usuarios'] = total_usuarios
        context['votos_sim'] = votos_sim
        context['votos_nao'] = votos_nao
        context['pct_sim'] = round(pct_sim, 2)
        context['pct_nao'] = round(pct_nao, 2)
        
        # ==================== VOTOS POR CAMPUS ====================
        votos_por_campus = Voto.objects.select_related('sugestao__campus').values(
            'sugestao__campus__nome'
        ).annotate(
            total=Count('id'),
            concordam=Count('id', filter=Q(escolha=True)),
            discordam=Count('id', filter=Q(escolha=False))
        ).order_by('sugestao__campus__nome')
        
        campus_labels = [item['sugestao__campus__nome'] for item in votos_por_campus]
        campus_concordam = [item['concordam'] for item in votos_por_campus]
        campus_discordam = [item['discordam'] for item in votos_por_campus]
        
        context['campus_labels'] = str(campus_labels)
        context['campus_concordam'] = str(campus_concordam)
        context['campus_discordam'] = str(campus_discordam)
        
        # ==================== VOTOS POR CATEGORIA ====================
        votos_por_categoria = Voto.objects.select_related('sugestao__categoria').values(
            'sugestao__categoria__nome'
        ).annotate(
            total=Count('id'),
            concordam=Count('id', filter=Q(escolha=True)),
            discordam=Count('id', filter=Q(escolha=False))
        ).order_by('sugestao__categoria__nome')
        
        categoria_labels = [item['sugestao__categoria__nome'] for item in votos_por_categoria]
        categoria_concordam = [item['concordam'] for item in votos_por_categoria]
        categoria_discordam = [item['discordam'] for item in votos_por_categoria]
        
        context['categoria_labels'] = str(categoria_labels)
        context['categoria_concordam'] = str(categoria_concordam)
        context['categoria_discordam'] = str(categoria_discordam)
        
        # ==================== SUGESTÕES POR STATUS ====================
        sugestoes_por_status = Sugestao.objects.values('status').annotate(
            total=Count('id')
        ).order_by('status')
        
        # Se não houver dados, criar array vazio
        if sugestoes_por_status.exists():
            status_labels = [item['status'].upper() for item in sugestoes_por_status]
            status_valores = [item['total'] for item in sugestoes_por_status]
        else:
            status_labels = []
            status_valores = []
        
        context['status_labels'] = str(status_labels) if status_labels else "[]"
        context['status_valores'] = str(status_valores) if status_valores else "[]"
        
        # ==================== SUGESTÕES POR PRIORIDADE ====================
        sugestoes_por_prioridade = Sugestao.objects.values('prioridade').exclude(
            prioridade__isnull=True
        ).annotate(
            total=Count('id')
        ).order_by('prioridade')
        
        prioridade_labels = [item['prioridade'].upper() for item in sugestoes_por_prioridade]
        prioridade_valores = [item['total'] for item in sugestoes_por_prioridade]
        
        context['prioridade_labels'] = str(prioridade_labels)
        context['prioridade_valores'] = str(prioridade_valores)
        
        # ==================== TOP 5 SUGESTÕES MAIS VOTADAS ====================
        top_sugestoes = Sugestao.objects.annotate(
            total_votos=Count('votos')
        ).order_by('-total_votos')[:5]
        
        top_sugestoes_data = []
        for sug in top_sugestoes:
            votos_agg = sug.votos.aggregate(
                sim=Count('id', filter=Q(escolha=True)),
                nao=Count('id', filter=Q(escolha=False))
            )
            top_sugestoes_data.append({
                'titulo': sug.titulo[:30] + '...' if len(sug.titulo) > 30 else sug.titulo,
                'total': sug.total_votos,
                'sim': votos_agg['sim'],
                'nao': votos_agg['nao']
            })
        
        # Se não houver dados, criar arrays vazios
        if top_sugestoes_data:
            top_titles = [item['titulo'] for item in top_sugestoes_data]
            top_votos = [item['total'] for item in top_sugestoes_data]
        else:
            top_titles = []
            top_votos = []
        
        context['top_titles'] = str(top_titles) if top_titles else "[]"
        context['top_votos'] = str(top_votos) if top_votos else "[]"
        
        # ==================== TAXA DE PARTICIPAÇÃO POR CAMPUS ====================
        participacao_campus = Campus.objects.annotate(
            total_sugestoes=Count('sugestao'),
            total_votos=Count('sugestao__votos')
        ).order_by('-total_votos')
        
        part_campus_labels = [c.nome for c in participacao_campus]
        part_campus_sugestoes = [c.total_sugestoes for c in participacao_campus]
        part_campus_votos = [c.total_votos for c in participacao_campus]
        
        context['part_campus_labels'] = str(part_campus_labels)
        context['part_campus_sugestoes'] = str(part_campus_sugestoes)
        context['part_campus_votos'] = str(part_campus_votos)
        
        # ==================== MÉDIA DE VOTOS POR SUGESTÃO ====================
        media_votos = Sugestao.objects.annotate(
            total_votos=Count('votos')
        ).aggregate(media=Avg('total_votos'))
        context['media_votos'] = round(media_votos['media'] or 0, 2)
        
        # ==================== ENGAJAMENTO: COMENTÁRIOS POR SUGESTÃO ====================
        media_comentarios = Sugestao.objects.annotate(
            total_comentarios=Count('comentarios')
        ).aggregate(media=Avg('total_comentarios'))
        context['media_comentarios'] = round(media_comentarios['media'] or 0, 2)
        
        # ==================== SUGESTÕES POR CAMPUS (Pizza) ====================
        sugestoes_campus = Campus.objects.annotate(
            total=Count('sugestao')
        ).order_by('-total')
        
        campus_pizza_labels = [c.nome for c in sugestoes_campus]
        campus_pizza_valores = [c.total for c in sugestoes_campus]
        
        context['campus_pizza_labels'] = str(campus_pizza_labels)
        context['campus_pizza_valores'] = str(campus_pizza_valores)
        
        # ==================== CATEGORIAS MAIS VOTADAS ====================
        categorias_votadas = Categoria.objects.annotate(
            total_votos=Count('sugestao__votos')
        ).order_by('-total_votos')[:5]
        
        # Se não houver dados, criar arrays vazios
        if categorias_votadas.exists():
            cat_labels = [c.nome for c in categorias_votadas]
            cat_votos = [c.total_votos for c in categorias_votadas]
        else:
            cat_labels = []
            cat_votos = []
        
        context['cat_labels'] = str(cat_labels) if cat_labels else "[]"
        context['cat_votos'] = str(cat_votos) if cat_votos else "[]"
        
        # ==================== ÍNDICE DE CONCORDÂNCIA POR CATEGORIA ====================
        indice_categoria = Voto.objects.select_related('sugestao__categoria').values(
            'sugestao__categoria__nome'
        ).annotate(
            total=Count('id'),
            concordam=Count('id', filter=Q(escolha=True))
        ).order_by('sugestao__categoria__nome')
        
        indice_cat_labels = [item['sugestao__categoria__nome'] for item in indice_categoria]
        indice_cat_valores = []
        for item in indice_categoria:
            if item['total'] > 0:
                indice = (item['concordam'] / item['total']) * 100
                indice_cat_valores.append(round(indice, 2))
            else:
                indice_cat_valores.append(0.0)
        
        context['indice_cat_labels'] = str(indice_cat_labels)
        context['indice_cat_valores'] = str(indice_cat_valores)
        
        return context
