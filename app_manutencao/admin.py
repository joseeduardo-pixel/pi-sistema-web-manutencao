from django.contrib import admin

# Register your models here.

from .models import (
    Predio, Local, Categoria, Marca, Equipamento, 
    Fornecedor, Manutencao, ItemManutencao
)
admin.site.site_header = "Sistema Web para Gestão de Manutenção de Equipamentos de Ar-condicionado"       # Título na barra azul superior
admin.site.site_title = "Admin de Manutenção"      # Título na aba do navegador
admin.site.index_title = "Bem-vindo ao Gerenciador" # Título da página inicial do admin

admin.site.register(Predio)
admin.site.register(Local)
admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Fornecedor)
admin.site.register(Manutencao)
admin.site.register(ItemManutencao)

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('patrimonio', 'marca', 'local', 'situacao')
    search_fields = ('patrimonio',)