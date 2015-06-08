# -*- coding: utf-8 -*-
'''
@author: Florian Niefind
@contact: nifflor@googlemail.com
@date: 2014-07-15
'''

from psychopy import visual, core, event, gui, data
from random import shuffle
import string, codecs, sys

#===============================================================================
# global variables: INTERFACE
#===============================================================================

PATH = 'Y:/Florian/FaceRecognitionBattery_Andrea/04/04_tasks_retention'
CHAR_SIZE = 60 #character size for text
OUTPATH = '%s/results/'%(PATH) #output path for storing the results
AVAILABLE_KEYS = ['1','2','3','4','5','6','7','8','9','lctrl','q']
LANGUAGE = 'DE' #which language is the experiment in: 'DE'=German. 'CN'=Chinese
SCREEN_SIZE = [1366, 768] #what is your screen resolution?
LANG_FONT_MAP = {'DE':'Courier New', 'CN':'SimSun'} #what font is used for what language?
BLOCK_SIZE = 42 # number of trial per block

#===============================================================================
# prepare psychopy
#===============================================================================

#create a window
exp_win = visual.Window(size=SCREEN_SIZE, monitor="testMonitor", color=(230,230,230), colorSpace='rgb255', units=u'pix')

#gather experiment and subject information
exp_name = 'Replace DigSym'
exp_info = {'Subject':str(sys.argv[1])}

#dictionary with additional info about the experiment
exp_info['date'] = data.getDateStr()#add a simple timestamp
exp_info['exp_name'] = exp_name


#===============================================================================
# read stimuli
#===============================================================================


def read_stims(stim_file):
    item_list = []
    trial_order = [] #order of the trials in the experiment (hard-coded in the trial file)
    with codecs.open(stim_file, 'rb', encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if '###' in line: #its the header
                continue
            elif len(line) == 0: #last line if an empty one
                break
            line = line.split(';')
            item_list.append(line)
    return item_list

items_digits = read_stims('%s/%s/stimuli/1_Detect_Digits_%s.txt'%(PATH,LANGUAGE,LANGUAGE))

#===============================================================================
# Other preparations
#===============================================================================

#width for text wrapping
wrap_width = SCREEN_SIZE[0]-100
font = LANG_FONT_MAP[LANGUAGE] #font based on language selection

output_file = OUTPATH + exp_info['exp_name'] + '_%02i.txt'%(int(exp_info['Subject']))
rt_clock = core.Clock() #reaction time clock

#------------------------------------------------------------------------------
#load instructions and other pictures

try:
    instr_screen_1 = visual.SimpleImageStim(exp_win, image='%s/%s/Replace_DigSym_I1_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    instr_screen_2 = visual.SimpleImageStim(exp_win, image='%s/%s/Replace_DigSym_I2_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    instr_screen_3 = visual.SimpleImageStim(exp_win, image='%s/%s/Replace_DigSym_I3_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    instr_screen_4 = visual.SimpleImageStim(exp_win, image='%s/%s/Replace_DigSym_I4_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    reminder_screen = visual.SimpleImageStim(exp_win, image='%s/%s/DigSym_Map.png'%(PATH, LANGUAGE), pos = [0,-200])
    putmap_screen_1 = visual.SimpleImageStim(exp_win, image='%s/%s/Replace_DigSym_PutMap1_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    putmap_screen_2 = visual.SimpleImageStim(exp_win, image='%s/%s/Replace_DigSym_PutMap2_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    clearmap_screen = visual.SimpleImageStim(exp_win, image='%s/%s/Clear_Map_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    keyboard_screen = visual.SimpleImageStim(exp_win, image='%s/%s/Keyboard_Settings_Replace_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    end_screen = visual.SimpleImageStim(exp_win, image='%s/%s/End_Screen_%s.png'%(PATH, LANGUAGE, LANGUAGE))
except IOError:
    print 'Error: Language option set to unknown language. Choose DE for German or CN for Chinese.'
    exp_win.close()
    core.quit()

def match_answer(answer_given, condition):
    '''
    Function to match the answer of the participant with the correct answer.
    '''
    return int(answer_given == condition)

#------------------------------------------------------------------------------
# define trial procedure
def run_trials(items, block_id, block_size):
    '''
    @param list items: the item list as returned by read_stims
    @param int block_id: which block of the item list is run?
    @param int block_size: how many trials are in a block?
    '''

    #loop through trials
    for trial_count in xrange(1,block_size+1):

        item = items[(block_id * trial_count)-1]

        target = visual.TextStim(exp_win, pos=[0, 0], text=item[3], font=font, color=-1, height=CHAR_SIZE, alignHoriz='center', wrapWidth=wrap_width, units=u'pix')

        #pre-stimulus interval
        exp_win.flip() #flip blank screen
        core.wait(0.5) #500 ms

        #draw to back buffer
        target.draw()
        reminder_screen.draw()
        #present
        exp_win.flip()

        #start reaction time clock and collect answer
        rt_clock.reset()
        ans = event.waitKeys(keyList=AVAILABLE_KEYS)

        #get reaction time
        rt = rt_clock.getTime()

        #write out answers
        string_output = [exp_info['Subject'], str(trial_count)] #initialize output list: subject ID, trial number (in exp)
        string_output.extend([str(x) for x in item]) #add trial infos
        string_output.extend([str(ans[-1]), str(match_answer(ans[-1], item[2])), str(rt)]) #add answer infos
        outfile.write(';'.join(string_output) + '\n') #write to file

        #check if experiment was aborted
        if len(ans) == 2:
            if ans[-2] == 'lctrl' and ans[-1] == 'q':
                exp_win.close()
                core.quit()


#===============================================================================
# experiment
#===============================================================================

#------------------------------------------------------------------------------
# present instructions
# this time it is possible to page backwards and forwards through the instructions
instructions_list = [keyboard_screen, instr_screen_1, putmap_screen_1, putmap_screen_2, instr_screen_2, instr_screen_3]
page_count = 0

while page_count < len(instructions_list):
    instructions_list[page_count].draw()
    exp_win.flip()
    ans = event.waitKeys(keyList=['lctrl','rctrl'])
    if ans[-1] == 'rctrl': #move forward in instructions
        page_count += 1
    elif ans[-1] == 'lctrl' and page_count > 0: #move backwards if not first page
        page_count -= 1

#------------------------------------------------------------------------------
# run experiment
with codecs.open(output_file, 'wb', encoding="utf-8") as outfile:

    #write outfile header
    #outfile.write('### Experiment: %s\n### Subject ID: %s\n### Date: %s\n\n' %(exp_info['exp_name'], exp_info['Subject'], exp_info['date']))
    outfile.write('subject_id;trial;block;trial_id;target;stimulus;ans;correct;rt\n') #header

    #run trials
    run_trials(items_digits, 1, BLOCK_SIZE)
    
    instr_screen_4.draw()
    exp_win.flip()
    event.waitKeys(keyList=['space'])
    
    run_trials(items_digits, 1, BLOCK_SIZE)

end_screen.draw()
exp_win.flip()
event.waitKeys()

exp_win.close()
core.quit()
