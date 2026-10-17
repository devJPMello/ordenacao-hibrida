"""Mede o tempo da ordenação híbrida variando o corte e compara com a rápida pura.

Gera resultados.csv e grafico.png.
"""

import csv
import random
import statistics
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ordenacao import hibrida, rapida

N = 20_000
CORTES = [1, 5, 10, 16, 20, 32, 50, 100, 200]
REPETICOES = 15
SEMENTE = 42


def cronometrar(funcao, entradas):
    """Roda `funcao` em cópias de cada entrada e devolve os tempos em ms."""
    tempos = []
    for entrada in entradas:
        v = entrada.copy()
        inicio = time.perf_counter()
        resultado = funcao(v)
        tempos.append((time.perf_counter() - inicio) * 1000)
        assert resultado == sorted(entrada), "resultado não está ordenado"
    return tempos


def main():
    random.seed(SEMENTE)
    # As mesmas entradas são usadas por todas as variantes, para a comparação ser justa.
    entradas = [[random.randint(0, 10 * N) for _ in range(N)] for _ in range(REPETICOES)]

    # Aquecimento: evita que a primeira variante medida pague o custo de "esquentar" o interpretador.
    for _ in range(3):
        rapida(entradas[0].copy())

    linhas = []
    pura =cronometrar(rapida, entradas)
    linhas.append(("pura", statistics.median(pura), statistics.stdev(pura)))
    print(f"{'pura':>6}: mediana {statistics.median(pura):7.2f} ms")

    for corte in CORTES:
        tempos = cronometrar(lambda v: hibrida(v, corte), entradas)
        linhas.append((corte, statistics.median(tempos), statistics.stdev(tempos)))
        print(f"{corte:>6}: mediana {statistics.median(tempos):7.2f} ms")

    with open("resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["corte", "mediana_ms", "desvio_ms"])
        for corte, med, dp in linhas:
            w.writerow([corte, f"{med:.2f}", f"{dp:.2f}"])

    t_pura = linhas[0][1]
    hib = linhas[1:]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar([c for c, _, _ in hib], [m for _, m, _ in hib], yerr=[d for _, _, d in hib],
                marker="o", capsize=3, label="híbrida (rápida + inserção)")
    ax.axhline(t_pura, color="gray", linestyle="--", label=f"rápida pura ({t_pura:.1f} ms)")
    melhor = min(hib, key=lambda l: l[1])
    ax.annotate(f"melhor: corte = {melhor[0]}", (melhor[0], melhor[1]),
                textcoords="offset points", xytext=(10, -20))
    ax.set_xscale("log")
    ax.set_xticks(CORTES)
    ax.set_xticklabels([str(c) for c in CORTES])
    ax.set_xlabel("corte (escala log)")
    ax.set_ylabel("tempo mediano (ms)")
    ax.set_title(f"Tempo da ordenação híbrida em função do corte (n = {N:,}, {REPETICOES} repetições)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("grafico.png", dpi=120)


if __name__ == "__main__":
    main()
