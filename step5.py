from importlib.resources import path
from re import X



def move_to_mark(path_x, path_y, turned_theta,distance_to_mark):
    count=1
    while(count!=0):
        if(count==1):
            turn_right(turned_theta)
            if(can_move()==True):
                count+=1
    
            elif(count==2):
                move_forward(path_x)
                if(can_move()==True):
                    count+=1
            elif(count==3):
                turnleft(90)
                if(can_move()==True):
                    count+=1            
            elif(count==4):
                move_forward(path_y)
                count==0
    return True
