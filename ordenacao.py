"""Ordenação rápida (quicksort) pura e híbrida com ordenação por inserção."""

import random


def insercao(v):
    """Ordenação por inserção. Ordena a lista no lugar e a devolve."""
    for i in range(1, len(v)):
        chave = v[i]
        j = i - 1
        while j >= 0 and v[j] > chave:
            v[j + 1] = v[j]
            j -= 1
        v[j + 1] = chave
    return v


def rapida(v):
    """Ordenação rápida pura: pivô aleatório, partição em menores/iguais/maiores."""
    if len(v) <= 1:
        return v
    pivo = random.choice(v)
    menores = [x for x in v if x < pivo]
    iguais = [x for x in v if x == pivo]
    maiores = [x for x in v if x > pivo]
    return rapida(menores) + iguais + rapida(maiores)


def hibrida(v, corte):
    """Ordenação rápida que passa para a inserção quando o pedaço tem menos que `corte` elementos.

    Com corte = 1 a inserção nunca é chamada (nenhum pedaço tem menos de 1 elemento
    além do vazio, já tratado pelo caso base), então o comportamento é o da rápida pura.
    """
    if len(v) <= 1:
        return v
    if len(v) < corte:
        return insercao(v)
    pivo = random.choice(v)
    menores = [x for x in v if x < pivo]
    iguais = [x for x in v if x == pivo]
    maiores = [x for x in v if x > pivo]
    return hibrida(menores, corte) + iguais + hibrida(maiores, corte)
