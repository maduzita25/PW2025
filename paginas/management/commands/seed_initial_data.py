from django.core.management.base import BaseCommand

from paginas.models import Campus, Categoria, Curso, TipoSolicitacao


class Command(BaseCommand):
    help = 'Cria dados iniciais (campus, categorias, cursos e tipos de solicitação) se não existirem.'

    def handle(self, *args, **options):
        created = {
            'campus': [],
            'categorias': [],
            'cursos': [],
            'tipos': []
        }

        # Campi de exemplo
        campus_names = ['Paranavaí', 'Toledo', 'Cascavel']
        for name in campus_names:
            obj, was_created = Campus.objects.get_or_create(nome=name)
            if was_created:
                created['campus'].append(name)

        # Categorias de sugestão
        categoria_names = ['Infraestrutura', 'Ensino', 'Segurança', 'Serviços', 'Outros']
        for name in categoria_names:
            obj, was_created = Categoria.objects.get_or_create(nome=name)
            if was_created:
                created['categorias'].append(name)

        # Cursos de exemplo vinculados ao primeiro campus
        primeiro_campus = Campus.objects.first()
        if primeiro_campus:
            curso_names = ['Análise e Desenvolvimento de Sistemas', 'Engenharia', 'Administração']
            for name in curso_names:
                obj, was_created = Curso.objects.get_or_create(nome=name, campus=primeiro_campus)
                if was_created:
                    created['cursos'].append(name)

        # Tipos de solicitação
        tipos = ['Manutenção', 'Compra de Equipamento', 'Solicitação Acadêmica']
        for t in tipos:
            obj, was_created = TipoSolicitacao.objects.get_or_create(descricao=t)
            if was_created:
                created['tipos'].append(t)

        # Relatório
        lines = []
        for k, v in created.items():
            if v:
                lines.append(f"{k}: {', '.join(v)}")

        if lines:
            self.stdout.write(self.style.SUCCESS('Dados iniciais criados:'))
            for l in lines:
                self.stdout.write(' - ' + l)
        else:
            self.stdout.write(self.style.WARNING('Nenhum dado novo criado — tudo já existia.'))
