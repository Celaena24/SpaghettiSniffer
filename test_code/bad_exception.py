try:
    something()
except:
    something_else()
    
try:
    the_right_way()
except ValueError as e:
    catch_the_right_way(e)