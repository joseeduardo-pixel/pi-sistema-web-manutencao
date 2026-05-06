from django.db import models

# Create your models here.

class Predio(models.Model):
    nome_predio = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome_predio

class Local(models.Model):
    nome_local = models.CharField(max_length=100)
    predio = models.ForeignKey(Predio, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_local

class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_categoria

class Marca(models.Model):
    marca = models.CharField(max_length=100)

    def __str__(self):
        return self.marca

class Equipamento(models.Model):
    patrimonio = models.CharField(max_length=50, unique=True)
    capacidade = models.DecimalField(max_digits=10, decimal_places=2)
    unidade_medida = models.CharField(max_length=20)
    valor_bem = models.DecimalField(max_digits=10, decimal_places=2)
    situacao = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    local = models.ForeignKey(Local, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.patrimonio} - {self.marca}"

class Fornecedor(models.Model):
    razao_social = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.razao_social

class Manutencao(models.Model):
    data = models.DateField()
    nota_fiscal = models.CharField(max_length=50)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    solicitacao = models.IntegerField()
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"Manutenção {self.id} - {self.data}"

class ItemManutencao(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    manutencao = models.ForeignKey(Manutencao, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)

   