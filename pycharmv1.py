# -*- coding: utf-8 -*-
"""pycharmV1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LEA47EbNg3DRLmzhYBm8mU3GCm8dthhj
"""

# Peças: E=Elefante, C=Camelo, A=Cavalo, D=Cachorro, G=Gato, O=Coelho

import sys
import math
from copy import deepcopy

class EstadoJogo:
    def __init__(self, tabuleiro, jogador, mov_restantes, fim=False, vencedor=None):
        self.tabuleiro = tabuleiro
        self.jogador = jogador
        self.mov_restantes = mov_restantes
        self.fim = fim
        self.vencedor = vencedor

    def copiar(self):
        return EstadoJogo(
            [linha.copy() for linha in self.tabuleiro],
            self.jogador,
            self.mov_restantes,
            self.fim,
            self.vencedor
        )

def criar_tabuleiro():
    return [
        ['O', 'O', 'O', 'O', 'O', 'G', 'D', 'A'],
        ['E', 'C', 'A', 'D', 'G', 'O', 'O', 'O'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'E', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'o', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', 'g', 'd', 'a'],
        ['e', 'c', 'a', 'd', 'g', ' ', ' ', ' ']
    ]

def mostrar_tabuleiro(tab):
    print("\n  a b c d e f g h")
    for i in range(8):
        print(f"{8-i} ", end="")
        for celula in tab[i]:
            print(celula if celula != ' ' else '.', end=" ")
        print(f"{8-i}")
    print("  a b c d e f g h\n")

def verificar_congelamento(tab, x, y, jogador):
    peca = tab[x][y].lower()
    adversario = 'Prata' if jogador == 'Ouro' else 'Ouro'

    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8:
            vizinha = tab[nx][ny]
            if (adversario == 'Ouro' and vizinha.isupper()) or (adversario == 'Prata' and vizinha.islower()):
                if forcas[vizinha.lower()] > forcas[peca]:
                    tem_aliado = False
                    for dx2, dy2 in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nx2, ny2 = x + dx2, y + dy2
                        if 0 <= nx2 < 8 and 0 <= ny2 < 8:
                            aliado = tab[nx2][ny2]
                            if (jogador == 'Ouro' and aliado.isupper()) or (jogador == 'Prata' and aliado.islower()):
                                tem_aliado = True
                                break
                    if not tem_aliado:
                        return True
    return False

def validar_movimento(tab, x, y, direcao, jogador):
    dx, dy = direcoes[direcao]
    novo_x = x + dx
    novo_y = y + dy

    if not (0 <= novo_x < 8) or not (0 <= novo_y < 8):
        return False

    peca = tab[x][y]
    if (jogador == 'Ouro' and not peca.isupper()) or (jogador == 'Prata' and not peca.islower()):
        return False

    if verificar_congelamento(tab, x, y, jogador):
        return False

    destino = tab[novo_x][novo_y]

    if destino == ' ':
        return True

    if (jogador == 'Ouro' and destino.islower()) or (jogador == 'Prata' and destino.isupper()):
        if forcas[peca.lower()] > forcas[destino.lower()]:
            empurrar_x = novo_x + dx
            empurrar_y = novo_y + dy
            if 0 <= empurrar_x < 8 and 0 <= empurrar_y < 8:
                return tab[empurrar_x][empurrar_y] == ' '

    return False

def executar_movimento(estado, origem, direcao):
    x, y = origem
    dx, dy = direcoes[direcao]
    novo_estado = estado.copiar()
    tab = novo_estado.tabuleiro
    peca = tab[x][y]

    if tab[x+dx][y+dy] == ' ':
        tab[x][y] = ' '
        tab[x+dx][y+dy] = peca
    else:
        inimigo = tab[x+dx][y+dy]
        tab[x][y] = ' '
        tab[x+dx][y+dy] = peca
        if 0 <= x+dx*2 < 8 and 0 <= y+dy*2 < 8:
            tab[x+dx*2][y+dy*2] = inimigo

    for dx_p, dy_p in [(-1,0), (1,0), (0,-1), (0,1)]:
        px = x - dx_p
        py = y - dy_p
        if 0 <= px < 8 and 0 <= py < 8:
            peca_puxar = tab[px][py]
            if ((novo_estado.jogador == 'Ouro' and peca_puxar.islower()) or
                (novo_estado.jogador == 'Prata' and peca_puxar.isupper())):
                if forcas[peca.lower()] > forcas[peca_puxar.lower()]:
                    tab[x][y] = peca_puxar
                    tab[px][py] = ' '
                    break

    novo_estado.mov_restantes -= 1
    return novo_estado

def processar_capturas(estado):
    tab = estado.tabuleiro
    for x in range(8):
        for y in range(8):
            if tab[x][y] != ' ':
                jogador = 'Ouro' if tab[x][y].isupper() else 'Prata'
                if verificar_congelamento(tab, x, y, jogador):
                    tab[x][y] = ' '

def verificar_vitoria(estado):
    linha_alvo = 7 if estado.jogador == 'Ouro' else 0
    peca_alvo = 'O' if estado.jogador == 'Ouro' else 'o'

    for y in range(8):
        if estado.tabuleiro[linha_alvo][y] == peca_alvo:
            return True

    coelhos_inimigos = 0
    for linha in estado.tabuleiro:
        for peca in linha:
            if (estado.jogador == 'Ouro' and peca == 'o') or (estado.jogador == 'Prata' and peca == 'O'):
                coelhos_inimigos += 1
    return coelhos_inimigos == 0

forcas = {'e':6, 'c':5, 'a':4, 'd':3, 'g':2, 'o':1}
direcoes = {
    'cima': (-1,0),
    'baixo': (1,0),
    'esquerda': (0,-1),
    'direita': (0,1)
}

class IAJogador:  # <--- CLASSE IA ADICIONADA AQUI
    def __init__(self, profundidade=2, jogador='Prata'):
        self.profundidade = profundidade
        self.jogador = jogador

    def avaliar_estado(self, estado):
        if estado.fim:
            return math.inf if estado.vencedor == self.jogador else -math.inf

        score = 0
        coelhos_inimigos = 0
        coelhos_aliados = 0

        for x in range(8):
            for y in range(8):
                peca = estado.tabuleiro[x][y]
                if peca == ' ':
                    continue

                aliado = (self.jogador == 'Prata' and peca.islower()) or (self.jogador == 'Ouro' and peca.isupper())

                valor = forcas[peca.lower()] * 10
                if aliado:
                    score += valor
                    if peca.lower() == 'o':
                        coelhos_aliados += 1
                        if self.jogador == 'Prata':
                            score += x * 5
                        else:
                            score += (7 - x) * 5
                else:
                    score -= valor
                    if peca.lower() == 'o':
                        coelhos_inimigos += 1
                        if self.jogador == 'Prata':
                            score -= (7 - x) * 5
                        else:
                            score -= x * 5

                centro_x, centro_y = 3.5, 3.5
                dist_centro = abs(x - centro_x) + abs(y - centro_y)
                if aliado:
                    score += (4 - dist_centro) * (2 if peca.lower() != 'o' else 5)
                else:
                    score -= (4 - dist_centro) * (2 if peca.lower() != 'o' else 5)

                if verificar_congelamento(estado.tabuleiro, x, y, 'Ouro' if peca.isupper() else 'Prata'):
                    if aliado:
                        score -= 15
                    else:
                        score += 15

        score += (4 - coelhos_inimigos) * 100
        score -= (4 - coelhos_aliados) * 100
        return score

    def gerar_movimentos(self, estado):
        movimentos = []
        for x in range(8):
            for y in range(8):
                peca = estado.tabuleiro[x][y]
                if peca == ' ' or (self.jogador == 'Prata' and peca.isupper()) or (self.jogador == 'Ouro' and peca.islower()):
                    continue

                for direcao in direcoes:
                    if validar_movimento(estado.tabuleiro, x, y, direcao, estado.jogador):
                        movimentos.append((x, y, direcao))
        return movimentos

    def minimax(self, estado, profundidade, alpha, beta, maximizando):
        if profundidade == 0 or estado.fim:
            return self.avaliar_estado(estado), None

        movimentos = self.gerar_movimentos(estado)
        if not movimentos:
            return self.avaliar_estado(estado), None

        melhor_mov = None
        if maximizando:
            max_eval = -math.inf
            for x, y, dir in movimentos:
                novo_estado = executar_movimento(deepcopy(estado), (x, y), dir)
                if novo_estado is None:
                    continue

                avaliacao, _ = self.minimax(novo_estado, profundidade-1, alpha, beta, False)

                if avaliacao > max_eval:
                    max_eval = avaliacao
                    melhor_mov = (x, y, dir)
                alpha = max(alpha, avaliacao)
                if beta <= alpha:
                    break
            return max_eval, melhor_mov
        else:
            min_eval = math.inf
            for x, y, dir in movimentos:
                novo_estado = executar_movimento(deepcopy(estado), (x, y), dir)
                if novo_estado is None:
                    continue

                avaliacao, _ = self.minimax(novo_estado, profundidade-1, alpha, beta, True)

                if avaliacao < min_eval:
                    min_eval = avaliacao
                    melhor_mov = (x, y, dir)
                beta = min(beta, avaliacao)
                if beta <= alpha:
                    break
            return min_eval, melhor_mov

    def melhor_jogada(self, estado):
        if estado.jogador != self.jogador:
            return None

        _, movimento = self.minimax(estado, self.profundidade, -math.inf, math.inf, True)
        return movimento

def main():
    estado = EstadoJogo(criar_tabuleiro(), 'Ouro', 4)
    ia = IAJogador(profundidade=2, jogador='Prata')

    print("Bem-vindo ao Arimaa!")
    print("Você joga como Ouro (peças maiúsculas)")
    print("Digite movimentos no formato 'a3 cima'")
    print("---------------------------------------")

    while not estado.fim:
        mostrar_tabuleiro(estado.tabuleiro)
        print(f"Turno de: {estado.jogador}")
        print(f"Movimentos restantes: {estado.mov_restantes}")

        if estado.mov_restantes == 0:
            processar_capturas(estado)
            estado.jogador = 'Prata' if estado.jogador == 'Ouro' else 'Ouro'
            estado.mov_restantes = 4
            continue

        if estado.jogador == 'Prata':
            print("\nIA está jogando...")
            movimento = ia.melhor_jogada(estado)

            if movimento:
                x, y, dir = movimento
                pos = f"{chr(y + ord('a'))}{8 - x}"
                print(f"IA moveu: {pos} {dir}")
                estado = executar_movimento(estado, (x, y), dir)
            else:
                print("IA não encontrou movimentos válidos!")
                estado.mov_restantes = 0
        else:
            try:
                entrada = input("Sua jogada (ex: a7 cima): ").lower().split()
                if len(entrada) != 2:
                    print("Formato inválido! Use: letra número direção")
                    continue

                pos, dir = entrada
                if len(pos) != 2 or not pos[0].isalpha() or not pos[1].isdigit():
                    print("Posição inválida!")
                    continue

                y = ord(pos[0]) - ord('a')
                x = 8 - int(pos[1])

                if not validar_movimento(estado.tabuleiro, x, y, dir, estado.jogador):
                    print("Movimento inválido!")
                    continue

                estado = executar_movimento(estado, (x, y), dir)

            except Exception as e:
                print(f"Erro: {str(e)}")

        if verificar_vitoria(estado):
            estado.fim = True
            print(f"\n=== {estado.jogador} VENCEU! ===")
            mostrar_tabuleiro(estado.tabuleiro)

if __name__ == "__main__":
    main()
