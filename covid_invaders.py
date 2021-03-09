import pygame, random, math

# screen/window initialiser with dimensions
pygame.init()
screen = pygame.display.set_mode((800, 1000))

# window title and icon
pygame.display.set_caption("Covid Invaders")
icon = pygame.image.load("images/logo1.png")
pygame.display.set_icon(icon)

# background top image
background = pygame.image.load("images/topimage.png")
imageX = 150
imageY = -125
imageX_change = 1
# background sound
pygame.mixer.music.load("soundtrack/Afterglow.mp3")
pygame.mixer.music.play(-1)

# player (injection) model
playerImg = pygame.image.load("images/injection.png")
playerX = 370
playerY = 890
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))        # function to attach the model

####  VIRUS 1  ####
virus1Img = []
virus1X = []
virus1Y = []
# controls the speed of the movement
virus1X_change = []
virus1Y_change = []
num_of_enemies1 = 6

for i in range(num_of_enemies1):
    virus1Img.append(pygame.image.load("images/virus1.png"))
    virus1X.append(random.randint(0, 736))
    virus1Y.append(random.randint(20, 100))
    # controls the speed of the movement
    virus1X_change.append(1)
    virus1Y_change.append(0.1)

def virus1(x, y, i):
    screen.blit(virus1Img[i], (x, y))     # function to attach the model

####  VIRUS 2  #####
virus2Img = []
virus2X = []
virus2Y = []
# controls the speed of the movement
virus2X_change = []
virus2Y_change = []
num_of_enemies2 = 14

for i in range(num_of_enemies2):
    virus2Img.append(pygame.image.load("images/virus2.png"))
    virus2X.append(random.randint(0, 736))
    virus2Y.append(random.randint(20, 100))
    # controls the speed of the movement
    virus2X_change.append(1.5)
    virus2Y_change.append(0.2)

def virus2(x, y, i):
    screen.blit(virus2Img[i], (x, y))     # function to attach the model


#### BULLET (BLOOD DROP) #####
bulletImg = pygame.image.load("images/blood.png")
bulletX = 0
bulletY = 900                        # select the option like the X point since you re moving the y axis as well
# controls the speed of the movement
bulletX_change = 0
bulletY_change = 18
bullet_state = "ready"               # ready = cant see the bullet on the screen. fire = bullet moving

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+56.5, y-16))

def isCollisionVirus1(virus1X, virus1Y, bulletX, bulletY):
    bulletXCorr = bulletX + 30       # correction for model position
    distance = math.sqrt((virus1X-bulletXCorr)**2 + (virus1Y-bulletY)**2)
    if distance <= 30:
        return True
    else: return False

def isCollisionVirus2(virus2X, virus2Y, bulletX, bulletY):
    bulletXCorr = bulletX + 45       # correction for model position
    distance = math.sqrt((virus2X-bulletXCorr)**2 + (virus2Y-bulletY)**2)
    if distance <= 18:
        return True
    else: return False

#### Score
score_value = 0
font = pygame.font.Font('font\Coronaviral.otf', 32)    # (name of font, size)
textX = 20
textY = 20

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

# game over func
game_over_font = pygame.font.Font('font\Coronaviral.otf', 64)    # (name of font, size)
lockdown_font = pygame.font.Font('font\Coronaviral.otf', 52)     # (name of font, size)
gameOver = False

def game_over():
    game_over_text1 = game_over_font.render("GAME OVER", True, (255,255,255))
    game_over_text2 = lockdown_font.render("THE WORLD IS IN LOCKDOWN", True, (255,255,255))
    screen.blit(game_over_text1, (250, 450))
    screen.blit(game_over_text2, (95, 510))
    gameOver = True


# to keep the loop running so the window doesnt close
running = True
while running:

    for event in pygame.event.get():
        # to close the window and quit the executions
        if event.type == pygame.QUIT:
            running = False

        # if any key is pressed, check whether its right or left or up or down
        if event.type == pygame.KEYDOWN:                      # if any key is pressed
            if event.key == pygame.K_LEFT:                    # if left key is pressed
                playerX_change = -8
            if event.key == pygame.K_RIGHT:                   # if right key is pressed
                playerX_change = 8
            if event.key == pygame.K_SPACE:                   # if space key is pressed
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:                        # if any key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_SPACE:
                bulletY = 900
                bullet_state = "ready"

    screen.fill((0, 0, 255))
    # adding movement of the background top image (for dramatic effects)
    if score_value > 12:
        imageX += imageX_change
        if imageX >= 204:
            imageX_change = -1
        if imageX <= 95:
            imageX_change = 1

    screen.blit(background, (imageX, imageY))

    # managing player movement
    playerX += playerX_change
    # for restricting player movement within bounds
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    # attaching the player model
    player(playerX, playerY)

    # virus1 movement
    for i in range(num_of_enemies1):
        virus1X[i] += virus1X_change[i]
        virus1Y[i] += virus1Y_change[i]
        if virus1X[i] <= 0:
            virus1X_change[i] = 1
        if virus1X[i] >= 736:
            virus1X_change[i] = -1

         # collision
        collisionVirus1 = isCollisionVirus1(virus1X[i], virus1Y[i], bulletX, bulletY)
        if collisionVirus1:
            bulletY = 900
            bullet_state = "ready"
            score_value += 1
            virus1X[i] = random.randint(0, 736)                                             # respawning
            virus1Y[i] = random.randint(25, 125)

        # game over
        if virus1Y[i] > 945:
            for j in range(num_of_enemies1):
                virus1X_change[j] = 0
                virus1Y_change[j] = 15
            for k in range(num_of_enemies2):
                virus2X_change[k] = 0
                virus2Y_change[k] = 15
            game_over()
            break

        virus1(virus1X[i], virus1Y[i], i)

    # virus2 movement
    for i in range(num_of_enemies2):
        virus2X[i] += virus2X_change[i]
        virus2Y[i] += virus2Y_change[i]
        if virus2X[i] <= 0:
            virus2X_change[i] = 1.5
        if virus2X[i] >= 768:
            virus2X_change[i] = -1.5

        # collision
        collisionVirus2 = isCollisionVirus2(virus2X[i], virus2Y[i], bulletX, bulletY)
        if collisionVirus2:
            bulletY = 900
            bullet_state = "ready"
            score_value += 1
            virus2X[i] = random.randint(0, 768)                                             # respawning
            virus2Y[i] = random.randint(25, 125)

        # game over
        if virus2Y[i] > 945:
            for j in range(num_of_enemies1):
                virus1X_change[j] = 0
                virus1Y_change[j] = 15
            for k in range(num_of_enemies2):
                virus2X_change[k] = 0
                virus2Y_change[k] = 15
            game_over()
            break

        virus2(virus2X[i], virus2Y[i], i)

    # bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # showing score
    show_score(textX, textY)

    # essential worker icons
    screen.blit(pygame.image.load("images/fireman.png"), (20, 947))
    screen.blit(pygame.image.load("images/worker3.png"), (560, 947))
    screen.blit(pygame.image.load("images/bus-driver.png"), (175, 947))
    screen.blit(pygame.image.load("images/doctor.png"), (100, 950))
    screen.blit(pygame.image.load("images/doctor1.png"), (140, 947))
    screen.blit(pygame.image.load("images/nurse.png"), (600, 947))
    screen.blit(pygame.image.load("images/coronavirus.png"), (500, 947))
    screen.blit(pygame.image.load("images/face-mask.png"), (-10, 947))
    screen.blit(pygame.image.load("images/hijab.png"), (720, 947))
    screen.blit(pygame.image.load("images/doctor2.png"), (745, 947))
    screen.blit(pygame.image.load("images/farmer.png"), (210, 947))
    screen.blit(pygame.image.load("images/worker.png"), (325, 947))
    screen.blit(pygame.image.load("images/constructor.png"), (395, 947))
    screen.blit(pygame.image.load("images/army.png"), (425, 947))
    screen.blit(pygame.image.load("images/doctor3.png"), (365, 947))
    screen.blit(pygame.image.load("images/farmer1.png"), (60, 947))
    screen.blit(pygame.image.load("images/pharmacist.png"), (255, 947))
    screen.blit(pygame.image.load("images/pharmacist1.png"), (295, 947))
    screen.blit(pygame.image.load("images/people.png"), (465, 947))
    screen.blit(pygame.image.load("images/worker2.png"), (525, 947))
    screen.blit(pygame.image.load("images/boss.png"), (640, 947))
    screen.blit(pygame.image.load("images/manager.png"), (685, 947))

    pygame.display.update()                   # to keep updating the window

