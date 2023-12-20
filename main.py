# A,D or arrow keys to move, Spacebar to shoot 

import pygame;
import random;
import math;
pygame.init()

screen = pygame.display.set_mode((800,600));
pygame.display.set_caption("Space Invaders");
icon = pygame.image.load('icon.png');
backdrop = pygame.image.load('newBg.jpg');
pygame.display.set_icon(icon);

playerImg = pygame.image.load('shuttle.png');
playerX = 370;
playerY = 500;
playerdx = 0;

enemyImg = pygame.image.load('enemy.png');
enemyY = [];
enemydy = 35;
num_enemies = 5;
enemyX = [];
enemydx = [];

for i in range(num_enemies) : 
    enemyX.append(random.randint(0,720));
    enemydx.append(random.uniform(0.3,0.7));
    enemyY.append(random.randint(50,150));

bulletImg = pygame.image.load('bullet.png');
bulletX = 0;
bulletY = 480;
bulletdx = 0.2;
bulletdy = 1;
bullet_state = 'ready';

# def player(x,y) : 
#     screen.blit(playerImg,(x,y));
def player() : 
    screen.blit(playerImg,(playerX,playerY));
    
def enemy(x,y,i) : 
    screen.blit(enemyImg,(x,y));
    
def fire_bullet(x,y) : 
    global bullet_state;
    bullet_state = 'fire';
    screen.blit(bulletImg,(x+16,y+10));
    
def hasCollided(x1,y1,x2,y2) : 
    dist = math.sqrt( math.pow( (x2-x1), 2 ) + math.pow( (y2-y1), 2 ) );
    return (dist <= 29);

score_val = 0;
font = pygame.font.Font('freesansbold.ttf',32);
tx = 10;
ty = 10;

def show_score(x,y) : 
    score = font.render("Score : " + str(score_val),True,(255,255,255));
    screen.blit(score,(x,y));

over_font = pygame.font.Font('freesansbold.ttf',64);    
def game_over() : 
    for j in range(num_enemies) : 
        enemyY[j] = 2000;
        enemydy = 0;
    over_text = over_font.render("GAME OVER",True,(255,255,255));
    screen.blit(over_text,(200,250));
    
#Game Loop : 
running = True;
while running : 
    screen.fill((19,19,19));
    screen.blit(backdrop,(0,0)); 
    
    for event in pygame.event.get() : 
        if event.type == pygame.QUIT : 
            running = False;
            
        if event.type == pygame.KEYDOWN : 
            if event.key == pygame.K_LEFT or event.key == pygame.K_a: 
                playerdx = -0.45;
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
                playerdx = 0.45;
            if event.key == pygame.K_SPACE and bullet_state == "ready" : 
                fire_bullet(playerX,bulletY);
                bulletX = playerX;
        
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_a :
                if playerdx == -0.33 : 
                    playerdx = 0;               
                            
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
                if playerdx == 0.33 : 
                    playerdx = 0; 
                
    if bulletY <= 0 : 
        bullet_state = 'ready';
        bulletY = 480;
    
    if playerX < 0 :
        playerX = 0;
    if playerX > 736  : 
        playerX = 736;
    playerX += playerdx;            

    for i in range(num_enemies) :   
        if enemyY[i] > 440 : 
            game_over();
            break;
        
        if enemyX[i] < 0 : 
            enemydx[i] = -1 * enemydx[i] ;
            enemyY[i] += enemydy;
        if enemyX[i] > 736  : 
            enemydx[i] = -1 * enemydx[i];
            enemyY[i] += enemydy;
        enemyX[i] += enemydx[i]; 
    
        if hasCollided(enemyX[i],enemyY[i],bulletX,bulletY) : 
            bulletY = 480;
            bullet_state = 'ready';
            score_val += 1;
            enemyX[i] = random.randint(0,720);
            enemyY[i] = random.randint(50,150);
        
        enemy(enemyX[i],enemyY[i],i);
    
    if bullet_state == 'fire' : 
        fire_bullet(bulletX,bulletY);
        bulletY -= bulletdy;
        
    show_score(tx,ty);
    
    player();
    # player(playerX,playerY);
    pygame.display.update();