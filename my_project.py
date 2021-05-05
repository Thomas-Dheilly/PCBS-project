import random
from expyriment import design, control, stimuli

MIN_WAIT_TIME = 2000
MAX_WAIT_TIME = 3000
MAX_RESPONSE_DELAY = 400
#POSSIBLE_POSITIONS = ((0, 0), (0, 50), (0, -50))

exp = design.Experiment(name="Visual Detection", text_size=40)
control.set_develop_mode(on=True)  ## Set develop mode. Comment out for actual experiment

control.initialize(exp)

blocks = {"right" : "Use your right hand for the next stimuli (press the space bar to start)",
 "left" : "Use your left hand for the next stimuli (press the space bar to start)"}
block = design.Block()
POSSIBLE_POSITIONS = [(189 ,0), (680,0), (1172, 0)] #the possible positions do not correspond to the positions implemented in the original expriment
#assuming 96dpi the right dispositions of the stimuli should be on the horizontal axis in px : +/- (189, 680, 1172)
random.shuffle(POSSIBLE_POSITIONS)
for position in POSSIBLE_POSITIONS:
    t = design.Trial()
    t.set_factor("position", str(position))
    t.add_stimulus(stimuli.Rectangle(size=(33,33), colour=(255,255,255), position = position))
    block.add_trial(t)


#TARGETS=[]
#for position in POSSIBLE_POSITIONS : 
#    stimulus = stimuli.Rectangle(size=(33,33), colour=(255,255,255), position = position[0])
#    TARGETS.append(stimulus)

blankscreen = stimuli.BlankScreen()
#TextBox(text, size, position=None, text_font=None, text_size=None, text_bold=None, text_italic=None, text_underline=None, text_justification=None)
instructions = stimuli.TextScreen("Instructions",
    f"""This experience aims at measuring certain properties of your visual system :

    during the whole experiment, you need to position yourself at 50 cm of
    the screen and close your left eye. 

    From time to time, a rectangle will appear on the horizontal central ligne of the screen.

    Your task is to press a key as quickly as possible using the indicated hand
    when you see it (We measure your reaction-time).

    There will be 2 blocks of {len(POSSIBLE_POSITIONS)} trials in total.

    Press the space bar to start.""", 

    text_size = 18)


exp.add_data_variable_names(['position', 'RT', 'side']) #I have to change the relevant variables
#I have to do 2 blocks with different hands
#autre option pur la boucle en version non optimisée, préparer 6 stimuli à la main, puis les mettre dans une liste, puis la diffuser dans la boucle
### insert here some code to generate the stimuli

control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait()

for side, instruction in blocks.items() : 
    stimuli.TextLine(instruction, text_size = 20).present()
    exp.keyboard.wait()
    for trial in block.trials:
        blankscreen.present()
        waiting_time = random.randint(MIN_WAIT_TIME, MAX_WAIT_TIME)
        exp.clock.wait(waiting_time)
        trial.stimuli[0].present()
        exp.clock.wait(32)
        key, rt = exp.keyboard.wait(duration=MAX_RESPONSE_DELAY)
        exp.data.add([trial.get_factor('position'), rt, side])

### insert here some code to present the stimuli and record responses

control.end()
