
class spaceship:
    def __init__(self, posX, posY):
        self.estimatedBoostPower = 2 # [N]
        self.estimatedMass = 1000 # [kg]
        self.measuredX = posX
        self.measuredY = posY
        self.measuredVelocity = 0 # [m/s]
        self.measuredAngle = 0 # [rad] 

    def newTransmission(self, posX, posY):
        self.measuredX = posX
        self.measuredY = posY

if __name__ == '__main__':
    pass