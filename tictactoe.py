import pygame, sys
import numpy as np

# inicia o jogo


# ---------
# variaveis
# ---------

#Tamanho do frame
WIDTH = 600
HEIGHT = 600

#Size das linhas e quadrados e players
linhaWidth = 15
linhaVitoriaSize = 15
nLinhas = 3
nColunas = 3
tamanhoQuadrado = 200
circuloRadius = 60
circulo_width = 15
x_width = 25
SPACE = 55

#cores
RED = (255, 0, 0)
WHITE = (255,255,255)
corBackground = (28, 170, 156)
corLinha = (23, 145, 135)
corCirculo = (239, 231, 200)
corX = (66, 66, 66)

# ------
# criar o frame 
# ------
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'Jogo da Velha' )
screen.fill( corBackground )
pygame.init()

# -------------
# matriz com as linhas e colunas do jogo
# -------------
tabuleiro = np.zeros((nLinhas, nColunas))


def desenharLinhasTabuleiro():
	# Desenhar linhas horizontais
	pygame.draw.line( screen, corLinha, (0, tamanhoQuadrado), (WIDTH, tamanhoQuadrado), linhaWidth )
	pygame.draw.line( screen, corLinha, (0, 2 * tamanhoQuadrado), (WIDTH, 2 * tamanhoQuadrado), linhaWidth )

	# Desenhar linhas verticais
	pygame.draw.line( screen, corLinha, (tamanhoQuadrado, 0), (tamanhoQuadrado, HEIGHT), linhaWidth )
	pygame.draw.line( screen, corLinha, (2 * tamanhoQuadrado, 0), (2 * tamanhoQuadrado, HEIGHT), linhaWidth )

def desenharPlayers():
	# Desenhar X e O 
	for linha in range(nLinhas):
		for col in range(nColunas):
			if tabuleiro[linha][col] == 1:
				pygame.draw.circle( screen, 
                      				corCirculo, 
                      				(int( col * tamanhoQuadrado + tamanhoQuadrado//2 ), 
                    			    int( linha * tamanhoQuadrado + tamanhoQuadrado//2 )), 
                    				circuloRadius, 
                      				circulo_width )
			elif tabuleiro[linha][col] == 2:
				pygame.draw.line( screen, 
									corX, 
									(col * tamanhoQuadrado + SPACE, 
									linha * tamanhoQuadrado + tamanhoQuadrado - SPACE), 
									(col * tamanhoQuadrado + tamanhoQuadrado - SPACE, 
									linha * tamanhoQuadrado + SPACE), 
									x_width )
    	
				pygame.draw.line( screen, 
									corX, 
									(col * tamanhoQuadrado + SPACE, 
									linha * tamanhoQuadrado + SPACE), 
									(col * tamanhoQuadrado + tamanhoQuadrado - SPACE, 
									linha * tamanhoQuadrado + tamanhoQuadrado - SPACE), 
									x_width )

def marcarQuadrado(linha, col, player):
	tabuleiro[linha][col] = player

def quadradosDisponiveis(linha, col):
	return tabuleiro[linha][col] == 0



def checkVitoria(player):
	# check vitoria vertical 
	for col in range(nColunas):
		if tabuleiro[0][col] == player and tabuleiro[1][col] == player and tabuleiro[2][col] == player:
			desenharLinhaVitoriaVertical(col, player)
			showVitoria(player, 'vitoria')
			return True

	# check vitoria horizontal 
	for linha in range(nLinhas):
		if tabuleiro[linha][0] == player and tabuleiro[linha][1] == player and tabuleiro[linha][2] == player:
			desenharLinhaVitoriaHorizontal(linha, player)
			showVitoria(player, 'vitoria')
			return True

	# check vitoria diagonal asc 
	if tabuleiro[2][0] == player and tabuleiro[1][1] == player and tabuleiro[0][2] == player:
		desenharDiagonalASC(player)
		showVitoria(player, 'vitoria')
		return True

	# check vitoria vertical desc
	if tabuleiro[0][0] == player and tabuleiro[1][1] == player and tabuleiro[2][2] == player:
		desenharDiagonalDESC(player)
		showVitoria(player, 'vitoria')
		return True

	# check empate
	if is_tabuleiro_full():
		showVitoria(player, 'empate')
		return True

	return False

def is_tabuleiro_full():
	for linha in range(nLinhas):
		for col in range(nColunas):
			if tabuleiro[linha][col] == 0:
				return False
	return True

def desenharLinhaVitoriaVertical(col, player):
	posX = col * tamanhoQuadrado + tamanhoQuadrado//2

	if player == 1:
		color = corCirculo
	elif player == 2:
		color = corX

	pygame.draw.line( screen, color, (posX, 15), (posX, HEIGHT - 15), linhaWidth )

def desenharLinhaVitoriaHorizontal(linha, player):
	posY = linha * tamanhoQuadrado + tamanhoQuadrado//2

	if player == 1:
		color = corCirculo
	elif player == 2:
		color = corX

	pygame.draw.line( screen, color, (15, posY), (WIDTH - 15, posY), linhaVitoriaSize )
	
def desenharDiagonalASC(player):
	if player == 1:
		color = corCirculo
	elif player == 2:
		color = corX

	pygame.draw.line( screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), linhaVitoriaSize )

def desenharDiagonalDESC(player):
	if player == 1:
		color = corCirculo
	elif player == 2:
		color = corX

	pygame.draw.line( screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), linhaVitoriaSize )
	

def showVitoria(playerName, status):
	font = pygame.font.Font('freesansbold.ttf', 32)
	if status == 'vitoria':
		text = font.render('Player ' + str(playerName) + ' ganhou', True, WHITE, RED)
  
	elif status == 'empate':
		text = font.render('Deu Velha!', True, WHITE, RED)
     
	textRect = text.get_rect()
	screen.blit(text, (0, 0))
 

def restart():
	screen.fill( corBackground )
	desenharLinhasTabuleiro()
	for linha in range(nLinhas):
		for col in range(nColunas):
			tabuleiro[linha][col] = 0

desenharLinhasTabuleiro()


# --------
# Main
# --------

player = 1
game_over = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

			mouseX = event.pos[0] # x
			mouseY = event.pos[1] # y

			clicked_linha = int(mouseY // tamanhoQuadrado)
			clicked_col = int(mouseX // tamanhoQuadrado)

			if quadradosDisponiveis( clicked_linha, clicked_col ):

				marcarQuadrado( clicked_linha, clicked_col, player )
				if checkVitoria( player ):
					game_over = True
					
				player = player % 2 + 1

				desenharPlayers()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				restart()
				player = 1
				game_over = False

	pygame.display.update()

