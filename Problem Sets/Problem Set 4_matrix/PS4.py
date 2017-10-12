import time

start = time.time()

'''
This script calls all scripts necessary to read & clean the PS4 data as well
as create payoff functions and run the optimization routine

input: None

output: prints results of optimization routines
'''

exec(open("./read_data.py").read())

exec(open("./counter_fact.py").read())

exec(open("./distance.py").read())

exec(open("./payoff_func.py").read())

exec(open("./max_score.py").read())

exec(open("./optimization.py").read())
