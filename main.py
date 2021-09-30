##########
#
#  NOTE:  Important!  Please read!
#  
#  The code below is my attempt to add additional features to the game and is NOT optimized 
#  due to time constraints.  If you wish to look at a project that is closer to the parameter
#  of the mini-project, please look at:
#  
#  http://www.codeskulptor.org/#user27_zAO4po4eDf_0.py
#
#  However, if you wish to see what I was up to, I hope you enjoy the game!
#
##########



# implementation of Spaceship - program template for RiceRocks
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 4
time = 0
number_hit = 0
started = False
shield = 3

# initialize sets for rocks and missile
rock_group = set([])
missile_group = set([])
explosion_group = set([])

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# starship image
#starship_info = ImageInfo([231, 220], [462, 441], 45)
#starship_image = simplegui.load_image("https://dl.dropbox.com/s/rr5i5w17zk0avsy/imageedit_3_5777260884.gif")
#starship_power_image = simplegui.load_image("https://dl.dropbox.com/s/fj89llvew9z41m6/imageedit_3_2802981209.gif")
starship_info = ImageInfo([45, 45], [90, 90], 35)
starship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
starship_power_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image_1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroid_image_2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")
asteroid_image_3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")


# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_rock_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_rock_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# animated explosion for rocks
explosion_big_info = ImageInfo([50, 50], [100, 100], 17, 80, True)
explosion_big_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")


# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(0.5)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        #canvas.draw_image(self.image, self.image_center, self.image_size,
        #                  self.pos, [self.image_size[0] / 5, self.image_size[1] / 5], self.angle)
        if self.thrust:
            canvas.draw_image(starship_power_image, self.image_center, self.image_size,
                              self.pos, [self.image_size[0] / 5, self.image_size[1] / 5], self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, [self.image_size[0] / 5, self.image_size[1] / 5], self.angle)
        # draw shield
        if shield == 3:
            canvas.draw_circle(self.pos, 55, 1, "rgba(0, 0, 255, 0.3)", "rgba(0, 0, 255, 0.4)")
        elif shield == 2:
            canvas.draw_circle(self.pos, 55, 1, "rgba(0, 0, 255, 0.2)", "rgba(0, 0, 255, 0.3)")
        elif shield == 1:
            canvas.draw_circle(self.pos, 55, 1, "rgba(0, 0, 255, 0.1)", "rgba(0, 0, 255, 0.2)")
        
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .992
        self.vel[1] *= .992

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global group_missile
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        # Sprite(self, pos, vel, ang, ang_vel, image, info, size, age = 0, sound = None)
        missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, "large", 0, missile_sound)
        missile_group.add(missile)
      
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, size, age = 0, sound = None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.size = size
        self.age = age
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        return self.pos
    
    def get_velocity(self):
        return self.vel
    
    def get_radius(self):
        return self.radius
    
    def get_size(self):
        return self.size
    
    def draw(self, canvas):
        if self.animated:
            explosion_index = self.age % 24
            canvas.draw_image (self.image, [self.image_center[0] + explosion_index * self.image_size[0],
                                            self.image_center[1]], self.image_size, self.pos, self.image_size)
            # this beautiful explosion seems to slow the game down significantly
            #explosion_index = [self.age % 9, (self.age // 9) % 9]
            #canvas.draw_image(self.image, [self.image_center[0] + explosion_index[0] * self.image_size[0],
            #                               self.image_center[1] + explosion_index[1] * self.image_size[1]], 
            #                               self.image_size, self.pos, self.image_size)
        elif self.size == "small":
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, [self.image_size[0] / 3, self.image_size[1] / 3], self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def collide(self, other_object):
        distance = dist(self.pos, other_object.get_position())
        if self.get_size() == "large":
            if distance <= self.radius + other_object.get_radius():
                return True
            else:
                return False
        elif self.get_size() == "small":
            if distance <= self.radius / 2 + other_object.get_radius():
                return True
            else:
                return False 
    
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # update age
        self.age += 1
        if self.age < self.lifespan:
            return False
        else:
            return True
  
        
# key handlers to control ship   
def keydown(key):
    if started:
        if key == simplegui.KEY_MAP['left']:
            my_ship.decrement_angle_vel()
        elif key == simplegui.KEY_MAP['right']:
            my_ship.increment_angle_vel()
        elif key == simplegui.KEY_MAP['up']:
            my_ship.set_thrust(True)
        elif key == simplegui.KEY_MAP['space']:
            my_ship.shoot()
        
def keyup(key):
    if started:
        if key == simplegui.KEY_MAP['left']:
            my_ship.increment_angle_vel()
        elif key == simplegui.KEY_MAP['right']:
            my_ship.decrement_angle_vel()
        elif key == simplegui.KEY_MAP['up']:
            my_ship.set_thrust(False)
            
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives, shield
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()
        lives = 4
        score = 0
        shield = 3

def draw(canvas):
    global time, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), 
                      [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    shield_percent = int(shield / 3.0 * 100)
    hull_percent = int(lives / 4.0 * 100)
    # color for shield indicator
    if shield_percent == 100:
        shield_color = "Green"
    elif shield_percent == 66:
        shield_color = "Yellow"
    elif shield_percent == 33:
        shield_color = "Red"
    else:
        shield_color = "Grey"
    
    # color for hull indicator
    if hull_percent == 100:
        hull_color = "Green"
    elif hull_percent == 75:
        hull_color = "Yellow"
    elif hull_percent == 50:
        hull_color = "Orange"
    elif hull_percent == 25:
        hull_color = "Red"
    else:
        hull_color = "Grey"
    canvas.draw_text("Shield Power:", [45, 50], 22, shield_color, "sans-serif")
    canvas.draw_text(str(shield_percent) + "%", [185, 50], 22, shield_color, "sans-serif")
    canvas.draw_text("Hull Integrity:", [55, 80], 22, hull_color, "sans-serif")
    canvas.draw_text(str(hull_percent) + "%", [185, 80], 22, hull_color, "sans-serif")
    canvas.draw_text("Score", [680, 50], 22, "White", "sans-serif")
    canvas.draw_text(str(score), [680, 80], 22, "White", "sans-serif")

    # draw ship
    my_ship.draw(canvas)
            
    # update ship
    my_ship.update()
    
    # call helper function that draws and updates sprites
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # call helper funtion that detects collision
    # collision between ship and rock
    group_collide(rock_group, my_ship)
    # collision between missiles and rocks
    group_group_collide(missile_group, rock_group)
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    elif started and lives == 0:
        reset()
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
 

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    if score < 200:
        rock_count = 5
        speed = 2.0
    elif score < 450:
        rock_count = 7
        speed = 3.0
    elif score < 750:
        rock_count = 10
        speed = 5.0
    else:
        rock_count = 14
        speed = 8.0
    #print rock_count    
    if started and len(rock_group) <= rock_count:
        rock_pos_1 = [random.randrange(0, WIDTH), 10]
        rock_pos_2 = [10, random.randrange(10, HEIGHT)]
        rock_pos_3 = [random.randrange(0, WIDTH), HEIGHT - 10]
        rock_pos_4 = [WIDTH - 10, random.randrange(0, HEIGHT)]
        rock_pos = random.choice([rock_pos_1, rock_pos_2, rock_pos_3, rock_pos_4])
        rock_vel = [random.random() * speed - (speed / 2), random.random() * speed - (speed / 2)]
        rock_avel = random.choice([-1, 1]) * random.randrange(0, 20)/600.0 
        asteroid_image = random.choice([asteroid_image_1, asteroid_image_2])
        # Sprite(self, pos, vel, ang, ang_vel, image, info, size, age = 0, sound = None)
        rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info, "large")
        if dist(rock_pos, my_ship.get_position()) > (my_ship.get_radius() + rock.get_radius()) * 1.5:
            rock_group.add(rock)    
   
# helper function to draw and updates the sprites in sprite_group
def process_sprite_group(group, canvas):
    timeout = set([])
    for sprite in group:
        sprite.draw(canvas)
        #sprite.update()
        if sprite.update():  # very interesting behaviour!  looks like update is done here
            timeout.add(sprite)
    group.difference_update(timeout)
        
# helper function to check for ship-rock collisions
def group_collide(group, other_object):
    global lives, explosion_group, shield
    hit_group = set([])
    for element in set(group):
        if element.collide(other_object):
            # Sprite(self, pos, vel, ang, ang_vel, image, info, size, age = 0, sound = None)
            rock_explosion = Sprite(element.get_position(), [0, 0], 0, 0, explosion_image, 
                                    explosion_info, "large", 0, explosion_sound)
            explosion_group.add(rock_explosion)
            hit_group.add(element)
            if shield > 0:
                shield -= 1
            elif shield == 0:
                lives -= 1
            if lives == 0:
                ship_explosion = Sprite(other_object.get_position(), [0, 0], 0, 0, explosion_rock_image, 
                                    explosion_info, "large", 0, explosion_sound)
                explosion_group.add(ship_explosion)
                reset()
    group.difference_update(hit_group)
    
# helper function to check for missile-rock collisions
def group_group_collide(group_m, group_r):
    global score, explosion_group
    score_group = set([])
    hit_group = set([])
    group_m_copy = set(group_m)
    for element_r in set(group_r):
        for element_m in set(group_m):
            if element_r.collide(element_m):
                # Sprite(self, pos, vel, ang, ang_vel, image, info, age = 0, sound = None)
                if element_r.get_size() == "large":
                    # explode large asteriod
                    rock_explosion = Sprite(element_r.get_position(), [0, 0], 0, 0, explosion_rock_image,
                                            explosion_info, "large", 0, explosion_sound)
                    explosion_group.add(rock_explosion)
                    # create two small asteriods
                    rock_vel = element_r.get_velocity()
                    rock_1 = Sprite(element_r.get_position(), 
                                  [rock_vel[0] * -1 / 10.0, 
                                   rock_vel[1] * random.randrange(10, 16) / 10.0], 
                                  0, 0, asteroid_image_3, asteroid_info, "small")
                    rock_2 = Sprite(element_r.get_position(), 
                                  [rock_vel[0] * random.randrange(10, 16)  / 10.0, 
                                   rock_vel[1] * -1 / 10.0], 
                                  0, 0, asteroid_image_3, asteroid_info, "small")
                    group_r.add(rock_1)
                    group_r.add(rock_2)
                    score_group.add(element_m)
                    hit_group.add(element_r)
                    score += 10
                elif element_r.get_size() == "small":
                    rock_explosion = Sprite(element_r.get_position(), [0, 0], 0, 0, explosion_rock_image,
                                            explosion_info, "large", 0, explosion_sound)
                    explosion_group.add(rock_explosion)
                    score_group.add(element_m)
                    hit_group.add(element_r)
                    score += 5
    group_m.difference_update(score_group)
    group_r.difference_update(hit_group)
    
# helper function that resets the game
def reset():
    global time, started, rock_group, missile_group, my_ship
    rock_group = set([])
    missile_group = set([])
    time = 0
    started = False
    soundtrack.pause()
    soundtrack.rewind()
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, starship_image, starship_info)
    my_ship.set_thrust(False)
                
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, starship_image, starship_info)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()



