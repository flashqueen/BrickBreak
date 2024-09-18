import pygame

#inicialização
pygame.init()

#tela
tamanho_tela = (800, 800)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Brick Break")

#elementos
tamanho_bola = 15
bola = pygame.Rect(100, 500, tamanho_bola, tamanho_bola)
tamanho_jogador = 100
jogador = pygame.Rect(0, 750, tamanho_jogador, 15)

qtde_blocos_linha = 8
qtde_linhas_blocos = 5
qtde_total_blocos = qtde_blocos_linha * qtde_linhas_blocos
qtde_coracao_total = 3

def criar_blocos(qtde_blocos_linha, qtde_linhas_blocos):
    altura_tela = tamanho_tela[1]
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / 8 - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10


    blocos = []
    #criar os blocos
    for j in range(qtde_linhas_blocos):
        for i in range(qtde_blocos_linha):
            #criar o bloco
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), j * distancia_entre_linhas, largura_bloco, altura_bloco)
            #adicionar a lista de blocos
            blocos.append(bloco)
    
    return blocos

def criar_coracao(qtde_coracao_total):
    altura_tela = tamanho_tela[0]
    largura_tela = tamanho_tela[1]
    distancia_entre_coracao = 5
    largura_coracao = largura_tela / 3 - distancia_entre_coracao
    altura_coracao = 15

    coracoes = []
    #criar os coracoes
    for c in range(qtde_coracao_total):
        #criar o coração
        coracao = pygame.Rect(c * (largura_coracao + distancia_entre_coracao), altura_coracao, largura_coracao, altura_coracao)
        #adicionar a lista de corações
        coracoes.append(coracao)

    return coracoes


cores = {
    "branco": (255, 255, 255),
    "preto": (0, 0, 0),
    "amarelo": (255, 255, 0),
    "verde":(0, 100, 0),
    "roxo": (177, 156, 217),
    "cereja": (255, 36, 92)
}

fim_jogo = False
pontuacao = 0
movimento_bola = [2, -2]

#Desenhar a tela
def desenhar_inicio_jogo():
    tela.fill(cores["preto"])
    pygame.draw.rect(tela, cores["verde"], jogador)
    pygame.draw.rect(tela, cores["branco"], bola)

def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["roxo"], bloco)

# def desenhar_coracoes(coracoes):
#     for coracao in coracoes:
#         pygame.draw.circle(tela, cores["cereja"], (720,720), 4)

#funções do jogo
def movimentar_jogador(evento):
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_RIGHT:
            if (jogador.x + tamanho_jogador) < tamanho_tela[0]:
                jogador.x = jogador.x + 2
        if evento.key == pygame.K_LEFT:
            if jogador.x > 0:
                jogador.x = jogador.x - 2
    

def movimentar_bola(bola):
    movimento = movimento_bola
    
    bola.x = bola.x + movimento[0]
    bola.y = bola.y + movimento[1]

    if bola.x <= 0:
        movimento[0] = - movimento[0]
    if bola.y <= 0:
        movimento[1] = - movimento[1]
    if bola.x + tamanho_bola >= tamanho_tela[0]:
        movimento[0] = - movimento[0]
    if bola.y + tamanho_bola >= tamanho_tela[1]:
       movimento[1] = - movimento[1]
       reduzir_vida()
       if qtde_coracao_total == 0:
           movimento = None

    if jogador.collidepoint(bola.x, bola.y):
        movimento[1] = - movimento[1]
    for bloco in blocos:
        if bloco.collidepoint(bola.x, bola.y):
            blocos.remove(bloco)
            movimento[1] = - movimento[1]

    return movimento

def reduzir_vida(coracao):
    vidas = coracao

    if bola.y + tamanho_bola >= tamanho_tela[1]:
       vidas - 1
       if vidas == 0:
           movimento = None
       return vidas

def atualizar_pontuacao(pontuacao):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontuação: {pontuacao}", 1, cores["amarelo"])
    tela.blit(texto, (0, 780))
    if pontuacao >= qtde_total_blocos:
        return True
    else:
        return False
    
def atualizar_vidas(coracao):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Vidas: {coracao}", 1, cores["cereja"])
    tela.blit(texto, (700, 700))

blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos)

coracoes = criar_coracao(qtde_coracao_total)

#loop infinito
while not fim_jogo:
    desenhar_inicio_jogo()
    desenhar_blocos(blocos)
    # desenhar_coracoes(coracoes)
    atualizar_vidas(qtde_coracao_total)
    fim_jogo = atualizar_pontuacao(qtde_total_blocos - len(blocos))
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo = True
    
    movimentar_jogador(evento)

    movimento_bola = movimentar_bola(bola)
    if not movimento_bola:
        fim_jogo = True
    pygame.time.wait(1)
    pygame.display.flip()

pygame.quit()