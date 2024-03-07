import pygame as pg
import json
from enemy import Enemy
from world import World
from tower import Tower
import constants as c

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH,c.SCREEN_HEIGHT))
pg.display.set_caption("Goobers vs Gobbers")

map_image = pg.image.load('images/goobersvsgoobbers.png').convert_alpha()

cursor_tower = pg.image.load('images/tower.png')

enemy_image = pg.image.load('images/redenemy.png').convert_alpha()

with open('goobersvsgoobbers.tmj') as file:
    world_data = json.load(file)

world = World(world_data, map_image)
world.process_data()

enemy_group = pg.sprite.Group()
tower_group = pg.sprite.Group()

print(world.waypoints)

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

run = True
while run:
    clock.tick(c.FPS)

    screen.fill("grey100")

    world.draw(screen)


    enemy_group.update()

    enemy_group.draw(screen)
    tower_group.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            tower = Tower(cursor_tower,mouse_pos)
            tower_group.add(tower)
    pg.display.flip()
pg.quit()