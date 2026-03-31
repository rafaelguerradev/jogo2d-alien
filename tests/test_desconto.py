import pytest
from src.desconto import DescontoNormal, DescontoVIP, DescontoPremium

@pytest.mark.parametrize("valor, esperado", [
    (100, 30),
    (200, 60),
    (300, 90)
])

def test_desconto_premium(valor, esperado):
    desconto = DescontoPremium()
    resultado = desconto.calcular(valor)

    assert resultado == esperado

def test_desconto_normal():
    desconto = DescontoNormal()
    resultado = desconto.calcular(100)
    assert resultado == 10, f"Esperado 10, mas obteve {resultado}"


@pytest.fixture
def desconto_vip():
    return DescontoVIP()

def test_desconto_vip_100(desconto_vip):
    assert desconto_vip.calcular(100) == 20

def test_desconto_vip_200(desconto_vip):
    assert desconto_vip.calcular(200) == 40

