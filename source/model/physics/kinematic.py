class kinematic():
    """
    expected inputs:
           [timeX]                                   [a_x]
    time = [timeY] = time_common [s], acceleration = [a_y] [m/s**2]
           [timeZ]                                   [a_z]
    
               [veloX]                   [x]
    velocity = [veloY] [m/s], position = [y] [m]
               [veloZ]                   [z]
    
    Note:
    - Add jerk
    - Add angular position, -velocity, -acceleration, tangular velocity
    """


    def velocity2position(velocity, time, position=0):
        #print('Kinematic velocity2position: x=%f.1, y=%f.1, z=%f.1' %(position[0,0],position[1,0],position[2,0]))
        return velocity * time + position

    def acceleration2velocity(acceleration, time, velocity=0):
        #print('Kinematic acceleration2velocity: x=%f.1, y=%f.1, z=%f.1' %(velocity[0,0], velocity[1,0], velocity[2,0]))
        return acceleration * time + velocity

    def acceleration2position( acceleration, time, velocity=0, position=0):
        return kinematic.acceleration2velocity(acceleration, time, velocity) * time + position
    
    def positions2velocity(previousPosition, currentPosition, deltaTime):
        return (currentPosition - previousPosition)/deltaTime