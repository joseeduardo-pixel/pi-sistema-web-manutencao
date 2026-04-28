from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.db.models import Sum, F, ExpressionWrapper, DecimalField

from .models import Equipamento, ItemManutencao
from .forms import EquipamentoForm, ItemManutencaoFormSet, ManutencaoForm

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa


from django.views.generic import View
# =========================
# REGISTER
# =========================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# =========================
# LISTA DE EQUIPAMENTOS
# =========================
@login_required
def lista_equipamentos(request):
    equipamentos = Equipamento.objects.all()
    return render(request, 'equipamentos/lista.html', {'equipamentos': equipamentos})


# =========================
# PROFILE
# =========================
@login_required
def profile(request):
    return render(request, 'registration/profile.html')


# =========================
# CADASTRO EQUIPAMENTO + ITENS
# =========================
@login_required
def cadastro_equipamento(request):

    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        formset = ItemManutencaoFormSet(request.POST, prefix='itens')

        if form.is_valid() and formset.is_valid():
            equipamento = form.save()

            itens = formset.save(commit=False)
            for item in itens:
                item.equipamento = equipamento
                item.save()

            messages.success(request, 'Equipamento cadastrado com sucesso!')
            return redirect('lista_equipamentos')

    else:
        form = EquipamentoForm()
        formset = ItemManutencaoFormSet(prefix='itens')

    return render(request, 'equipamentos/form.html', {
        'form': form,
        'formset': formset,
    })


# =========================
# RELATÓRIO
# =========================
@login_required
def relatorio_equipamentos(request):

    equipamentos = Equipamento.objects.all()

    dados = []

    for equipamento in equipamentos:

        itens = ItemManutencao.objects.filter(equipamento=equipamento)

        # calcula total por item
        for i in itens:
            i.total_item = i.quantidade * i.valor_unitario

        # soma total do equipamento
        total = itens.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('quantidade') * F('valor_unitario'),
                    output_field=DecimalField()
                )
            )
        )['total'] or 0

        dados.append({
            'equipamento': equipamento,
            'itens': itens,
            'total': total
        })

    return render(request, 'relatorios/relatorio_equipamentos.html', {'dados': dados})

##incluido depois
'''
@login_required
def relatorio(request):

    dados = gerar_dados()  # ou Equipamento.objects.all()

    com_manutencao = []
    sem_manutencao = []

    for item in dados:
        if item['itens']:
            com_manutencao.append(item)
        else:
            sem_manutencao.append(item)

    context = {
        'com_manutencao': com_manutencao,
        'sem_manutencao': sem_manutencao,
    }

    return render(request, 'relatorio_equipamentos.html', context)
'''

@login_required
def relatorio(request):

    dados = gerar_dados()

    com_manutencao = []
    sem_manutencao = []

    for item in dados:

        # 🔥 FILTRO GARANTIDO (funciona mesmo se for lista)
        itens_filtrados = [
            i for i in item['itens']
            if not i.manutencao.finalizado
        ]

        # Atualiza os itens
        item['itens'] = itens_filtrados

        # Recalcula total
        item['total'] = sum(i.total_item for i in itens_filtrados)

        # Separação
        if itens_filtrados:
            com_manutencao.append(item)
        else:
            sem_manutencao.append(item)

    context = {
        'com_manutencao': com_manutencao,
        'sem_manutencao': sem_manutencao,
    }

    return render(request, 'relatorio_equipamentos.html', context)
    






@login_required
def cadastrar_manutencao(request):

    if request.method == 'POST':
        manutencao_form = ManutencaoForm(request.POST)
        formset = ItemManutencaoFormSet(request.POST)

        if manutencao_form.is_valid() and formset.is_valid():
            manutencao = manutencao_form.save()


            itens = formset.save(commit=False)
            for item in itens:
                item.manutencao = manutencao
                item.save()

            return redirect('relatorio')

    else:
        manutencao_form = ManutencaoForm()
        formset = ItemManutencaoFormSet()

    return render(request, 'manutencao/form.html', {
        'manutencao_form': manutencao_form,  # 🔥 TEM QUE SER ESSE NOME
        'formset': formset
    })


### ALTERAÇÃO PARA INSERIR TOTAL GERAL NO RELATÓRIO DE MANUTENÇÕES POR EQUIPAMENTO
'''
def relatorio_view(request):
    # ... sua lógica para gerar a lista 'dados' ...
    
    # CALCULE O TOTAL GERAL AQUI
    total_geral = sum(item['total'] for item in dados if 'total' in item)

    context = {
        'dados': dados,
        'total_geral': total_geral,  # Enviando a soma para o HTML
    }
    return render(request, 'seu_template.html', context)

'''
### ALTERAÇÃO PARA INSERIR TOTAL GERAL NO RELATÓRIO DE TODOS EQUIPAMENTOS

@login_required
def relatorio_manutencao(request):
    dados = [] # Aqui está a sua lista de equipamentos que você já tem
    
    # --- ADICIONE ESTA LINHA ---
    total_geral_relatorio = sum(item['total'] for item in dados if item.get('total'))

    context = {
        'dados': dados,
        'total_geral': totalN_geral_relatorio, # O nome aqui deve ser igual ao do HTML
    }
    return render(request, 'seu_template.html', context)



'''

@login_required
def relatorio_pdf(request):
    # Buscamos os equipamentos
    equipamentos = Equipamento.objects.all()
    dados = []
    total_geral_relatorio = 0
    nome_predio = "UNESP - Campus de Marília"

    for equipamento in equipamentos:
        # FILTRO CRUCIAL:
        # 1. Buscamos em ItemManutencao
        # 2. Filtramos pela relação 'manutencao' onde o campo 'finalizado' é False
        # 3. select_related evita centenas de consultas extras ao banco (performance)
        itens_pendentes = ItemManutencao.objects.filter(
            equipamento=equipamento,
            manutencao__finalizado=False
        ).select_related('manutencao')

        # Se não houver itens abertos para este equipamento, pulamos para o próximo
        if itens_pendentes.exists():
            total_equip = 0
            
            for i in itens_pendentes:
                # Cálculo do total do item (Quantidade x Valor)
                i.total_item = i.quantidade * i.valor_unitario
                total_equip += i.total_item

            # Só adicionamos ao relatório se o valor total for maior que zero
            if total_equip > 0:
                total_geral_relatorio += total_equip
                dados.append({
                    'equipamento': equipamento,
                    'itens': itens_pendentes,
                    'total': total_equip
                })

    # Caso nenhum equipamento tenha manutenção aberta
    if not dados:
        return HttpResponse("<h2>Nenhuma manutenção pendente encontrada.</h2>")

    html = render_to_string('relatorios/relatorio_equipamentos_pdf.html', {
        'dados': dados,
        'total_geral': total_geral_relatorio,
        'nome_predio': nome_predio,
    })

    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response

'''

#VIEW FUNCIONAL PARA RELATÓRIO PDF, PORÉM NÃO FILTRA FINALIZADOS


@login_required
def relatorio_pdf(request):
    equipamentos = Equipamento.objects.all()
    dados = []
    total_geral_relatorio = 0

    # Exemplo: Pegar o nome do prédio do primeiro equipamento ou definir um título
    nome_predio = "UNESP - Campus de Marília" # Pode vir de equipamento.predio se existir

    for equipamento in equipamentos:
        itens = ItemManutencao.objects.filter(equipamento=equipamento)
        for i in itens:
            i.total_item = i.quantidade * i.valor_unitario

        total_equip = sum(i.total_item for i in itens) if itens else 0
        total_geral_relatorio += total_equip

        dados.append({
            'equipamento': equipamento,
            'itens': itens,
            'total': total_equip
        })

    html = render_to_string('relatorios/relatorio_equipamentos_pdf.html', {
        'dados': dados,
        'total_geral': total_geral_relatorio,
        'nome_predio': nome_predio, # <-- NOVA VARIÁVEL
    })

    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response






@login_required
def cadastro_equipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipamento cadastrado!")
            return redirect('cadastro_equipamento')
    else:
        form = EquipamentoForm()

    # Busca os últimos 6 equipamentos do banco de dados
    recentes = Equipamento.objects.all().order_by('-id')[:6] 

    return render(request, 'cadastro_equipamento.html', {
        'form': form,
        'recentes': recentes
    })



@login_required
def cadastro_manutencao(request):
    form = ManutencaoForm(request.POST or None)
    formset = ItemManutencaoFormSet(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            manutencao = form.save() 
            instancias = formset.save(commit=False)
            for item in instancias:
                item.manutencao = manutencao 
                item.save()
            
            # ALTERAÇÃO AQUI: 
            # Em vez de 'home', usamos o nome da url desta mesma view
            return redirect('cadastro_manutencao') 
            
    return render(request, 'cadastro_manutencao.html', {
        'form': form,
        'itens': formset
    })

