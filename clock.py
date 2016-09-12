import pygame

# write results to a file
# add a clock name for writing results by name
# add a color to the clock draw
# add height and width to class definition for CLockSprite object
# add method to run off other buttons when this button is turned on?
# use loop to create clocks and populate the list
# move self.posn calcl & vairables to init def and re-use in other methods
# use the colors dict
# use consistentand sensible naming for classes, variables, objects

class ClockSprite:

    def __init__(self, color, target_posn):
        self.posn = target_posn
        self.color = color
        self.is_on = 0
        self.total_seconds = 0

    def update(self):
        if self.is_on == True:
            self.total_seconds += 1

    def draw(self, target_surface):
        if self.is_on == True:
            pygame.draw.rect(target_surface, (0,255,0), (self.posn,(100,50)))
        else:
            pygame.draw.rect(target_surface, self.color, (self.posn,(100,50)))

        # move this into the is_on loop
	# add a clock name to the is_off loop
        seconds = self.total_seconds // 60 % 60
        minutes = self.total_seconds // 60 // 60 % 60
        output_string = "{1:02}:{0:02}".format(seconds, minutes)
        font = pygame.font.SysFont("comicsansms",20)
        textSurf = font.render(output_string,0,(0,0,0))
        textRect = textSurf.get_rect()
        (my_x, my_y) = self.posn
        my_width = 100
        my_height = 50
        textRect.center = ( (my_x+(my_width/2)), (my_y+(my_height/2)) )
        target_surface.blit(textSurf, textRect)

    def handle_click(self):
        if self.is_on == True:
            self.is_on = False
        else:
            self.is_on = True
        print(self.total_seconds // 60)

    def contains_point(self, pt):
        (my_x, my_y) = self.posn
        my_width = 100
        my_height = 50
        (x, y) = pt
        return ( x >= my_x and x < my_x + my_width and
                 y >= my_y and y < my_y + my_height)

def draw_board():

    pygame.init()
    colors = [(255,255,255), (0,0,0)]    # Set up colors [red, black]

    # Create the surface of (width, height), and its window.
    surface = pygame.display.set_mode((360, 360))
    pygame.display.set_caption("Time of possession")

    all_clocks = []      # Keep a list of all sprites in the game

    # Instantiate two duke instances, put them on the chessboard
    clock1 = ClockSprite((255,0,0),(80,100))
    clock2 = ClockSprite((0,0,255),(190,100))
    clock3 = ClockSprite((255,0,0),(80,160))
    clock4 = ClockSprite((0,0,255),(190,160))

    # Add them to the list of sprites which our game loop manages
    all_clocks.append(clock1)
    all_clocks.append(clock2)
    all_clocks.append(clock3)
    all_clocks.append(clock4)

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
            for sprite in all_clocks:
                if sprite.contains_point(posn_of_click):
                    sprite.handle_click()
                    break

        # Ask every sprite to update itself.
        for sprite in all_clocks:
            sprite.update()

        # Draw a surface
        surface.fill((255,255,255))

        # Ask every sprite to draw itself.
        for sprite in all_clocks:
            sprite.draw(surface)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    draw_board()
