from django.db import migrations


def seed_companies(apps, schema_editor):
    CompanyCategory = apps.get_model('companies', 'CompanyCategory')
    Company = apps.get_model('companies', 'Company')

    # Categorias
    categories = {
        'crm': {
            'name': 'CRM e Vendas',
            'slug': 'crm',
            'description': 'Soluções de CRM e aceleração de vendas',
            'color': '#7c3aed',
        },
        'lancamentos': {
            'name': 'Lançamentos e Infoprodutos',
            'slug': 'lancamentos',
            'description': 'Método de lançamentos para infoprodutores',
            'color': '#ff6b35',
        },
        'automacao': {
            'name': 'Automação e Operação',
            'slug': 'automacao',
            'description': 'Automação de processos comerciais e integrações',
            'color': '#0ea5e9',
        },
        'mentoria': {
            'name': 'Mentoria e Estratégia',
            'slug': 'mentoria',
            'description': 'Consultoria e mentoria estratégica de vendas',
            'color': '#f59e0b',
        },
    }

    created_categories = {}
    for key, data in categories.items():
        obj, _ = CompanyCategory.objects.get_or_create(slug=data['slug'], defaults=data)
        created_categories[key] = obj

    # Empresas
    companies = [
        {
            'name': 'Leadspot',
            'slug': 'leadspot',
            'tagline': 'O CRM que converte mais e melhor',
            'description': '<p>Muitos negócios perdem dinheiro porque não sabem transformar leads em vendas. Desenvolvemos um CRM que integra toda a jornada e otimiza processos para conversões reais.</p>',
            'website_url': 'https://leadspot.com.br',
            'category': created_categories['crm'],
            'order': 1,
        },
        {
            'name': 'LauncherX',
            'slug': 'launcherx',
            'tagline': 'Estratégia, escala e resultados para infoprodutores',
            'description': '<p>Lançamentos no modelo de sociedade e co-produção, com método e time sênior focado em crescimento e previsibilidade.</p>',
            'website_url': 'https://launcherx.com.br',
            'category': created_categories['lancamentos'],
            'order': 2,
        },
        {
            'name': 'Fluxo',
            'slug': 'fluxo',
            'tagline': 'Automação, eficiência e escalabilidade para sua operação',
            'description': '<p>Automatizamos processos, integramos CRM e entregamos dashboards para ganho de eficiência e escala.</p>',
            'website_url': 'https://fluxo.kaizen.com.br',
            'category': created_categories['automacao'],
            'order': 3,
        },
        {
            'name': 'Hacker das Vendas',
            'slug': 'hacker-das-vendas',
            'tagline': 'Consultoria e mentoria estratégica para escalar resultados',
            'description': '<p>Estratégia, posicionamento, ofertas e operação de vendas com foco em faturar com previsibilidade.</p>',
            'website_url': 'https://hackerdasvendas.com.br',
            'category': created_categories['mentoria'],
            'order': 4,
        },
    ]

    for data in companies:
        Company.objects.get_or_create(slug=data['slug'], defaults=data)


def unseed_companies(apps, schema_editor):
    Company = apps.get_model('companies', 'Company')
    Company.objects.filter(slug__in=['leadspot', 'launcherx', 'fluxo', 'hacker-das-vendas']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('companies', '0004_fluxopage'),
    ]

    operations = [
        migrations.RunPython(seed_companies, reverse_code=unseed_companies),
    ]


