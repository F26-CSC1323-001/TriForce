# Example file showing a circle moving on screen
import pygame
import ReaderDefiner
from random import randint
# pygame setup
pygame.init()
pygame.joystick.init
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

Reader = ReaderDefiner.inputReader(0,60,60,60,60,60)

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

controls =[False for n in range(10)]

while running:
    # poll for events
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

    if UsingKeyboard == True:
        keys = pygame.key.get_pressed()

        #This resets the controls if the escape key is pressed

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

        #This series of if statements set up the contols

        if up == 0 and Control_Setup_Timer > 60:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i] and i != pygame.K_ESCAPE:
                    up = i
                    Control_Setup_Timer = 0
        
        if down == 0 and Control_Setup_Timer > 60 and up != 0:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i] and i != pygame.K_ESCAPE:
                    down = i
                    Control_Setup_Timer = 0
        
        if left == 0 and Control_Setup_Timer > 60 and down != 0:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i] and i != pygame.K_ESCAPE:
                    left = i
                    Control_Setup_Timer = 0
        
        if right == 0 and Control_Setup_Timer > 60 and left != 0:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i] and i != pygame.K_ESCAPE:
                    right = i
                    Control_Setup_Timer = 0
        
        if Action1 == 0 and Control_Setup_Timer > 60 and right != 0:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i] and i != pygame.K_ESCAPE:
                    Action1 = i
                    Control_Setup_Timer = 0
        
        if Action2 == 0 and Control_Setup_Timer > 60 and Action1 != 0: 
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i] and i != pygame.K_ESCAPE:
                    Action2 = i
                    Control_Setup_Timer = 0

        if Action3 == 0 and Control_Setup_Timer > 60 and Action2 != 0:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i] and i != pygame.K_ESCAPE:
                    Action3 = i
                    Control_Setup_Timer = 0
        
        if Action4 == 0 and Control_Setup_Timer > 60 and Action3 != 0: 
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i] and i != pygame.K_ESCAPE:
                    Action4 = i
                    Control_Setup_Timer = 0
        
        if Action5 == 0 and Control_Setup_Timer > 60 and Action4 != 0:
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i] and i != pygame.K_ESCAPE:
                    Action5 = i
                    Control_Setup_Timer = 0

        #Sets Controls List

        if Action6 == 0 and Control_Setup_Timer > 60 and Action5 != 0: 
            keys = pygame.key.get_pressed()
            for i in range(len(keys)):
                if keys[i] and i != pygame.K_ESCAPE:
                    Action6 = i
                    Control_Setup_Timer = 0

        if Action6 != 0:
            controls = [keys[up], keys[down], keys[left], keys[right], keys[Action1], keys[Action2], keys[Action3], keys[Action4], keys[Action5], keys[Action6]]

        # flip() the display to put your work on screen
        pygame.display.flip()

    if UsingControler:

        #This resets the controls if the start button is clicked        

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

        #This series of if statements set up the controls

        if up == 0 and Control_Setup_Timer > 60:
            for i in range(len(buttonList)):
                if buttonList[i] and i != 0:
                    up = i
                    Control_Setup_Timer = 0

        if down == 0 and Control_Setup_Timer > 60 and up != 0:
            for i in range(len(buttonList)):
                if buttonList[i] and i != 0:
                    down = i
                    Control_Setup_Timer = 0

        if left == 0 and Control_Setup_Timer > 60 and down != 0:
            for i in range(len(buttonList)):
                if buttonList[i] and i != 0:
                    left = i
                    Control_Setup_Timer = 0

        if right == 0 and Control_Setup_Timer > 60 and left != 0:
            for i in range(len(buttonList)):
                if buttonList[i] and i != 0:
                    right = i
                    Control_Setup_Timer = 0

        if Action1 == 0 and Control_Setup_Timer > 60 and right != 0:
            for i in range(len(buttonList)):
                if buttonList[i] and i != 0:
                    Action1 = i
                    Control_Setup_Timer = 0

        if Action2 == 0 and Control_Setup_Timer > 60 and Action1 != 0: 
            for i in range(len(buttonList)):
                if buttonList[i] and i != 0:
                    Action2 = i
                    Control_Setup_Timer = 0

        if Action3 == 0 and Control_Setup_Timer > 60 and Action2 != 0:
            for i in range(len(buttonList)):
                if buttonList[i] and i != 0:
                    Action3 = i
                    Control_Setup_Timer = 0

        if Action4 == 0 and Control_Setup_Timer > 60 and Action3 != 0: 
            for i in range(len(buttonList)):
                if buttonList[i] and i != 0:
                    Action4 = i
                    Control_Setup_Timer = 0

        if Action5 == 0 and Control_Setup_Timer > 60 and Action4 != 0:
            for i in range(len(buttonList)):
                if buttonList[i] and i != 0:
                    Action5 = i
                    Control_Setup_Timer = 0

        if Action6 == 0 and Control_Setup_Timer > 60 and Action5 != 0:
            for i in range(len(buttonList)):
                if buttonList[i] and i != 0:
                    Action6 = i
                    Control_Setup_Timer = 0
            player_pos.x += 300 * dt

        #Sets Controls List

        if Action6 != 0:
            controls = [buttonList[up], buttonList[down], buttonList[left], buttonList[right], buttonList[Action1], buttonList[Action2], buttonList[Action3], buttonList[Action4], buttonList[Action5], buttonList[Action6]]
        
        # flip() the display to put your work on screen
        pygame.display.flip()


    #controls is a list of boolean values that correspond to the controls in this order: up, down, left, right, Action1, Action2, Action3, Action4, Action5, Action6
    
    #Reader is our input reader, any check functions will use it

    #all of the check funcitons have three return values, the first value is either the progress on the input (for input checks like fQCCheck) or the block type (for defenseCheck), the second is the timer, and the third is the check value (0 = incomplete, 1 = success, 2 = failure)

    #below is an example line for an input check function
    # sequence, timer, checkValue = Reader.fQCCheck(controls[0], controls[1], controls[2], controls[3], controls[4], sequence, timer)
    # the fifth parameter can be any of the action buttons, and should be set by the user
    # it is integral that both sequences and timers are the same variable

    #Main

    




    ###


    #You should put all frame counter here (if you have any)
    Control_Setup_Timer += 1

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
