import random
from expyriment import design, control, stimuli

N_TRIALS = 3
MIN_WAIT_TIME = 2000
MAX_WAIT_TIME = 3000
MAX_RESPONSE_DELAY = 400

exp = design.Experiment(name="Visual Detection", text_size=40)
control.set_develop_mode(on=True)  ## Set develop mode. Comment out for actual experiment

control.initialize(exp)
target = stimuli.Rectangle(size=(33,33), colour=(255,255,255), position=None)
blankscreen = stimuli.BlankScreen()
#TextBox(text, size, position=None, text_font=None, text_size=None, text_bold=None, text_italic=None, text_underline=None, text_justification=None)
instructions = stimuli.TextScreen("Instructions",
    f"""From time to time, a rectangle will appear on the horizontal central ligne of the screen.

    Your task is to press a key as quickly as possible when you see it (We measure your reaction-time).

    There will be {N_TRIALS} trials in total.

    Press the space bar to start.""", 

    text_size = 30)

exp.add_data_variable_names(['trial', 'wait', 'respkey', 'RT'])
### insert here some code to generate the stimuli

control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait()

for i_trial in range(N_TRIALS):
    blankscreen.present()
    waiting_time = random.randint(MIN_WAIT_TIME, MAX_WAIT_TIME)
    exp.clock.wait(waiting_time)
    target.present()
    exp.clock.wait(32)
    key, rt = exp.keyboard.wait(duration=MAX_RESPONSE_DELAY)
    exp.data.add([i_trial, waiting_time, key, rt])

### insert here some code to present the stimuli and record responses

control.end()
