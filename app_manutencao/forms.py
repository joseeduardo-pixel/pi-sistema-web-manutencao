from django import forms
from .models import Equipamento, Manutencao, ItemManutencao
from django.forms import inlineformset_factory

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = '__all__'
        widgets = {
            # Adicionando classes do Bootstrap para ficar bonito
            'patrimonio': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidade_medida': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_bem': forms.NumberInput(attrs={'class': 'form-control'}),
            'situacao': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'local': forms.Select(attrs={'class': 'form-control'}),
        }

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['data', 'nota_fiscal', 'fornecedor', 'solicitacao', 'finalizado']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nota_fiscal': forms.TextInput(attrs={'class': 'form-control'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'solicitacao': forms.NumberInput(attrs={'class': 'form-control'}),
            'finalizado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Isso permite adicionar itens dentro da tela de manutenção
ItemManutencaoFormSet = inlineformset_factory(
    Manutencao, ItemManutencao,
    fields=['equipamento', 'descricao', 'quantidade', 'valor_unitario'],
    extra=3, # Quantidade de linhas em branco que aparecem
    widgets={
        'equipamento': forms.Select(attrs={'class': 'form-control'}),
        'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        'valor_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)


## incluido em 18-08-2026
from django import forms
from .models import Equipamento

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Este loop adiciona automaticamente a classe do Bootstrap a TODOS os campos
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})