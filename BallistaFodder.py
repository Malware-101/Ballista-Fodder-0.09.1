import pygame
import math
import random
pygame.init()
pygame.mixer.init()

Run = True
Pause = False
Mode = 0
tick = 0
Width = 1920
Height = 1080
Maplength = 100
Mapheight = 100
SpawnX = 64
SpawnY = 0
PlayerX = 64
PlayerY = 0
CamX = 960
CamY = Mapheight * 64 - 540
PlayerVX = 0
PlayerVY = 0
XSmooth = 0
block_num = 1
HP = 100
Reload = 0
Hand = 0
Void = False
Wall = False
SL = ""
Area = "C"
HitBlock = []
Hitbox = (0,0,0,0)
Move = (0,0)

LSize = (Maplength * 64,Mapheight * 64)
BackLevel = pygame.Surface(LSize,pygame.SRCALPHA)
FrontLevel = pygame.Surface(LSize,pygame.SRCALPHA)
screen = pygame.display.set_mode((Width,Height))
pygame.display.set_caption('Ballista Fodder')
clock = pygame.time.Clock()
font = pygame.font.SysFont('lucidaconsole', 60)

def Load_Textures(image,num):
    Sheet = []
    y = 0
    for i in range(math.ceil(num/8)):
        if i == math.ceil(num/8) - 1:
            row = num % 8
            if row == 0:
                row = 8
        else:
            row = 8
            
        x = 0
        for j in range(row):
            Sheet.append(image.subsurface((x,y,64,64)))
            x += 64
        y += 64
    return Sheet

class Block:
    def __init__(self,block,animation,full,background,var):
        self.block = block
        self.animation = animation
        self.full = full
        self.background = background
        self.var = var

class Entity:
    def __init__(self,entity,costume,position,hitbox,velocity,stage,health,reload,var):
        self.entity = entity
        self.costume = costume
        self.position = position
        self.hitbox = hitbox
        self.velocity = velocity
        self.stage = stage
        self.health = health
        self.reload = reload
        self.var = var

Lightingblock = pygame.image.load('Assets/images/blocks/Lighting.png').convert_alpha()

Barry = [pygame.image.load('Assets/images/Entities/Barry.R.png').convert_alpha()]

Blocks = [Block('Air',[0,pygame.image.load('Assets/images/blocks/Air.png')],False,True,[])]
Textures = Load_Textures(pygame.image.load('Assets/images/Functional_Sheet.png').convert_alpha(),17)
Blocks += [Block('Ice',[0,Textures[0]],True,True,[]),Block('Lava_Top',[0,Textures[1]],False,True,[]),Block('Lava',[0,Textures[2]],False,True,[]),
          Block('Water_Top',[0,Textures[3]],False,True,[]),Block('Water',[0,Textures[4]],False,True,[]),Block('Candle',[0,Textures[5]],False,True,[]),
          Block('Candle_Bunch',[0,Textures[6]],False,True,[]),Block('Lantern',[0,Textures[7]],False,True,[]),Block('Spike_Up',[0,Textures[8]],False,True,[]),
          Block('Spike_Down',[0,Textures[9]],False,True,[]),Block('Spike_Right',[0,Textures[10]],False,True,[]),Block('Spike_Left',[0,Textures[11]],False,True,[]),
          Block('Crumble_Stone',[0,Textures[12],Textures[13],Textures[14],Textures[15]],True,True,[]),Block('Spawn',[0,Textures[16]],True,True,[])]

Textures = Load_Textures(pygame.image.load('Assets/images/House_Sheet.png').convert_alpha(),64)
Blocks += [Block('Roof_Top_Left',[0,Textures[0]],True,True,[]),Block('Roof_Top_Middle',[0,Textures[1]],True,True,[]),Block('Roof_Top_Right',[0,Textures[2]],True,True,[]),
           Block('Potted_Plant',[0,Textures[3]],False,True,[]),Block('Hanging_Plant',[0,Textures[4]],False,True,[]),Block('Bathtub_Left',[0,Textures[5]],False,True,[]),
           Block('Bathtub_Right',[0,Textures[6]],False,True,[]),Block('Barrel',[0,Textures[7]],False,True,[]),Block('Roof_Middle_Left',[0,Textures[8]],True,True,[]),
           Block('Roof_Middle_Middle',[0,Textures[9]],True,True,[]),Block('Roof_Middle_Right',[0,Textures[10]],True,True,[]),Block('Roof_Bottom_Left',[0,Textures[16]],True,True,[]),
           Block('Roof_Bottom_Middle',[0,Textures[17]],True,True,[]),Block('Roof_Bottom_Right',[0,Textures[18]],True,True,[]),Block('Weather_Vane',[0,Textures[24]],False,True,[]),
           Block('Chimney',[0,Textures[25]],False,True,[]),Block('Roof_Weather_Vane',[0,Textures[32]],True,True,[]),Block('Roof_Chimney',[0,Textures[33]],True,True,[]),
           Block('Wall_Top_Left',[0,Textures[40]],False,True,[]),Block('Wall_Top_Middle',[0,Textures[41]],False,True,[]),Block('Wall_Top_Right',[0,Textures[42]],False,True,[]),
           Block('Wall_Column_Top',[0,Textures[43]],False,True,[]),Block('Wall_Slab',[0,Textures[44]],False,True,[]),Block('Wall_Slab_Bordered',[0,Textures[45]],False,True,[]),
           Block('Stair',[0,Textures[46]],True,True,[]),Block('Wall_Middle_Left',[0,Textures[48]],False,True,[]),Block('Wall_Middle_Middle',[0,Textures[49]],False,True,[]),
           Block('Wall_Middle_Right',[0,Textures[50]],False,True,[]),Block('Wall_Column_Middle',[0,Textures[51]],False,True,[]),Block('Doorway_Top',[0,Textures[52]],False,True,[]),
           Block('Door_Top',[0,Textures[53]],False,True,[]),Block('Stair_Bit',[0,Textures[54]],False,True,[]),Block('Wall_Bottom_Left',[0,Textures[56]],False,True,[]),
           Block('Wall_Bottom_Middle',[0,Textures[57]],False,True,[]),Block('Wall_Bottom_Right',[0,Textures[58]],False,True,[]),Block('Wall_Column_Bottom',[0,Textures[59]],False,True,[]),
           Block('Doorway_Bottom',[0,Textures[60]],False,True,[]),Block('Door_Bottom',[0,Textures[61]],False,True,[]),Block('Platform',[0,Textures[62]],False,True,[])]

Textures = Load_Textures(pygame.image.load('Assets/images/Nature_Sheet.png').convert_alpha(),64)
Blocks += [Block('Sky_Clear',[0,Textures[0]],False,True,[]),Block('Sky_Mountain_Right',[0,Textures[1]],False,True,[]),Block('Sky_Mountain',[0,Textures[8]],False,True,[]),
           Block('Sky_Mountain_Left',[0,Textures[9]],False,True,[]),Block('Sky_House',[0,Textures[10]],False,True,[]),Block('Sky_Trees',[0,Textures[11]],False,True,[]),
           Block('Grass_Short',[0,Textures[23]],False,True,[]),Block('Stone_Brick',[0,Textures[24]],True,True,[]),Block('Dirt_Grassy_Short',[0,Textures[31]],1,True,[]),
           Block('Dirt_Grassy',[0,Textures[39]],True,True,[]),Block('Stone_Brick_Top_Left',[0,Textures[40]],True,True,[]),Block('Stone_Brick_Top_Middle',[0,Textures[41]],True,True,[]),
           Block('Stone_Brick_Top_Right',[0,Textures[42]],True,True,[]),Block('Stone_1',[0,Textures[43]],True,True,[]),Block('Stone_Bricks',[0,Textures[44]],True,True,[]),
           Block('Wood_Pillar_Top',[0,Textures[46]],True,True,[]),Block('Dirt',[0,Textures[47]],True,True,[]),Block('Stone_Bricks_Middle_Left',[0,Textures[48]],True,True,[]),
           Block('Stone_Bricks_Middle_Middle',[0,Textures[49]],True,True,[]),Block('Stone_Bricks_Middle_Right',[0,Textures[50]],True,True,[]),Block('Stone_2',[0,Textures[51]],True,True,[]),
           Block('Wood_Pillar_Middle',[0,Textures[54]],True,True,[]),Block('Dirt_Transition',[0,Textures[55]],True,True,[]),Block('Stone_Bricks_Bottom_Left',[0,Textures[56]],True,True,[]),
           Block('Stone_Bricks_Bottom_Middle',[0,Textures[57]],True,True,[]),Block('Stone_Bricks_Bottom_Right',[0,Textures[58]],True,True,[]),Block('Stone_3',[0,Textures[59]],True,True,[]),
           Block('Stone_Slab',[0,Textures[60]],1,True,[]),Block('Stone_Stairs_Right',[0,Textures[61]],2,True,[]),Block('Wood_Pillar_Bottom',[0,Textures[62]],True,True,[]),
           Block('Dirt_Dark',[0,Textures[63]],True,True,[]),]

Entity_Textures = [[pygame.image.load('Assets/images/Entities/Arrow.png').convert_alpha()],
                    [pygame.image.load('Assets/images/Entities/Bouncer_1.png').convert_alpha(),pygame.image.load('Assets/images/Entities/Bouncer_2.png').convert_alpha(),pygame.image.load('Assets/images/Entities/Bouncer_3.png').convert_alpha(),pygame.image.load('Assets/images/Entities/Bouncer_4.png').convert_alpha()],
                    [pygame.image.load('Assets/images/Entities/Reefle_4.png').convert_alpha(),pygame.image.load('Assets/images/Entities/Reefle_5.png').convert_alpha(),pygame.image.load('Assets/images/Entities/Reefle_6.png').convert_alpha()],
                    [pygame.image.load('Assets/images/Entities/Ttahr.png').convert_alpha()]]

Weapons = [pygame.image.load('Assets/images/Weapons/Greatsword.png').convert_alpha(),pygame.image.load('Assets/images/Items/Bow.png').convert_alpha()]

Items = [[pygame.image.load('Assets/images/Items/Greatsword.png').convert_alpha(),1],[pygame.image.load('Assets/images/Weapons/Bow.png').convert_alpha(),2],
         [pygame.image.load('Assets/images/Items/Orange_Berry.png').convert_alpha(),0],[pygame.image.load('Assets/images/Items/Twig.png').convert_alpha(),0]]

UI = [pygame.image.load('Assets/images/UI/Title.png').convert_alpha(),pygame.image.load('Assets/images/UI/Inventory.png').convert_alpha(),
      pygame.image.load('Assets/images/UI/Button.png').convert(),pygame.image.load('Assets/images/UI/Slider-3.png').convert_alpha(),
      pygame.image.load('Assets/images/UI/Healthbar.png').convert_alpha(),pygame.image.load('Assets/images/UI/Health_Overlay.png').convert_alpha()]

MELON = pygame.mixer.Sound('Assets/sounds/melon_chop.wav')
PIPE = pygame.mixer.Sound('Assets/sounds/Metal Pipe.wav')
MELON.set_volume(500)
PIPE.set_volume(3000)
Variables = [False,False,False,False,120,False]
#mouselock,mouse,escape,idk,layerslider
Entities = []
SaveEntities = []
#types = [item,arrow,bouncer,reefle,croissant,baguette,roll,ttahr]

Inventory = [0,1,2,3]

Hitboxes = [[22,42,22,42],[4,60,20,63],[4,60,4,60],[4,60,32,54]]

Map = []
Background = []
Foreground = []

lighting = []
def Get_Lighting():
    global lighting
    sources = []
    for i in range(Maplength*Mapheight):
        if Blocks[Map[i]].block == 'Lantern':
            sources.append([i % Maplength,math.floor(i / Maplength)])
    lighting = []
    index = -1
    for i in range(Maplength*Mapheight):
        index += 1
        block_count = 0
        if Blocks[Map[index]].block != 'Lantern':
            Nindex = index - Maplength - 1
            if Nindex > 0:
                if Blocks[Map[Nindex]].full:
                    block_count += 1
            else:
                block_count += 1
            Nindex = index - Maplength
            
            if Nindex > 0:
                if Blocks[Map[Nindex]].full:
                    block_count += 1
            else:
                block_count += 1
            Nindex = index - Maplength + 1
            
            if Nindex > 0:
                if Blocks[Map[Nindex]].full:
                    block_count += 1
            else:
                block_count += 1
            Nindex = index - 1
            
            if Nindex > 0:
                if Blocks[Map[Nindex]].full:
                    block_count += 1
            else:
                block_count += 1
            Nindex = index + 1
            
            if Nindex < Maplength * Mapheight:
                if Blocks[Map[Nindex]].full:
                    block_count += 1
            else:
                block_count += 1
            Nindex = index + Maplength - 1
            
            if Nindex < Maplength * Mapheight:
                if Blocks[Map[Nindex]].full:
                    block_count += 1
            else:
                block_count += 1
            Nindex = index + Maplength
            
            if Nindex < Maplength * Mapheight:
                if Blocks[Map[Nindex]].full:
                    block_count += 1
            else:
                block_count += 1

            Nindex = index + Maplength + 1
            if Nindex < Maplength * Mapheight:
                if Blocks[Map[Nindex]].full:
                    block_count += 1
            else:
                block_count += 1
        if block_count == 8:
                lighting.append(-100)
        else:
            Nindex = -1
            brightness = 200
            for i in range(len(sources)):
                Nindex += 1
                if 50 + 20 * math.sqrt((((index % Maplength) - (sources[Nindex][0]))**2) + (((math.floor(index / Maplength) - (sources[Nindex][1]))**2))) < brightness:
                    brightness = 50 + 20 * math.sqrt(((index % Maplength) - (sources[Nindex][0]))**2 + (math.floor(index / Maplength) - (sources[Nindex][1]))**2)
            if Area == "A":
                lighting.append(0)
            else:
                lighting.append(brightness)

    for i in range(Maplength * Mapheight):
        block_count = 0
        if lighting[i] == -100:
            if i - Maplength - 1 > 0:
                if lighting[i - Maplength - 1] > -1:
                    block_count += 1
                    
            if i - Maplength > 0:
                if lighting[i - Maplength] > -1:
                    block_count += 1

            if i - Maplength + 1 > 0:
                if lighting[i - Maplength + 1] > -1:
                    block_count += 1

            if i - 1 > 0:
                if lighting[i - 1] > -1:
                    block_count += 1

            if i + 1 < Maplength * Mapheight:
                if lighting[i + 1] > -1:
                    block_count += 1

            if i + Maplength - 1 < Maplength * Mapheight:
                if lighting[i + Maplength - 1] > -1:
                    block_count += 1

            if i + Maplength < Maplength * Mapheight:
                if lighting[i + Maplength] > -1:
                    block_count += 1

            if i + Maplength + 1 < Maplength * Mapheight:
                if lighting[i + Maplength + 1] > -1:
                    block_count += 1
        
        if block_count > 0:
            lighting[i] = -30

    for i in range(Maplength * Mapheight):
        if lighting[i] == -30:
            lighting[i] = 200
    return lighting
    
def editor():
    
    mouse_pos = pygame.mouse.get_pos()
    index = math.floor((mouse_pos[0] + CamX - Width / 2) / 64) + Maplength * math.floor((mouse_pos[1] + CamY - Height / 2) / 64)

    mouse_buttons = pygame.mouse.get_pressed(num_buttons = 3)
    if mouse_buttons[0] == True:
        if block_num < len(Blocks):
            if Variables[4] == 0:
                if not block_num == Background[index]:
                    Blocks[block_num].animation[Blocks[block_num].animation[0] + 1].set_alpha(50)
                    Background[index] = block_num
                    BackLevel.blit(Blocks[block_num].animation[Blocks[block_num].animation[0] + 1],(index % Maplength * 64,math.floor(index / Maplength) * 64))
            elif Variables[4] == 120:
                if not block_num == Map[index]:
                    Map[index] = block_num
                    Blocks[block_num].animation[Blocks[block_num].animation[0] + 1].set_alpha(255)
                    BackLevel.blit(Blocks[block_num].animation[Blocks[block_num].animation[0] + 1],(index % Maplength * 64,math.floor(index / Maplength) * 64))
            else:
                if not block_num == Foreground[index]:
                    Foreground[index] = block_num
                    Blocks[block_num].animation[Blocks[block_num].animation[0] + 1].set_alpha(255)
                    FrontLevel.blit(Blocks[block_num].animation[Blocks[block_num].animation[0] + 1],(index % Maplength * 64,math.floor(index / Maplength) * 64))
        elif tick % 10 == 0:
            Entities.append(Entity(block_num - len(Blocks),0,[math.floor((mouse_pos[0] + CamX - Width / 2) / 64) * 64,math.floor((mouse_pos[1] + CamY - Height / 2) / 64) * 64,0],Hitboxes[block_num - len(Blocks)],[0,0],0,100,0,[]))
            Entities[len(Entities) - 1].hitbox = [Entities[len(Entities) - 1].hitbox[0] + Entities[len(Entities) - 1].position[0],Entities[len(Entities) - 1].hitbox[1] + Entities[len(Entities) - 1].position[0],Entities[len(Entities) - 1].hitbox[2] + Entities[len(Entities) - 1].position[1],Entities[len(Entities) - 1].hitbox[3] + Entities[len(Entities) - 1].position[1]]
            
            if Entities[len(Entities) - 1].entity == 2:
                Entities[len(Entities) - 1].velocity[0] = 4
                Entities[len(Entities) - 1].velocity[1] = 4
                
    if mouse_buttons[2] == True:
        Blocks[0].animation[1].set_alpha(255)
        if Variables[4] == 0:
            if Background[index] != 0:
                Background[index] = 0
                if Blocks[Map[index]].full == False:
                    BackLevel.blit(Blocks[0].animation[1],(index % Maplength * 64,math.floor(index / Maplength) * 64))
                    Blocks[Map[index]].animation[Blocks[Map[index]].animation[0] + 1].set_alpha(lighting[index])
                    BackLevel.blit(Blocks[Map[index]].animation[Blocks[Map[index]].animation[0] + 1],(index % Maplength * 64,math.floor(index / Maplength) * 64))
        elif Variables[4] == 120:
            if Map[index] != 0:
                Map[index] = 0
                BackLevel.blit(Blocks[0].animation[1],(index % Maplength * 64,math.floor(index / Maplength) * 64))
                Blocks[Background[index]].animation[Blocks[Background[index]].animation[0] + 1].set_alpha(50)
                BackLevel.blit(Blocks[Background[index]].animation[Blocks[Background[index]].animation[0] + 1],(index % Maplength * 64,math.floor(index / Maplength) * 64))
        else:
            if Foreground[index] != 0:
                Foreground[index] = 0
                FrontLevel.blit(Blocks[0].animation[1],(index % Maplength * 64,math.floor(index / Maplength) * 64))
        
    if block_num < len(Blocks):
        Blocks[block_num].animation[Blocks[block_num].animation[0] + 1].set_alpha(125)
        screen.blit(Blocks[block_num].animation[Blocks[block_num].animation[0] + 1],(64 * (index % Maplength) - CamX + Width / 2,64 * math.floor(index / Maplength) - CamY + Height / 2))
    else:
        Entity_Textures[block_num - len(Blocks)][0].set_alpha(125)
        screen.blit(Entity_Textures[block_num - len(Blocks)][0],(64 * (index % Maplength) - CamX + Width / 2,64 * math.floor(index / Maplength) - CamY + Height / 2))

def game_tick():
    
    global CamX
    global CamY
    global SpawnX
    global SpawnY
    global PlayerX
    global PlayerY
    global PlayerVX
    global PlayerVY
    global Entities
    global HP
    global Reload
    global Move
    global Hitbox
    
    if Mode > 1:
        Reload -= 1
        if tick % 30 == 0:
            if HP < 100:
                HP += 1
    
        PlayerVY += 1
        OldPlayerVY = PlayerVY
        Hitbox = (16 + PlayerX,48 + PlayerX,12 + PlayerY,63 + PlayerY)
        Move = [PlayerVX,PlayerVY]
        trymove()
        PlayerX += Move[0]
        PlayerY += Move[1]
        
        if Wall and HitBlock[0] != 47 and HitBlock[1] != 47:
            PlayerVX = 0
        if Move[1] != PlayerVY:
            PlayerVY = 0
        if (Blocks[HitBlock[0]].block in ('Water_Top','Water','Lava_Top','Lava') or Blocks[HitBlock[1]].block in ('Water_Top','Water','Lava_Top','Lava')):
            if PlayerVY > 0:
                PlayerVY -= 0.75
            if PlayerVY > 4:
                PlayerVY -= 1
            if PlayerVY < -8:
                PlayerVY += 0.5
            if PlayerVX < -4:
                PlayerVX += 4
            if PlayerVX > 4:
                PlayerVX -= 4

        if Void:
            PlayerX = SpawnX
            PlayerY = SpawnY
            HP -= 9999
        
        index = math.floor((Hitbox[0] / 64) + Maplength * math.floor(Hitbox[3] / 64))
        index2 = math.floor((Hitbox[1] / 64) + Maplength * math.floor(Hitbox[3] / 64))
        index3 = math.floor((Hitbox[0] / 64) + Maplength * math.floor(Hitbox[2] / 64))
        index4 = math.floor((Hitbox[1] / 64) + Maplength * math.floor(Hitbox[2] / 64))
        
        if 10 < Map[index] < 15 or 10 < Map[index2] < 15 or 10 < Map[index3] < 15 or 10 < Map[index4] < 15:
            HP -= 100

        #if HP < 0:
        #    PlayerX = SpawnX
        #    PlayerY = SpawnY
        #    HP = 100
        
        if Map[math.floor((Hitbox[0] / 64) + Maplength * math.floor((Hitbox[3] + 16) / 64))] == 39:
            SpawnX = math.floor(PlayerX / 64) * 64
            SpawnY = math.floor(PlayerY / 64) * 64
        
                #PlayerVY = 0 - abs(PlayerVX)
        #if PlayerVY == 0 and OldPlayerVY > 30:
        #PlayerVY = 0 - math.floor(OldPlayerVY / 3)
        
        entity_index = -1
        while entity_index < len(Entities) - 1 and len(Entities) != 0:

            entity_index += 1
            
            if Entities[entity_index].entity == "ITEM":
                #ITEM
                if Entities[entity_index].stage == 0:
                    Entities[entity_index].velocity[1] += 1
            
            if Entities[entity_index].entity == 0:
                #arrow
                if Entities[entity_index].stage == 0:
                    Entities[entity_index].velocity[1] += 1

                    Hitbox = (Entities[entity_index].hitbox)

                    for i in range(len(Entities)):
                        if Entities[i].entity != 0:
                            if Hitbox[1] > Entities[i].hitbox[0] and Entities[i].hitbox[1] > Hitbox[0] and Hitbox[3] > Entities[i].hitbox[2] and Entities[i].hitbox[3] > Hitbox[2]:
                                Entities[i].health -= 100
                                Entities[entity_index].health -= 1
                                Entities[entity_index].stage = 1
                    
                    Move = [Entities[entity_index].velocity[0],Entities[entity_index].velocity[1]]
                    trymove()
                    Entities[entity_index].position[0] += Move[0]
                    Entities[entity_index].position[1] += Move[1]
                    Entities[entity_index].hitbox[0] += Move[0]
                    Entities[entity_index].hitbox[1] += Move[0]
                    Entities[entity_index].hitbox[2] += Move[1]
                    Entities[entity_index].hitbox[3] += Move[1]

                    if Wall:
                        Entities[entity_index].position[0] = Entities[entity_index].position[0] + math.sin(Entities[entity_index].position[2]) * 8
                        Entities[entity_index].position[1] = Entities[entity_index].position[1] + math.cos(Entities[entity_index].position[2]) * 8
                        Entities[entity_index].stage = 1
                        if random.randint(0,1) == 0:
                            MELON.play()
                        else:
                            PIPE.play()
                    if Entities[entity_index].stage == 0:
                        if Entities[entity_index].velocity[0] != 0:
                            theta = 360 - math.atan(Entities[entity_index].velocity[1] / Entities[entity_index].velocity[0]) * 57.29
                            if Entities[entity_index].velocity[0] < 0:
                                theta += 180
                        else:
                            if Entities[entity_index].velocity[1] > 0:
                                theta = 90
                            else:
                                theta = -90

                        Entities[entity_index].position[2] = theta
            
            if Entities[entity_index].entity == 1:
                #Bouncer
                Entities[entity_index].velocity[1] += 1
                Entities[entity_index].reload -= 1
                Hitbox = (Entities[entity_index].hitbox)
                Move = [Entities[entity_index].velocity[0],Entities[entity_index].velocity[1]]
                trymove()
                Entities[entity_index].position[0] += Move[0]
                Entities[entity_index].position[1] += Move[1]
                Entities[entity_index].hitbox[0] += Move[0]
                Entities[entity_index].hitbox[1] += Move[0]
                Entities[entity_index].hitbox[2] += Move[1]
                Entities[entity_index].hitbox[3] += Move[1]
                
                if Wall:
                    if Move[0] != Entities[entity_index].velocity[0]:
                        Entities[entity_index].velocity[0] = Move[0]
                    if Move[1] != Entities[entity_index].velocity[1]:
                        Entities[entity_index].velocity[1] = Move[1]
                
                if Entities[entity_index].reload < 0 and Entities[entity_index].stage == 0:
                    if random.randint(0,3) == 0:
                        Entities[entity_index].stage = 1
                    else:
                        Entities[entity_index].stage = 3
                        Entities[entity_index].velocity[1] -= random.randint(12,24)
                        Entities[entity_index].velocity[0] = random.randint(-10,10)
                if Entities[entity_index].stage == 1:
                    if Entities[entity_index].reload < 0 and Entities[entity_index].costume < 3:
                        Entities[entity_index].reload = 9
                        Entities[entity_index].costume += 1
                        if Entities[entity_index].costume == 3:
                            Entities[entity_index].reload = random.randint(240,600)
                    elif Entities[entity_index].reload < 0 and Entities[entity_index].costume == 3:
                        Entities[entity_index].stage = 2
                if Entities[entity_index].stage == 2:
                    if Entities[entity_index].reload < 0 and Entities[entity_index].costume > 0:
                        Entities[entity_index].reload = 9
                        Entities[entity_index].costume -= 1
                        if Entities[entity_index].costume == 0:
                            Entities[entity_index].reload = random.randint(30,180)
                            Entities[entity_index].stage = 0
                if Entities[entity_index].stage == 3 and Entities[entity_index].reload < -2 and Wall:
                    Entities[entity_index].velocity[0] = 0
                    Entities[entity_index].stage = 0
                    Entities[entity_index].reload = random.randint(30,180)

            if Entities[entity_index].entity == 2:
                #Reefle
                Hitbox = (Entities[entity_index].hitbox)
                Move = [Entities[entity_index].velocity[0],Entities[entity_index].velocity[1]]
                trymove()
                Entities[entity_index].position[0] += Move[0]
                Entities[entity_index].position[1] += Move[1]
                Entities[entity_index].hitbox[0] += Move[0]
                Entities[entity_index].hitbox[1] += Move[0]
                Entities[entity_index].hitbox[2] += Move[1]
                Entities[entity_index].hitbox[3] += Move[1]
                if Wall:
                    if Move[0] != Entities[entity_index].velocity[0]:
                        Entities[entity_index].velocity[0] *= -1
                    if Move[1] != Entities[entity_index].velocity[1]:
                        Entities[entity_index].velocity[1] *= -1
                Entities[entity_index].costume += 1
                if Entities[entity_index].costume == 3:
                    Entities[entity_index].costume = 0
            if Void:
                Entities[entity_index].health -= 9999

            if Entities[entity_index].health < 0:
                Entities.pop(entity_index)
                entity_index -= 1

        CamX = PlayerX
        CamY = PlayerY
    if CamX < Width / 2:
        CamX = Width / 2
    if CamY < Height / 2:
        CamY = Height / 2
    if CamX > Maplength * 64 - Width / 2:
        CamX = Maplength * 64 - Width / 2
    if CamY > Mapheight * 64 - Height / 2:
        CamY = Mapheight * 64 - Height / 2

    if HP < 0:
            PlayerX = SpawnX
            PlayerY = SpawnY
            HP = 100
    
    return Hitbox
    return CamX
    return CamY
    return SpawnX
    return SpawnY
    return PlayerX
    return PlayerY
    return PlayerVX
    return PlayerVY
    return Entities
    return HP
    return Reload
    return Move

def trymove():
    global Wall
    global Void
    global Move
    global HitBlock
    
    HitBlock = [0,0]
    Void = False
    index = math.floor(((Hitbox[1] + Move[0]) / 64) + Maplength * math.floor((Hitbox[2]) / 64))
    index2 = math.floor(((Hitbox[1] + Move[0]) / 64) + Maplength * math.floor((Hitbox[3]) / 64))
    index3 = math.floor(((Hitbox[0] + Move[0]) / 64) + Maplength * math.floor((Hitbox[2] + Move[1]) / 64))
    index4 = math.floor(((Hitbox[1] + Move[0]) / 64) + Maplength * math.floor((Hitbox[2] + Move[1]) / 64))
    if index + Maplength > len(Map) or index2 + Maplength > len(Map) or index3 < 0 or index4 < 0:
        Void = True
        Move = [0,0]

    Wall = False
    if Move[0] > 0:
        index = math.floor(((Hitbox[1] + Move[0]) / 64) + Maplength * math.floor((Hitbox[2]) / 64))
        index2 = math.floor(((Hitbox[1] + Move[0]) / 64) + Maplength * math.floor((Hitbox[3]) / 64))
        HitBlock = [Map[index],Map[index2]]
        if Blocks[Map[index]].full == True or Blocks[Map[index2]].full == True:
            Wall = True
            while Blocks[Map[index]].full == True or Blocks[Map[index2]].full == True:
                Move[0] -= 1
                index = math.floor(((Hitbox[1] + Move[0]) / 64) + Maplength * math.floor((Hitbox[2]) / 64))
                index2 = math.floor(((Hitbox[1] + Move[0]) / 64) + Maplength * math.floor((Hitbox[3]) / 64))
                HitBlock = [Map[index],Map[index2]]
    else:
        index = math.floor(((Hitbox[0] + Move[0]) / 64) + Maplength * math.floor((Hitbox[2]) / 64))
        index2 = math.floor(((Hitbox[0] + Move[0]) / 64) + Maplength * math.floor((Hitbox[3]) / 64))
        HitBlock = [Map[index],Map[index2]]
        if Blocks[Map[index]].full == True or Blocks[Map[index2]].full == True:
            Wall = True
            while Blocks[Map[index]].full == True or Blocks[Map[index2]].full == True:
                Move[0] += 1
                index = math.floor(((Hitbox[0] + Move[0]) / 64) + Maplength * math.floor((Hitbox[2]) / 64))
                index2 = math.floor(((Hitbox[0] + Move[0]) / 64) + Maplength * math.floor((Hitbox[3]) / 64))
                HitBlock = [Map[index],Map[index2]]
    if Move[1] > 0:
        index = math.floor(((Hitbox[0] + Move[0]) / 64) + Maplength * math.floor((Hitbox[3] + Move[1]) / 64))
        index2 = math.floor(((Hitbox[1] + Move[0]) / 64) + Maplength * math.floor((Hitbox[3] + Move[1]) / 64))
        HitBlock = [Map[index],Map[index2]]
        if Blocks[Map[index]].full == True or Blocks[Map[index2]].full == True:
            Wall = True
            while Blocks[Map[index]].full == True or Blocks[Map[index2]].full == True:
                Move[1] -= 1
                index = math.floor(((Hitbox[0] + Move[0]) / 64) + Maplength * math.floor((Hitbox[3] + Move[1]) / 64))
                index2 = math.floor(((Hitbox[1] + Move[0]) / 64) + Maplength * math.floor((Hitbox[3] + Move[1]) / 64))
                HitBlock = [Map[index],Map[index2]]
    else:
        index = math.floor(((Hitbox[0] + Move[0]) / 64) + Maplength * math.floor((Hitbox[2] + Move[1]) / 64))
        index2 = math.floor(((Hitbox[1] + Move[0]) / 64) + Maplength * math.floor((Hitbox[2] + Move[1]) / 64))
        HitBlock = [Map[index],Map[index2]]
        if Blocks[Map[index]].full == True or Blocks[Map[index2]].full == True:
            Wall = True
            while Blocks[Map[index]].full == True or Blocks[Map[index2]].full == True:
                Move[1] += 1
                index = math.floor(((Hitbox[0] + Move[0]) / 64) + Maplength * math.floor((Hitbox[2] + Move[1]) / 64))
                index2 = math.floor(((Hitbox[1] + Move[0]) / 64) + Maplength * math.floor((Hitbox[2] + Move[1]) / 64))
                HitBlock = [Map[index],Map[index2]]
    
    return Wall
    return Void
    return Move
    return HitBlock

def game_display():

    if Area == "A":
        screen.fill((90,235,255))
    else:
        screen.fill('black')

    PenX = 0
    PenY = 0

    screen.blit(BackLevel,(Width / 2 - CamX,Height / 2 - CamY))

    costume_num = 0
    screen.blit(Barry[costume_num],(PlayerX - CamX + Width / 2,PlayerY - CamY + Height / 2))

    if Items[Inventory[Hand]][1] != 0:
        screen.blit(Weapons[Items[Inventory[Hand]][1] - 1],(PlayerX - CamX + Width / 2,PlayerY - CamY + Height / 2))

    index = -1
    for i in range(len(Entities)):
        index += 1
        if Entities[index].position[0] - CamX + Width / 2 < Width and Entities[index].position[1] - CamY + Height / 2 < Height:
            Rotated = pygame.transform.rotate(Entity_Textures[Entities[index].entity][Entities[index].costume],Entities[index].position[2])
            Rotated.set_alpha(255)
            screen.blit(Rotated,(Entities[index].position[0] - CamX + Width / 2,Entities[index].position[1] - CamY + Height / 2))

    screen.blit(FrontLevel,(Width / 2 - CamX,Height / 2 - CamY))

    if Mode == 1 or Mode == 2:
        UI[2] = pygame.transform.scale(UI[2],(Width * 0.1,Height * 0.05))
        screen.blit(UI[2],(Width * 0.9, 0))
        font = pygame.font.SysFont('lucidaconsole', 20)
        text = font.render('Test', False, (255, 255, 255))
        screen.blit(text,(Width * 0.95,Height * 0.01))
        screen.blit(UI[2],(Width * 0.9,Height * 0.95))
        text = font.render('Save/Load', False, (255, 255, 255))
        screen.blit(text,(Width * 0.92,Height * 0.96))

    if Mode == 1:
        screen.blit(UI[3],(0,0))
        screen.blit(Entity_Textures[3][0],(Variables[4],8))
        
        
    if Mode > 1:
        screen.blit(UI[1],(-16,-16))
        
        if len(Inventory) < 6:
            for i in range(len(Inventory)):
                screen.blit(Items[Inventory[i]][0],(16 + i * 80,16))
        else:
            for i in range(5):
                screen.blit(Items[Inventory[i]][0],(16 + i * 80,16))

        R = 488 - 4.88 * HP
        G = 4.88 * HP
        if R > 255:
            R = 255
        if G > 255:
            G = 255

        screen.blit(UI[4],(-16,96))
        screen.blit(UI[5],(-24,92))
        pygame.draw.rect(screen, (255,255,0), pygame.Rect(Hand * 84, 92, 84, 5))
    
def Render_Level():
    BackLevel.fill((0,0,0,0))
    FrontLevel.fill((0,0,0,0))
    
    PenY = 0
    index = 0
    for i in range(Mapheight):
        PenX = 0
        for j in range(Maplength):

            if Background[index] != 0 and Foreground[index] < 25:
                Blocks[Background[index]].animation[Blocks[Background[index]].animation[0] + 1].set_alpha(50)
                BackLevel.blit(Blocks[Background[index]].animation[Blocks[Background[index]].animation[0] + 1],(PenX,PenY))
            
            if Map[index] != 0:
                Blocks[Map[index]].animation[Blocks[Map[index]].animation[0] + 1].set_alpha(255)
                if Blocks[Map[index]].background:
                    BackLevel.blit(Blocks[Map[index]].animation[Blocks[Map[index]].animation[0] + 1],(PenX,PenY))
                else:
                    FrontLevel.blit(Blocks[Map[index]].animation[Blocks[Map[index]].animation[0] + 1],(PenX,PenY))
                
            if Foreground[index] != 0:
                Blocks[Foreground[index]].animation[Blocks[Foreground[index]].animation[0] + 1].set_alpha(255)
                FrontLevel.blit(Blocks[Foreground[index]].animation[Blocks[Foreground[index]].animation[0] + 1],(PenX,PenY))
            
            if lighting[index] != -100:
                Lightingblock.set_alpha(lighting[index])
            else:
                Lightingblock.set_alpha(255)
            if Mode == 1:
                Lightingblock.set_alpha(0)
            FrontLevel.blit(Lightingblock,(PenX,PenY))
            
            PenX += 64
            index += 1
        PenY += 64
    
def player_controls():
    global Pause
    global PlayerX
    global PlayerY
    global PlayerVX
    global PlayerVY
    global XSmooth
    global block_num
    global Mode
    global CamX
    global CamY
    global Reload
    global Barry
    global Blocks
    global Entity_Textures
    global Weapons
    global UI
    global Entities
    global SaveEntities
    global Variables
    global Hand
    global SL
    
    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed(num_buttons = 3)
    mouse_pos = pygame.mouse.get_pos()

    if not mouse_buttons[0]:
        Variables[0] = False

    if not Pause:
        if keys[pygame.K_1]:
            Hand = 0
        elif keys[pygame.K_2]:
            Hand = 1
        elif keys[pygame.K_3]:
            Hand = 2
        elif keys[pygame.K_4]:
            Hand = 3
        elif keys[pygame.K_5]:
            Hand = 4

        if Mode == 1:
            if keys[pygame.K_LSHIFT]:
                if keys[pygame.K_w]:
                    CamY -= 12
            
                if keys[pygame.K_a]:
                    CamX -= 12
            
                if keys[pygame.K_s]:
                    CamY += 12
            
                if keys[pygame.K_d]:
                    CamX += 12
            else:
                if keys[pygame.K_w]:
                    CamY -= 4
            
                if keys[pygame.K_a]:
                    CamX -= 4
            
                if keys[pygame.K_s]:
                    CamY += 4
            
                if keys[pygame.K_d]:
                    CamX += 4
        
            if keys[pygame.K_RIGHT]:
                if tick % 5 == 0:
                    block_num += 1
                    if block_num == len(Blocks) + len(Entity_Textures):
                        block_num = 1
        
            if keys[pygame.K_LEFT]:
                if tick % 5 == 0:
                    block_num -= 1
                    if block_num < 1:
                        block_num = len(Blocks) + len(Entity_Textures) - 1

        if Mode > 1:
            if keys[pygame.K_d]:
                PlayerVX = XSmooth + 1
                if PlayerVX > 8:
                    PlayerVX = 8
    
            if keys[pygame.K_a]:
                PlayerVX = XSmooth - 1
                if PlayerVX < -8:
                    PlayerVX = -8

            if not keys[pygame.K_d] and not keys[pygame.K_a]:
                if abs(XSmooth) < 1:
                    XSmooth = 0
                if XSmooth > 0:
                    PlayerVX = XSmooth - 1
                if XSmooth < 0:
                    PlayerVX = XSmooth + 1

            XSmooth = PlayerVX

            if keys[pygame.K_SPACE]:
                if PlayerVY == 0:
                    index = math.floor((PlayerX + 48) / 64) + Maplength * math.floor((PlayerY + 68) / 64)
                    index2 = math.floor((PlayerX + 16) / 64) + Maplength * math.floor((PlayerY + 68) / 64)
                    if Blocks[Map[index]].full == True or Blocks[Map[index2]].full == True:
                        PlayerVY = -21
                if PlayerVY > 3:
                    index = math.floor((PlayerX + 48) / 64) + Maplength * math.floor((PlayerY + 68) / 64)
                    index2 = math.floor((PlayerX + 16) / 64) + Maplength * math.floor((PlayerY + 68) / 64)
                    if Blocks[Map[index]].block in ('Water_Top','Water','Lava_Top','Lava') or Blocks[Map[index2]].block in ('Water_Top','Water','Lava_Top','Lava'):
                        PlayerVY = -16

            xdiff = (PlayerX - CamX + (Width / 2)) - mouse_pos[0]
            ydiff = (PlayerY - CamY + (Height / 2)) - mouse_pos[1]
            if mouse_buttons[0]:
                if Inventory[Hand] == 1:
                    if Reload < 0:
                        Reload = 20
                        if xdiff == 0:
                            if ydiff > 0:
                                theta = 90
                            else:
                                theta = -90
                        else:
                            theta = math.atan(ydiff / xdiff)
                        if xdiff < 0:
                            theta += 3.1415
                        Entities.append(Entity(0,0,[PlayerX,PlayerY,theta],[22 + PlayerX,42 + PlayerX,22 + PlayerY,42 + PlayerY],[-30 * math.cos(theta),-30 * math.sin(theta)],0,0,0,[]))

        if Mode == 1:
            if mouse_buttons[0] and mouse_pos[0] < 256 and mouse_pos[1] < 96:
                Variables[0] = True
                Variables[4] = 120 * math.floor((mouse_pos[0] + 64) / 128)
            if keys[pygame.K_e]:
                block_num = Map[math.floor((mouse_pos[0] + CamX - Width / 2) / 64) + Maplength * math.floor((mouse_pos[1] + CamY - Height / 2) / 64)]
    
    if Mode == 1 or Mode == 2:
        if keys[pygame.K_ESCAPE] and not Variables[2]:
            Pause = not Pause
        if mouse_buttons[0] and not Variables[1]:
            if mouse_pos[0] > Width * 0.9 and mouse_pos[1] < Height * 0.05:
                Variables[0] = True
                if Mode == 1:
                    SaveEntities = Entities
                    #pygame.mixer.music.play()
                    Mode = 2
                    for i in range(len(Map)):
                        if Map[i] == 39:
                            PlayerX = (i % Maplength) * 64
                            PlayerY = (math.ceil(i / Maplength) - 2) * 64
                else:
                    Mode = 1
                    Entities = SaveEntities
                Get_Lighting()
                Render_Level()
            
            if mouse_pos[0] > Width * 0.9 and mouse_pos[1] > Height * 0.95:
                Variables[0] = True
                SL = input("[S]ave or [L]oad?").upper()
                while SL != "S" and SL != "L":
                    print("Invalid Entry")
                    SL = input("[S]ave or [L]oad?").upper()
                Save_Load_New()

    Variables[1] = mouse_buttons[0]
    Variables[2] = keys[pygame.K_ESCAPE]

    return Pause
    return Mode
    return PlayerX
    return PlayerY
    return PlayerVX
    return PlayerVY
    return XSmooth
    return block_num
    return CamX
    return CamY
    return Reload
    return Barry
    return Blocks
    return Entity_Textures
    return Weapons
    return UI
    return Entities
    return SaveEntities
    return Variables
    return Hand
    return SL

def Save_Load_New():
    global Background
    global Map
    global Foreground
    global SL
    global Maplength
    global Mapheight
    global SpawnY
    global PlayerY
    global Area

    if SL == "S":
        filename = input("Save as:")
        with open(filename, "w") as file:
            file.write(str(Maplength) + "," + str(Mapheight))
            file.write(str(Background))
            file.write(str(Map))
            file.write(str(Foreground))
                        
    if SL == "L":
        filename = input("Load:")
        Entities = []
        Background = []
        Map = []
        Foreground = []          
        with open(filename) as file:
            Maps = file.readline().split('[')

            Maplength = int(Maps[0].split(',')[0])
            Mapheight = int(Maps[0].split(',')[1])
            
            Background = (Maps[1][:-1].split(','))
            for i in range(len(Background)):
                Background[i] = int(Background[i])
                            
            Map = Maps[2][:-1].split(',')
            for i in range(len(Map)):
                Map[i] = int(Map[i])
                            
            Foreground = Maps[3][:-1].split(',')
            for i in range(len(Foreground)):
                Foreground[i] = int(Foreground[i])
        Get_Lighting()
        Render_Level()

    if SL == "N":
        Background = []
        Map = []
        Foreground = []

        Area = input("[C]aves,[A]boveground").upper()
        while Area != "C" and Area != "A":
            print("Invalid Entry")
            Area = input("[C]aves,[A]boveground").upper()
        
        Maplength = int(input("Input Map Length"))
        while not isinstance(Maplength,int) and Maplength > 0:
            print("Input Natural Number")
            Maplength = int(input("Input Map Length"))
        
        Mapheight = int(input("Input Map Height"))
        while not isinstance(Mapheight,int) and Mapheight > 0:
            print("Input Natural Number")
            Mapheight = int(input("Input Map Height"))

        if Area == "C":
            for i in range(Maplength * Mapheight):
                Background.append(14)
                if random.randint(0,4) == 0:
                    Map.append(13)
                else:
                    Map.append(13)
                Foreground.append(0)

            
        elif Area == "A":
            for i in range(Maplength * math.ceil((Mapheight / 2) - 1)):
                Background.append(0)
                Map.append(0)
                Foreground.append(0)
            for i in range(Maplength):
                Background.append(14)
                Map.append(13)
                Foreground.append(0)
            for i in range(Maplength * (math.floor(Mapheight / 4))):
                Background.append(14)
                Map.append(13)
                Foreground.append(0)
            for i in range(Maplength * (math.ceil(Mapheight / 4))):
                Background.append(14)
                if random.randint(0,4) == 0:
                    Map.append(13)
                else:
                    Map.append(13)
                Foreground.append(0)
    
    SpawnY = Mapheight * 64 - 128
    PlayerY = SpawnY
    
    return Background
    return Map
    return Foreground
    return SL
    return Maplength
    return Mapheight
    return SpawnY
    return PlayerY
    return Area
    
while Run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            Run = False

    if Mode == 0:
        screen.fill("black")
        #UI[0] = pygame.transform.scale(UI[0],(Width * 0.3,Height * 0.25))
        #screen.blit(UI[0],(Width * 0.05, Height * 0.1))
        UI[2] = pygame.transform.scale(UI[2],(Width * 0.25,Height * 0.1))
        screen.blit(UI[2],(Width * 0.05, Height * 0.5))
        #pygame.draw.rect(screen, (20,20,20), pygame.Rect(Width * 0.05, Height * 0.5, Width * 0.25, Height * 0.10))
        text = font.render('Level Editor', False, (255, 255, 255))
        screen.blit(text,(Width * 0.075,Height * 0.525))
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed(num_buttons = 3)
        if Width * 0.30 > mouse_pos[0] > Width * 0.05 and Height * 0.6 > mouse_pos[1] > Height * 0.5:
            if mouse_buttons[0]:
                Mode = 1
                Variables[0] = True
                SL = input("[N]ew Level or [L]oad Level?").upper()
                while SL != "N" and SL != "L":
                    print("Invalid Entry")
                    SL = input("[N]ew Level or [L]oad Level?").upper()
                Save_Load_New()
                Get_Lighting()
                Render_Level()

    if Mode > 0:
        if not Pause:
            game_tick()
        
        game_display()
        
        player_controls()

    if Mode == 1:
        if not Variables[0] and not Pause:
            editor()
        
    clock.tick(60)
    tick += 1

    pygame.display.flip()

pygame.quit()
