import random
import pygame as pg
import json
from enemy import Enemy
from world import World
from tower import Tower
from button import Button
import event_cards as e
import constants as c

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL,c.SCREEN_HEIGHT))
pg.display.set_caption("Goobers vs Gobbers")

game_over = False
game_outcome = 0
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_towers = False
selected_tower = None

map_image = pg.image.load('images/goobersvsgoobbers1.png').convert_alpha()

tower_sheet = pg.image.load('images/towers1.png').convert_alpha()

cursor_tower = pg.image.load('images/tower_1.png')

enemy_images = {
   "weak": pg.image.load('images/redenemy.png').convert_alpha(),
   "medium": pg.image.load('images/blueenemy.png').convert_alpha(),
   "strong": pg.image.load('images/purpleenemy.png').convert_alpha(),
}
enemy_image = pg.image.load('images/redenemy.png').convert_alpha()

buy_tower_image = pg.image.load('images/buy_tower.png').convert_alpha()
cancel_image = pg.image.load('images/cancel.png').convert_alpha()
upgrade_image = pg.image.load('images/upgrade.png').convert_alpha()
start_image = pg.image.load('images/start.png').convert_alpha()
restart_image = pg.image.load('images/restart.png').convert_alpha()
bread_image = pg.image.load('images/bread.png').convert_alpha()
heart_image = pg.image.load('images/heart.png').convert_alpha()
logo_image = pg.image.load('images/logo.png').convert_alpha()
draw_cards_image = pg.image.load('images/draw_cards.png')
with open('goobersvsgoobbers1.tmj') as file:
    world_data = json.load(file)

text_font = pg.font.SysFont("Consolas",12,bold=True)
large_font = pg.font.SysFont("Consolas",18)

def draw_text(text,font,text_col,x,y):
   img = font.render(text,True,text_col)
   screen.blit(img,(x,y))
def display_data():
    pg.draw.rect(screen,"maroon",(c.SCREEN_WIDTH,0,c.SIDE_PANEL,c.SCREEN_HEIGHT))
    pg.draw.rect(screen,"grey0",(c.SCREEN_WIDTH,0,c.SIDE_PANEL,150),2)
    screen.blit(logo_image, (c.SCREEN_WIDTH, 150))
    draw_text("LEVEL: "+str(world.level),text_font,"grey100",c.SCREEN_WIDTH+5,3)
    screen.blit(heart_image, (c.SCREEN_WIDTH+5, 15))
    draw_text(str(world.health),text_font,"grey100",c.SCREEN_WIDTH+25,15)
    screen.blit(bread_image, (c.SCREEN_WIDTH+5, 30))
    draw_text(str(world.money),text_font,"grey100",c.SCREEN_WIDTH+25,30)

def create_tower(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  if world.tile_map[mouse_tile_num] == 7: # 7 is grass
    space_is_free = True
    for tower in tower_group:
      if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
        space_is_free = False
    if space_is_free == True:
      new_tower = Tower(tower_sheet, mouse_tile_x, mouse_tile_y)
      tower_group.add(new_tower)
      world.money -= c.BUY_COST

def select_tower(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  for tower in tower_group:
      if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
         return tower
def clear_selection():
   for tower in tower_group:
      tower.selected = False

def draw_event_cards(num_cards):
    drawn_cards = []
    for _ in range(num_cards):
        card = random.choice(e.event_cards)
        drawn_cards.append(card)
    return drawn_cards
def apply_event_card_effects(event_card, towers):
    global event_card_applied
    if event_card_applied == False:
      effect = event_card["effect"]
      if effect["type"] == "double_range":
          change_tower_range(towers, 2)
          event_card_applied = True
          print(f'event card {event_card} applied')
      if effect["type"] == "gain_bread":
        world.money += 100
        event_card_applied = True
        print(f'event card {event_card} applied')
      if effect["type"] == "lose_health":
         world.health -= 20
         event_card_applied = True
         print(f'event card {event_card} applied')
      if effect["type"] == "half_range":
         change_tower_range(towers, 0.5)
         event_card_applied = True
         print(f'event card {event_card} applied')
      if effect["type"] == "increase_health":
        world.health += 20
        event_card_applied = True
        print(f'event card {event_card} applied')


def change_tower_range(towers, range):
    for tower in towers:
        tower.range *= range
        new_range_image = pg.Surface((tower.range * 2, tower.range * 2))
        new_range_image.fill((0, 0, 0))
        new_range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(new_range_image, "grey100", (tower.range, tower.range), tower.range)
        new_range_image.set_alpha(100)
        tower.range_image = new_range_image
        tower.range_rect = tower.range_image.get_rect()
        tower.range_rect.center = tower.rect.center

world = World(world_data, map_image)
world.process_data()
world.process_enemies()

enemy_group = pg.sprite.Group()
tower_group = pg.sprite.Group()

print(world.waypoints)


tower_button = Button(c.SCREEN_WIDTH+15,60,buy_tower_image,True)
cancel_button = Button(c.SCREEN_WIDTH+25,90,cancel_image,True)
upgrade_button = Button(c.SCREEN_WIDTH+15,90,upgrade_image,True)
start_button = Button(c.SCREEN_WIDTH+30,130,start_image,True)
restart_button = Button(120,110,restart_image,True)
draw_cards_button = Button(c.SCREEN_WIDTH+40,110,draw_cards_image,True)

run = True
while run:
    clock.tick(c.FPS)
    if game_over == False:
       if world.health <=0:
          game_over = True
          game_outcome = -1
       if world.level > c.TOTAL_LEVELS:
          game_over = True
          game_outcome = 1   
    enemy_group.update(world)
    tower_group.update(enemy_group)

    if selected_tower:
       selected_tower.selected = True

    
    world.draw(screen)
    
    enemy_group.draw(screen)
    for tower in tower_group:
       tower.draw(screen)
    clicked = True
    display_data()
    if game_over == False:
      if level_started == False:
        if world.level is not 1 and clicked:
                if draw_cards_button.draw(screen):
                  player_event_cards = draw_event_cards(1)
                  apply_event_card_effects(player_event_cards[0], tower_group)
                  pg.draw.rect(screen,"dodgerblue",(40,50,200,100),border_radius = 15)
                  draw_text("card aquired", large_font, "grey0", 70,80)
                  draw_text(f"{player_event_cards[0].get('name')}",large_font,"grey0",70,100)
                  pg.display.flip()
                  pg.time.wait(3000)
                  

                      
                      
        if start_button.draw(screen):
          level_started = True
      else:
        if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
            if world.spawned_enemies < len(world.enemy_list): 
              enemy_type = world.enemy_list[world.spawned_enemies]
              enemy = Enemy(enemy_type, world.waypoints, enemy_images)
              enemy_group.add(enemy)
              world.spawned_enemies += 1
              last_enemy_spawn = pg.time.get_ticks()

            
    
      if world.check_level_complete() == True:
        world.money += c.LEVEL_COMPLETE_REWARD
        world.level += 1
        level_started = False
        last_enemy_spawn = pg.time.get_ticks()
        world.reset_level()
        world.process_enemies()
        event_card_applied = False
        for tower in tower_group:
          tower.range = 45
          new_range_image = pg.Surface((tower.range, tower.range))
          new_range_image.fill((0, 0, 0))
          new_range_image.set_colorkey((0, 0, 0))
          pg.draw.circle(new_range_image, "grey100", (tower.range * 2, tower.range * 2), tower.range)
          new_range_image.set_alpha(100)
          tower.range_image = new_range_image
          tower.range_rect = tower.range_image.get_rect()
          tower.range_rect.center = tower.rect.center

            
      draw_text(str(c.BUY_COST),text_font,"grey100",c.SCREEN_WIDTH+75,60)
      screen.blit(bread_image, (c.SCREEN_WIDTH+55, 60))
      if tower_button.draw(screen):
        placing_towers = True
      if placing_towers:
          cursor_rect = cursor_tower.get_rect()
          cursor_pos = pg.mouse.get_pos()
          cursor_rect.center = cursor_pos
          if cursor_pos[0] <= c.SCREEN_WIDTH:
              screen.blit(cursor_tower,cursor_rect)
          if cancel_button.draw(screen):
              placing_towers = False
      if selected_tower:
        if selected_tower.upgrade_level < c.TOWER_LEVELS:
          draw_text(str(c.UPGRADE_COST),text_font,"grey100",c.SCREEN_WIDTH+75,90)
          screen.blit(bread_image, (c.SCREEN_WIDTH+55, 90))
          if upgrade_button.draw(screen):
              if world.money >= c.UPGRADE_COST: 
                selected_tower.upgrade()
                world.money -= c.UPGRADE_COST
    else:
       pg.draw.rect(screen,"dodgerblue",(40,50,200,100),border_radius = 15)
       if game_outcome == -1:
          draw_text("GAME OVER", large_font, "grey0", 90,80)
       elif game_outcome == 1:
          draw_text("YOU WIN", large_font, "grey0", 100,80)
       if restart_button.draw(screen):
          game_over = False
          level_started = False
          placing_towers = False
          selected_tower = False
          last_enemy_spawn = pg.time.get_ticks()
          world = World(world_data, map_image)
          world.process_data()
          world.process_enemies()
          enemy_group.empty()
          tower_group.empty()
    for event in pg.event.get():
     if event.type == pg.QUIT:
      run = False
     if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = pg.mouse.get_pos()
      if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
        selected_tower = None
        clear_selection()
        if placing_towers: 
            if world.money >= c.BUY_COST:
              create_tower(mouse_pos)
        else:
          selected_tower = select_tower(mouse_pos)
    pg.display.flip()
pg.quit()