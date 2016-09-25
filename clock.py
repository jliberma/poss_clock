# This program creates a possession timer that tracks:
# live ball time of possession for two teams
# dead ball time of possession for two teams
# and writes the total time of possession for both teams
# to a file.
# jliberman@utexas.edu

import pygame
from pygame.locals import Color
from sys import argv, exit


class Timer:

    def __init__(self, name, color, target_posn, height, width):
        self.my_h = height
        self.my_w = width
        (self.my_x, self.my_y) = self.posn = target_posn
        self.color = color
        self.name = name
        self.is_on = 0
        self.total_seconds = 0
        self.count = 0

    def update(self):
        if self.is_on == True:
            self.total_seconds += 1

    def draw(self, target_surface):
        font = pygame.font.SysFont("comicsansms",20)

        # highlight the active timer
        if self.is_on == True:
            pygame.draw.rect(target_surface, Color("green"), (self.posn,(self.my_h,self.my_w)))
            seconds = self.total_seconds // 60 % 60
            minutes = self.total_seconds // 60 // 60 % 60
            output_string = "{1:02}:{0:02}".format(seconds, minutes)
            text_surf = font.render(output_string,0,(0,0,0))
            text_rect = text_surf.get_rect()
            text_rect.center = ( (self.my_x+(self.my_w/2)), (self.my_y+(self.my_w/2)) )
            target_surface.blit(text_surf, text_rect)
        else:
            pygame.draw.rect(target_surface, self.color, (self.posn,(self.my_h,self.my_w)))
            label = font.render(self.name,0,Color("white"))
            label_rect = label.get_rect()
            label_rect.center = ( (self.my_x+(self.my_w/2)), (self.my_y+(self.my_w/2)) )
            target_surface.blit(label,label_rect)

    def handle_click(self):
        self.is_on = True
        self.count += 1

    def contains_point(self, pt):
        (x, y) = pt
        return ( x >= self.my_x and x < self.my_x + self.my_h and
                 y >= self.my_y and y < self.my_y + self.my_w)

    def halt(self):
        self.is_on = False

    def timer_exit(self):
        return

def draw_timers():

    pygame.init()

    # Create the surface
    surface = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("Time of possession")

    # keep a list of timers
    all_timers = []

    # Instantiate the timers
    timer1 = all_timers.append(Timer("1_LIVE",Color("red"),(1,1),150,100))
    timer2 = all_timers.append(Timer("1_DEAD",Color("red"),(1,101),150,100))
    timer3 = all_timers.append(Timer("2_LIVE",Color("blue"),(150,1),150,100))
    timer4 = all_timers.append(Timer("2_DEAD",Color("blue"),(150,101),150,100))

    while True:

        # Look for keyboard, mouse events
        ev = pygame.event.poll()
#        if ev.type != pygame.NOEVENT:      # print interesting events
#            print(ev)
        if ev.type == pygame.QUIT:
            break;
        if ev.type == pygame.KEYDOWN:
            key = ev.dict["key"]
            if key == 27:                  # Exit on Escape key
                break
            if key == pygame.K_p:          # Pause all timers on p key
                for timer in all_timers:
                    timer.halt()

        # Handle mouse clicks
        if ev.type == pygame.MOUSEBUTTONDOWN:
            posn_of_click = ev.dict["pos"]
            for timer in all_timers:
                timer.halt()
                if timer.contains_point(posn_of_click):
                    timer.handle_click()

        # Update every timer
        for timer in all_timers:
            timer.update()

        # Draw the surface
        surface.fill(Color("white"))

        # Draw every timer
        for timer in all_timers:
            timer.draw(surface)

        pygame.display.flip()

    pygame.quit()

    # write results to a file
    target = open(filename, 'w')
    for timer in all_timers:
        output_string = "{},{},{}\n".format(timer.name,timer.count,timer.total_seconds // 60)
        target.write(output_string)
    target.close()

if __name__ == "__main__":
    try:
        filename = argv[1]
    except IndexError:
        print("Usage: clock.py <output_filename>")
        exit(1)

    draw_timers()
