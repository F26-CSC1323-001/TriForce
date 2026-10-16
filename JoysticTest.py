import pygame

pygame.init()


# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


def main():
    # Set the width and height of the screen (width, height), and name the window.
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption("Joystick example")
    buttonList = [False for n in range(0,30)]
    GrumbleButton = 0
    ChangeButton = False
    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Get ready to print.
    text_print = TextPrint()

    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    done = False
    while not done:

        #print(pygame.event.get())
        
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.
            if event.type == pygame.JOYBUTTONDOWN:        
                buttonList[event.button] = True

            if event.type == pygame.JOYAXISMOTION:
                joystick = joysticks[event.instance_id]
                if joystick.get_axis(0) > .5:
                    buttonList[16] = True
                else:
                    buttonList[16] = False
                if joystick.get_axis(0) < -.5:
                    buttonList[17] = True
                else:
                    buttonList[17] = False
                if joystick.get_axis(1) > .5:
                    buttonList[18] = True
                else:
                    buttonList[18] = False
                if joystick.get_axis(1) < -.5:
                    buttonList[19] = True
                else:
                    buttonList[19] = False
                if joystick.get_axis(2) > .5:
                    buttonList[20] = True
                else:
                    buttonList[20] = False
                if joystick.get_axis(2) < -.5:
                    buttonList[21] = True
                else:
                    buttonList[21] = False
                if joystick.get_axis(3) > .5:
                    buttonList[22] = True
                else:
                    buttonList[22] = False
                if joystick.get_axis(3) <-.5:
                    buttonList[23] = True
                else:
                    buttonList[23] = False
                if joystick.get_axis(4) > 0:
                    buttonList[24] = True
                else:
                    buttonList[24] = False
                if joystick.get_axis(5) > 0:
                    buttonList[25] = True
                else:
                    buttonList[25] = False  

            if event.type == pygame.JOYHATMOTION:
                joystick = joysticks[event.instance_id]
                hat_x,hat_y = joystick.get_hat(0)
                if hat_x == 1:
                    buttonList[26] = True
                else:
                    buttonList[26] = False
                if hat_x == -1:
                    buttonList[27] = True
                else:
                    buttonList[27] = False
                if hat_y == 1:
                    buttonList[28] = True
                else:
                    buttonList[28] = False
                if hat_y == -1:
                    buttonList[29] = True
                else:
                    buttonList[29] = False


            if event.type == pygame.JOYBUTTONUP:
                buttonList[event.button] = False

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")
            print(buttonList)

        # Drawing step
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill((255, 255, 255))
        text_print.reset()

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        text_print.tprint(screen, f"Number of joysticks: {joystick_count}")
        text_print.indent()

        # For each joystick:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()

            text_print.tprint(screen, f"Joystick {jid}")
            text_print.indent()

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            text_print.tprint(screen, f"Joystick name: {name}")

            guid = joystick.get_guid()
            text_print.tprint(screen, f"GUID: {guid}")

            power_level = joystick.get_power_level()
            text_print.tprint(screen, f"Joystick's power level: {power_level}")

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other. Triggers count as axes.
            axes = joystick.get_numaxes()
            text_print.tprint(screen, f"Number of axes: {axes}")
            text_print.indent()

            for i in range(axes):
                axis = joystick.get_axis(i)
                text_print.tprint(screen, f"Axis {i} value: {axis:>6.3f}")
            text_print.unindent()

            buttons = joystick.get_numbuttons()
            text_print.tprint(screen, f"Number of buttons: {buttons}")
            text_print.indent()

            for i in range(buttons):
                button = joystick.get_button(i)
                text_print.tprint(screen, f"Button {i:>2} value: {button}")
            text_print.unindent()

            hats = joystick.get_numhats()
            text_print.tprint(screen, f"Number of hats: {hats}")
            text_print.indent()

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)
                text_print.tprint(screen, f"Hat {i} value: {str(hat)}")
            text_print.unindent()

            text_print.unindent()

        

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 30 frames per second.
        clock.tick(30)


if __name__ == "__main__":

    print(pygame.JOYBUTTONDOWN)
    
    main()
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()