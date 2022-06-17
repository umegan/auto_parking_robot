def calculate_path(distance_to_mark, turned_theta):
    import numpy as np
    path_x = distance_to_mark * np.cos(turned_theta)
    path_y = distance_to_mark * np.sin(turned_theta)
    return path_x,path_y

print(" git teset")