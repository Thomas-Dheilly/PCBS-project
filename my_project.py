import random
from expyriment import design, control, stimuli

MIN_WAITING_TIME = 2000
MAX_WAITING_TIME = 3000
MAX_RESPONSE_DELAY = 400


exp = design.Experiment(name="Visual detection of stimuli in impaired position/hand conditions", text_size=40)
control.set_develop_mode(on=True)  

control.initialize(exp)


block = design.Block()
POSSIBLE_POSITIONS = [(50,0), (200,0), (300, 0), (-50, 0), (-200,0), (-300, 0)]*5
random.shuffle(POSSIBLE_POSITIONS)
for position in POSSIBLE_POSITIONS:
    t = design.Trial()
    t.set_factor("position", str(position))
    t.add_stimulus(stimuli.Rectangle(size=(33,33), colour=(255,255,255), position = position))
    block.add_trial(t)


hands_instructions = {"right" : "Use your right hand for the next stimuli (press the space bar to start)",
 "left" : "Use your left hand for the next stimuli (press the space bar to start)"}

blankscreen = stimuli.BlankScreen()

general_instructions = stimuli.TextScreen("Instructions",
    f"""This experience aims at measuring certain properties of your visual system :

    during the whole experiment, you need to position yourself at 50 cm of
    the screen and close your left eye. 

    From time to time, a rectangle will appear on the horizontal central ligne of the screen.

    Your task is to press a key as quickly as possible using the indicated hand
    when you see it (We measure your reaction-time).

    There will be 2 blocks of {len(POSSIBLE_POSITIONS)} trials in total.

    Press the space bar to start.""", 

    text_size = 18)


exp.add_data_variable_names(['position', 'RT', 'side'])

control.start(skip_ready_screen=True)
general_instructions.present()
exp.keyboard.wait()

for side, instruction in hands_instructions.items() : 
    stimuli.TextLine(instruction, text_size = 20).present()
    exp.keyboard.wait()
    for trial in block.trials:
        blankscreen.present()
        waiting_time = random.randint(MIN_WAITING_TIME, MAX_WAITING_TIME)
        exp.clock.wait(waiting_time)
        trial.stimuli[0].present()
        exp.clock.wait(32)
        key, rt = exp.keyboard.wait(duration=MAX_RESPONSE_DELAY)
        exp.data.add([trial.get_factor('position'), rt, side])


control.end()
