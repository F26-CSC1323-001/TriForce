# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
pygame.joystick.init
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

ControlScheme = False
UsingKeyboard = False
UsingControler = False

Control_Setup_Timer = 9999999

buttonList = [False for n in range(31)]
joysticks = {}
up = 0
down = 0
left = 0
right = 0
Action1 = 0
Action2 = 0
Action3 = 0
Action4 = 0
Action5 = 0
Action6 = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
            print(f"Joystick {joy.get_instance_id()} connencted")
        if not ControlScheme and event.type == pygame.KEYDOWN:
            ControlScheme = True
            UsingKeyboard = True
            UsingControler = False
            Control_Setup_Timer = 0
        if not ControlScheme and event.type == pygame.JOYBUTTONDOWN:
            ControlScheme = True
            UsingKeyboard = False
            UsingControler = True
            Control_Setup_Timer = 0

        if UsingControler:
            if event.type == pygame.JOYBUTTONDOWN:        
                if event.button != 7:
                    buttonList[event.button+1] = True
                elif event.button > 7:
                    buttonList[event.button] = True
                else:
                    buttonList[0] = True

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
                if event.button < 7:
                    buttonList[event.button+1] = False
                elif event.button > 7:
                    buttonList[event.button] = False
                else:
                    buttonList[0] = False
    

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)

    if UsingKeyboard == True:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            up = 0
            down = 0
            left = 0
            right = 0
            Action1 = 0
            Action2 = 0
            Action3 = 0
            Action4 = 0
            Action5 = 0
            Action6 = 0
            Control_Setup_Timer = 0

        if up == 0 and Control_Setup_Timer > 60:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i]:
                    up = i
                    Control_Setup_Timer = 0
            

        if down == 0 and Control_Setup_Timer > 60 and up != 0:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i]:
                    down = i
                    Control_Setup_Timer = 0

        if left == 0 and Control_Setup_Timer > 60 and down != 0:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i]:
                    left = i
                    Control_Setup_Timer = 0

        if right == 0 and Control_Setup_Timer > 60 and left != 0:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i]:
                    right = i
                    Control_Setup_Timer = 0

        if Action1 == 0 and Control_Setup_Timer > 60 and right != 0:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i]:
                    Action1 = i
                    Control_Setup_Timer = 0

        if Action2 == 0 and Control_Setup_Timer > 60 and Action1 != 0: 
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i]:
                    Action2 = i
                    Control_Setup_Timer = 0

        if Action3 == 0 and Control_Setup_Timer > 60 and Action2 != 0:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i]:
                    Action3 = i
                    Control_Setup_Timer = 0

        if Action4 == 0 and Control_Setup_Timer > 60 and Action3 != 0: 
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i]:
                    Action4 = i
                    Control_Setup_Timer = 0

        if Action5 == 0 and Control_Setup_Timer > 60 and Action4 != 0:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i]:
                    Action5 = i
                    Control_Setup_Timer = 0

        if Action6 == 0 and Control_Setup_Timer > 60 and Action5 != 0: 
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i]:
                    Action6 = i
                    Control_Setup_Timer = 0
        
        if keys[up] and up != 0:
            player_pos.y -= 300 * dt
        if keys[down] and up != 0:
            player_pos.y += 300 * dt
        if keys[left] and up != 0:
            player_pos.x -= 300 * dt
        if keys[right] and up != 0:
            player_pos.x += 300 * dt

        # flip() the display to put your work on screen
        pygame.display.flip()

    if UsingControler:

        if buttonList[0]:
            up = 0
            down = 0
            left = 0
            right = 0
            Action1 = 0
            Action2 = 0
            Action3 = 0
            Action4 = 0
            Action5 = 0
            Action6 = 0
            Control_Setup_Timer = 0

        if up == 0 and Control_Setup_Timer > 60:
            for i in range(len(buttonList)):
                if buttonList[i]:
                    up = i
                    Control_Setup_Timer = 0

        if down == 0 and Control_Setup_Timer > 60 and up != 0:
            for i in range(len(buttonList)):
                if buttonList[i]:
                    down = i
                    Control_Setup_Timer = 0

        if left == 0 and Control_Setup_Timer > 60 and down != 0:
            for i in range(len(buttonList)):
                if buttonList[i]:
                    left = i
                    Control_Setup_Timer = 0

        if right == 0 and Control_Setup_Timer > 60 and left != 0:
            for i in range(len(buttonList)):
                if buttonList[i]:
                    right = i
                    Control_Setup_Timer = 0

        if Action1 == 0 and Control_Setup_Timer > 60 and right != 0:
            for i in range(len(buttonList)):
                if buttonList[i]:
                    Action1 = i
                    Control_Setup_Timer = 0

        if Action2 == 0 and Control_Setup_Timer > 60 and Action1 != 0: 
            for i in range(len(buttonList)):
                if buttonList[i]:
                    Action2 = i
                    Control_Setup_Timer = 0

        if Action3 == 0 and Control_Setup_Timer > 60 and Action2 != 0:
            for i in range(len(buttonList)):
                if buttonList[i]:
                    Action3 = i
                    Control_Setup_Timer = 0

        if Action4 == 0 and Control_Setup_Timer > 60 and Action3 != 0: 
            for i in range(len(buttonList)):
                if buttonList[i]:
                    Action4 = i
                    Control_Setup_Timer = 0

        if Action5 == 0 and Control_Setup_Timer > 60 and Action4 != 0:
            for i in range(len(buttonList)):
                if buttonList[i]:
                    Action5 = i
                    Control_Setup_Timer = 0

        if Action6 == 0 and Control_Setup_Timer > 60 and Action5 != 0:
            for i in range(len(buttonList)):
                if buttonList[i]:
                    Action6 = i
                    Control_Setup_Timer = 0
        
        if buttonList[up] and up != 0:
            player_pos.y -= 300 * dt
        if buttonList[down] and up != 0:
            player_pos.y += 300 * dt
        if buttonList[left] and up != 0:
            player_pos.x -= 300 * dt
        if buttonList[right] and up != 0:
            player_pos.x += 300 * dt

        # flip() the display to put your work on screen
        pygame.display.flip()

    Control_Setup_Timer += 1

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
