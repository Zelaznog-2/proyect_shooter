# ¡Crea tu propio juego de disparos!
from pygame import *
from random import randint

init()

# CONSTANTES
ANCHO = 1000
ALTO = 1000
FPS = 30

pantalla = display.set_mode((ANCHO, ALTO))
reloj = time.Clock()


# clase padre para otros objetos
class GameSprite(sprite.Sprite):
    # constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # llamamos al constructor de la clase (Sprite):
        sprite.Sprite.__init__(self)

        # cada objeto debe almacenar una propiedad image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # cada objeto debe almacenar la propiedad rect en la cual está inscrito
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # método que dibuja al personaje en la ventana
    def reset(self):
        pantalla.blit(self.image, (self.rect.x, self.rect.y))

    # Verifica si hubo una colision
    def isCollision(self, object):
        return self.rect.colliderect(object.rect)

# Listas 
enemigos = []
bullets = []

# clase del jugador principal
class Bullet(GameSprite):
    def moveUp(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 :
            if self in bullets:
                bullets.remove(self)

class Player(GameSprite):
    
    def moves(self):
        keys = key.get_pressed()

        if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 0:
            self.rect.x -= self.speed
        elif (keys[K_d] or keys[K_RIGHT]) and self.rect.x < ANCHO - self.rect.width:
            self.rect.x += self.speed

    def shoot(self):
            bullet = Bullet('bullet.png', self.rect.x + 20, self.rect.y - 50, 60, 60, 5)
            bullets.append(bullet)
            mixer.music.load('fire.ogg')
            mixer.music.play()


class Enemy(GameSprite):
    def moveDown(self):
        self.rect.y += self.speed
        if self.rect.y > ALTO + 20:
            self.rect.y = 0

# FUNCIONES 
def setTextos(text, size, fuente = 'Arial', coors = (0, 0), color = (255, 255, 255)):
    sysFont = font.SysFont(fuente, size)
    render = sysFont.render(text, '', color)
    pantalla.blit(render, coors)



# objectos 
jugador = Player('rocket.png', 400, 850, 100, 100, 10)


# Creacion de enemigos
def generarEnemigos():
    for i in range(randint(4, 10)):
        tmpSpeed = randint(1, 5)
        tmpX = randint(0, ANCHO - 100)
        enemigo = Enemy('ufo.png', tmpX, 0, 100, 100, tmpSpeed)
        enemigos.append(enemigo)

# fondos
background = transform.scale(image.load('galaxy.jpg'), (ANCHO, ALTO))

game_over = False
isLoser = False
starButton = False

while not game_over:

    for evento in event.get():
        if evento.type == QUIT:
            game_over = True
        if evento.type == KEYDOWN:
            if evento.key == K_SPACE and not isLoser:
                jugador.shoot()
            if evento.key == K_s:
                starButton = True
                generarEnemigos()

    pantalla.blit(background, (0, 0))

    # mostrar jugador
    
    if starButton:
        if not isLoser:
            jugador.reset()
            jugador.moves()
        else:
            setTextos('Perdiste', 50, coors= (ANCHO / 3, ALTO / 2), color = (217, 45, 11))

        # Mostrar Enemigos
        for enemy in enemigos:
            enemy.reset()
            enemy.moveDown()

            ## mostras balas
            for bullet in bullets:
                bullet.reset()
                bullet.moveUp()

                #Colision de Balas enemigos
                if bullet.isCollision(enemy):
                    if enemy in enemigos:
                        enemigos.remove(enemy)
                    if bullet in bullets:
                        bullets.remove(bullet)

            if enemy.isCollision(jugador):
                isLoser = True
                
        
    else:
        setTextos('Presione S para iniciar', 50, coors= (ANCHO / 3, ALTO / 2))


    # actualizar juego
    display.update()
    reloj.tick(FPS)