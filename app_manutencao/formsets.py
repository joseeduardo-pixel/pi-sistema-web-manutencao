'''

# =========================
# MANUTENÇÃO (SUBFORM DO EQUIPAMENTO)
# =========================
ManutencaoFormSet = inlineformset_factory(
    parent_model=Equipamento,
    model=Manutencao,
    form=ManutencaoForm,
    extra=1,
    can_delete=True
)


# =========================
# ITENS (SUBFORM DA MANUTENÇÃO)
# =========================
ItemManutencaoFormSet = inlineformset_factory(
    parent_model=Manutencao,
    model=ItemManutencao,
    form=ItemManutencaoForm,
    extra=1,
    can_delete=True
)

ItemManutencaoFormSet = inlineformset_factory(
    Manutencao,
    ItemManutencao,
    fields=['equipamento', 'descricao', 'quantidade', 'valor_unitario'],
    extra=1,
    can_delete=True
)

ManutencaoFormSet = inlineformset_factory(
    Equipamento,
    Manutencao,
    fields=['data', 'nota_fiscal', 'fornecedor', 'solicitacao'],
    extra=1,
    can_delete=True
)
    data = models.DateField()
    nota_fiscal = models.CharField(max_length=50)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    solicitacao = models.IntegerField()
    finalizado = models.BooleanField(default=False)

'''