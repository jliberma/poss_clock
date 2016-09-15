import pygame
from pygame.locals import Color

# write results to a file
# add method to turn off other buttons when this button is turned on?
# use loop to create timers and populate the list using an offset
# add stop all timers before exit on button push
# instead of printing valued, pass them to a dict to sum them at exit

class Timer:

    def __init__(self, name, color, target_posn, height, width):
        self.my_h = height
        self.my_w = width
        (self.my_x, self.my_y) = self.posn = target_posn
        self.color = color
        self.name = name
        self.is_on = 0
        self.total_seconds = 0

    def update(self):
        if self.is_on == True:
            self.total_seconds += 1

    def draw(self, target_surface):
        # highlight the timer that is on
        if self.is_on == True:
            pygame.draw.rect(target_surface, Color("green"), (self.posn,(self.my_h,self.my_w)))
        else:
            pygame.draw.rect(target_surface, self.color, (self.posn,(self.my_h,self.my_w)))

        # label the timers
        font = pygame.font.SysFont("comicsansms",20)
        label = font.render(self.name,0,Color("black"))
        target_surface.blit(label, (self.my_x+5,self.my_y-25))

        # draw the time
        seconds = self.total_seconds // 60 % 60
        minutes = self.total_seconds // 60 // 60 % 60
        output_string = "{1:02}:{0:02}".format(seconds, minutes)
        text_surf = font.render(output_string,0,(0,0,0))
        text_rect = text_surf.get_rect()
        text_rect.center = ( (self.my_x+(self.my_h/2)), (self.my_y+(self.my_w/2)) )
        target_surface.blit(text_surf, text_rect)

    def handle_click(self):
        if self.is_on == True:
            self.is_on = False
            print(self.name,": ",self.total_seconds // 60)
        else:
            self.is_on = True

    def contains_point(self, pt):
        (x, y) = pt
        return ( x >= self.my_x and x < self.my_x + self.my_h and
                 y >= self.my_y and y < self.my_y + self.my_w)

def draw_board():

    pygame.init()

    # Create the surface of (width, height), and its window.
    surface = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("Time of possession")

    all_timers = []      # Keep a list of all timers in the game

    # Instantiate two duke instances, put them on the chessboard
    timer1 = Timer("1 LIVE",Color("red"),(45,40),100,50)
    timer2 = Timer("1 DEAD",Color("red"),(45,115),100,50)
    timer3 = Timer("2 LIVE",Color("blue"),(155,40),100,50)
    timer4 = Timer("2 DEAD",Color("blue"),(155,115),100,50)

    # Add them to the list of timers which our game loop manages
    all_timers.append(timer1)
    all_timers.append(timer2)
    all_timers.append(timer3)
    all_timers.append(timer4)

    while True:

        # Look for an event from keyboard, mouse, etc.
        ev = pygame.event.poll()
#        if ev.type != pygame.NOEVENT:   # Only print if it is interesting!
#            print(ev)
        if ev.type == pygame.QUIT:
            break;
        if ev.type == pygame.KEYDOWN:
            key = ev.dict["key"]
            if key == 27:                  # On Escape key ...
                break                      #   leave the game loop.

        if ev.type == pygame.MOUSEBUTTONDOWN:
            posn_of_click = ev.dict["pos"]
            for timer in all_timers:
                if timer.contains_point(posn_of_click):
                    timer.handle_click()
                    break

        # Ask every timer to update itself.
        for timer in all_timers:
            timer.update()

        # Draw a surface
        surface.fill(Color("white"))

        # Ask every timer to draw itself.
        for timer in all_timers:
            timer.draw(surface)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    draw_board()
