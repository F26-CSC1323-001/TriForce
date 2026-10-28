from random import randint

class opponentAttack():
    def __init__(self, HitTime:int, High:bool = False, Mid:bool = False, Low:bool = False, CHigh:bool = False, CMid:bool = False, CLow:bool = False, AmbiguityTime:int = 1):
        
        #ReaderDefiner.opponentsAttack is a class that defines an attack, initialization has 8 vars: HitTime:int (how long the move takes to hit from startup), High:bool, Mid:bool, Low:bool, CHigh:bool, CMid:bool, CLow:bool (These last 6 define the type of blocking the action threatens, one will be chosen), AmbiguityTime:int (how long until the move can be discerned)
        
        self.Hits = [High, Mid, Low, CHigh, CMid, CLow]
        self.HitTime = HitTime
        self.AmbiguityTime = AmbiguityTime
    

class inputReader():

    def __init__(self, buffer:int, QCFrames:int, ZFrames:int, FCFrames:int, HCFrames:int, TurnAround:int):
        
        #ReaderDefiner.inputReader is a class that sets the buffer and has all of the motion inputs and defensive check, initialization has 6 vars: buffer:int (may not be used), QCFrames:int (defines how long a player has to input a quarter circle), ZFrames:int (defines how long a player has to input a Z-input), FCFrames:int (defines how long a player has to input a 360), HCFrames:int (defines how long a player has to input a half circle), TurnAround:int (defines how long a player has until they have to block in the other direction on crossup)
        
        self.buffer = buffer
        self.QCFrames = QCFrames
        self.ZFrames = ZFrames
        self.FCFrames = FCFrames
        self.HCFrames = HCFrames
        self.TurnAround = TurnAround

    def defenseCheck(self, up:bool, down:bool, left:bool, right:bool, attack:opponentAttack, hitType:int, framesSinceStartUp:int):
        
        #the first four vars are the inputs, attack is the attack that is being defended, framesSinceStartUp is the time since the attack has been started, hitType is the index if the type of hit
        
        #this returns 3 values, the first is the next framesSinceStartup, the second is wether the attack was blocked (0 = attack has not hit yet, 1 = attack was successfully blocked, 2 = attack was not blocked)
        
        hitID = hitType

        #this decides if the attack should start this frame
        if framesSinceStartUp == 0:
            if randint(0,50) >= 40:
                return 1, 1, 0
            else:
                return 1, 0, 0

        #this decides what block type is required once it reaches AmbiguityTime
        if framesSinceStartUp == attack.AmbiguityTime:
            setHitType = False
            if attack.Hits[0] or attack.Hits[1] or attack.Hits[2] or attack.Hits[3] or attack.Hits[4] or attack.Hits[5]:
                setHitType = False
                while not setHitType:
                    hitID = randint(0,5)
                    if attack.Hits[hitID]:
                        setHitType = True
            else:
                hitID = 1

        #this checks if the player has properly blocked
        if framesSinceStartUp == attack.HitTime:
            if hitType == 0 and not up and not down and left and not right:
                return 1, 0, 1
            if hitType == 1 and not up and left and not right:
                return 1, 0, 1
            if hitType == 2 and not up and down and left and not right:
                return 1, 0, 1
            if hitType == 3 and not up and not down and not left and right:
                return 1, 0, 1
            if hitType == 4 and not up and not left and right:
                return 1, 0, 1
            if hitType == 5 and not up and down and not left and right:
                return 1, 0, 1
            else:
                return 1, 0, 2
        else:
            return hitID, framesSinceStartUp+1, 0


    def fQCcheck(self, up, down, left, right, actionButton, sequence, timer):

        # checks if the player does a forward quarter circle
        # up, down, left, right, actionButton (controls), sequence (the point in the input, should be changed by the function over time), timer (time since the input started, should be changed by the function over time)
        
        # returns three values: the sequence of the input (should be passed back in), the timer (should be passed back in), and the check value (0 = no definite result, 1 = successcul input, 2 = failed input)

        #this general pattern is maintained for all input check functions

        if timer > self.QCFrames and sequence != 0:
            return 0 , 0,  2
        if sequence == 0 and not up and down and not left and not right:
            return 1 , timer+1, 0
        if sequence == 1 and not up and down and not left and right:
            return 2 , timer+1, 0
        if sequence == 2 and not up and not down and not left and right:
            return 3, timer+1, 0
        if sequence == 3 and actionButton:
            return 0 , timer+1, 1
        else:
            return sequence, timer + 1, 0, 0

    def bQCcheck(self, up, down, left, right, actionButton, sequence, timer):
        if timer > self.QCFrames and sequence != 0:
            return 0 , 0, 2
        if sequence == 0 and not up and down and not left and not right:
            return 1 , timer+1, 0
        if sequence == 1 and not up and down and left and not right:
            return 2 , timer+1, 0
        if sequence == 2 and not up and not down and left and not right:
            return 3, timer +1, 0
        if sequence == 3 and actionButton:
            return 0 , timer+1, 1
        else:
            return sequence, timer + 1, 0

    def fZcheck(self, up, down, left, right, actionButton, sequence, timer):
        if timer > self.ZFrames and sequence != 0:
            return 0 , 0, 2
        if sequence == 0 and not up and not down and not left and right:
            return 1 , timer+1, 0
        if sequence == 1 and not up and down and not left and not right:
            return 2 , timer+1, 0
        if sequence == 2 and not up and down and not left and right:
            return 3, timer+1, 0
        if sequence == 3 and actionButton:
            return 0 , timer+1, 1
        else:
            return sequence, timer + 1, 0

    def bZcheck(self, up, down, left, right, actionButton, sequence, timer):
        if timer > self.ZFrames and sequence != 0:
            return 0 , 0, 2
        if sequence == 0 and not up and not down and left and not right:
            return 1 , timer+1, 0
        if sequence == 1 and not up and down and not left and not right:
            return 2 , timer+1, 0
        if sequence == 2 and not up and down and left and not right:
            return 3, timer+1, 0
        if sequence == 3 and actionButton:
            return 0 , timer+1, 1
        else:
            return sequence, timer + 1, 0

    def fHCcheck(self, up, down, left, right, actionButton, sequence, timer):
        if timer > self.HCFrames and sequence != 0:
            return 0 , 0, 2
        if sequence == 0 and not up and not down and left and not right:
            return 1 , timer+1, 0
        if sequence == 1 and not up and down and left and not right:
            return 2 , timer+1, 0
        if sequence == 2 and not up and down and not left and not right:
            return 3 , timer+1, 0
        if sequence == 3 and not up and down and not left and right:
            return 4, timer+1, 0
        if sequence == 4 and not up and not down and not left and right:
            return 5, timer+1, 0
        if sequence == 5 and actionButton:
            return 0, timer+0, 1
        else:
            return sequence, timer+1, 0

    def bHCcheck(self, up, down, left, right, actionButton, sequence, timer):
        if timer > self.HCFrames and sequence != 0:
            return 0 , 0, 2
        if sequence == 0 and not up and not down and not left and right:
            return 1 , timer+1, 0
        if sequence == 1 and not up and down and not left and right:
            return 2 , timer+1, 0
        if sequence == 2 and not up and down and not left and not right:
            return 3 , timer+1, 0
        if sequence == 3 and not up and down and left and not right:
            return 4, timer+1, 0
        if sequence == 4 and not up and not down and left and not right:
            return 5, timer+1, 0
        if sequence == 5 and actionButton:
            return 0, timer+0, 1
        else:
            return sequence, timer+1, 0

    def bHCFcheck(self, up, down, left, right, actionButton, sequence, timer):
        if timer > self.FCFrames and sequence != 0:
            return 0 , 0, 2
        if sequence == 0 and not up and not down and not left and right:
            return 1 , timer+1, 0
        if sequence == 1 and not up and down and not left and right:
            return 2 , timer+1, 0
        if sequence == 2 and not up and down and not left and not right:
            return 3 , timer+1, 0
        if sequence == 3 and not up and down and left and not right:
            return 4, timer+1, 0
        if sequence == 4 and not up and not down and left and not right:
            return 5, timer+1, 0
        if sequence == 5 and not up and not down and not left and right:
            return 6, timer+1, 0
        if sequence == 6 and actionButton:
            return 0, timer+0, 1
        else:
            return sequence, timer+1

    def fHCBcheck(self, up, down, left, right, actionButton, sequence, timer):
        if timer > self.FCFrames and sequence != 0:
            return 0 , 0, 2
        if sequence == 0 and not up and not down and left and not right:
            return 1 , timer+1, 0
        if sequence == 1 and not up and down and left and not right:
            return 2 , timer+1, 0
        if sequence == 2 and not up and down and not left and not right:
            return 3 , timer+1, 0
        if sequence == 3 and not up and down and not left and right:
            return 4, timer+1, 0
        if sequence == 4 and not up and not down and not left and right:
            return 5, timer+1, 0
        if sequence == 5 and not up and not down and left and not right:
            return 6, timer+1, 0
        if sequence == 6 and actionButton:
            return 0, timer+0, 1
        else:
            return sequence, timer+1, 0


    
