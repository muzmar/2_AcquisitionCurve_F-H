# -*- coding: utf-8 -*-
'''
@author: Florian Niefind
@contact: nifflor@googlemail.com
@date: 2014-07-15
'''

#TODO: will there be chinese pictures? yes!
#TODO: Practice Liste brauch ich noch

from psychopy import visual, core, event, gui, data
from random import shuffle
import string, codecs


#===============================================================================
# global variables: INTERFACE
#===============================================================================

PATH = 'Y:/Florian/FaceRecognitionBattery_Andrea/04'
FIXCROSS_SIZE = 40 #size of the fixation cross (the character '+' in Arial)
CHAR_SIZE = 18 #character size for text
OUTPATH = '%s/results/'%(PATH) #output path for storing the results
AVAILABLE_KEYS = ['lctrl', 'rctrl', 'q']
LANGUAGE = 'DE' #which language is the experiment in: 'DE'=German. 'CN'=Chinese
MATCHING = {'lctrl':'left', 'rctrl':'right'} #matching of buttons to answers
SCREEN_SIZE = [1366, 768] #what is your screen resolution?
LANG_FONT_MAP = {'DE':'Courier New', 'CN':'SimSun'} #what font is used for what language?


#===============================================================================
# prepare psychopy
#===============================================================================

#create a window
exp_win = visual.Window(size=SCREEN_SIZE, monitor="testMonitor", color=(230,230,230), colorSpace='rgb255', units=u'pix')

#gather experiment and subject information
exp_name = 'AcquisitionCurve'
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
            trial_order.append(int(line[11])) #trial order
            item_list.append(line[0:8]+line[9:11]) #write entire rest of the line
    return item_list, trial_order

items, trial_order = read_stims('%s/%s/stimuli/Trials_AcquisitionCurve_%s.txt'%(PATH,LANGUAGE,LANGUAGE))


#===============================================================================
# Other preparations
#===============================================================================

#width for text wrapping
wrap_width = SCREEN_SIZE[0]-100
font = LANG_FONT_MAP[LANGUAGE] #font based on language selection

output_file = OUTPATH + exp_info['exp_name'] + '_%02i.txt'%(int(exp_info['Subject']))
rt_clock = core.Clock() #reaction time clock

#fixation cross
fix_cross = visual.TextStim(exp_win, pos=[0, 0], text = '+', font='Arial', color=-1, height=FIXCROSS_SIZE, alignHoriz='center', units=u'pix')


#------------------------------------------------------------------------------
#load instructions and other pictures

try:
    test_end_screen = visual.SimpleImageStim(exp_win, image='%s/%s/Test_End_Screen_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    target_matrix_2 = visual.SimpleImageStim(exp_win, image='%s/%s/Matrix_02_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    attention_screen = visual.SimpleImageStim(exp_win, image='%s/%s/Attention_Screen_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    correct_frame_l = visual.ImageStim(exp_win, image='%s/%s/Correct_Frame.png'%(PATH, LANGUAGE), size= (205, 305), pos =  (-200,0), units=u'pix')
    incorrect_frame_l = visual.ImageStim(exp_win, image='%s/%s/Incorrect_Frame.png'%(PATH, LANGUAGE), size= (205, 305), pos =  (-200,0), units=u'pix')
    correct_frame_r = visual.ImageStim(exp_win, image='%s/%s/Correct_Frame.png'%(PATH, LANGUAGE), size= (205, 305), pos =  (200,0), units=u'pix')
    incorrect_frame_r = visual.ImageStim(exp_win, image='%s/%s/Incorrect_Frame.png'%(PATH, LANGUAGE), size= (205, 305), pos =  (200,0), units=u'pix')
    with codecs.open('%s/%s/Reminder_%s.txt'%(PATH,LANGUAGE,LANGUAGE), 'rb', encoding='utf-8') as infile:
        rem_text = infile.read()
except IOError:
    print 'Error: Language option set to unknown language. Choose DE for German or CN for Chinese.'
    exp_win.close()
    core.quit()

#task question shown again
reminder_screen = visual.TextStim(exp_win, pos=[0, -300], text=rem_text, font=font, color=-1, height=CHAR_SIZE, alignHoriz='center', wrapWidth=wrap_width, units=u'pix')

def match_answer(answer_given, condition):
    '''
    Function to match the answer of the participant with the correct answer.
    '''
    return int(MATCHING.get(answer_given, 'escape') == condition)

#------------------------------------------------------------------------------
# define trial procedure
def run_trials(items, trial_order, practice=False):

    ### NOTE: If one wants a random order each time, uncomment the following two lines
    #trial_order = range(len(items)) #NOTE: initial seed is system time, so it is different each time
    #shuffle(trial_order)

    #dictionary defining the picture position on the screen based on trial info
    position_dict = {'left':(-200,0), 'right':(200,0)}
    position_dict_target = {'left':correct_frame_l, 'right':correct_frame_r}
    position_dict_distractor = {'left':incorrect_frame_r, 'right':incorrect_frame_l}

    trial_count = 1

    #loop through trials
    for i in trial_order:

        item = items[i-1]

        #prepare feedback frames
        target_pos = item[7]
        correct_frame = position_dict_target.get(target_pos, None)
        incorrect_frame = position_dict_distractor.get(target_pos, None)

        #prepare stimulus and draw on screen
        target_pos_px = position_dict.get(target_pos, None)
        distractor_pos_px = tuple([i*-1 for i in target_pos_px]) #by multiplying with -1 the position is mirrored on the screen center
        target = visual.ImageStim(exp_win, image='%s/%s/stimuli/%s'%(PATH, LANGUAGE, item[8]), pos=target_pos_px, units=u'pix')
        distractor = visual.ImageStim(exp_win, image='%s/%s/stimuli/%s'%(PATH, LANGUAGE, item[9]), pos=distractor_pos_px, units=u'pix')

        #pre-stimulus interval
        exp_win.flip() #flip blank screen
        core.wait(1.3) #1300 ms

        #fix_cross
        fix_cross.draw()
        exp_win.flip()
        core.wait(0.2) #200 ms

        #draw to back buffer
        target.draw()
        distractor.draw()
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
        string_output.extend([str(int(practice)),str(ans[-1]), str(match_answer(ans[-1], target_pos)), str(rt)]) #add answer infos
        outfile.write(';'.join(string_output) + '\n') #write to file

        target.draw()
        distractor.draw()
        reminder_screen.draw()
        correct_frame.draw()
        if not match_answer(ans[-1], target_pos): #if answer is wrong
            incorrect_frame.draw()
        exp_win.flip()
        core.wait(1)

        #check if experiment was aborted
        if len(ans) == 2:
            if ans[-2] == 'lctrl' and ans[-1] == 'q':
                exp_win.close()
                core.quit()

        trial_count += 1


#===============================================================================
# experiment
#===============================================================================

#------------------------------------------------------------------------------
# run experiment
with codecs.open(output_file, 'ab', encoding="utf-8") as outfile:

    #write outfile header done in pre-test, this just appends data to existing file

    #capture attention
    attention_screen.draw()
    exp_win.flip()
    core.wait(5.0) #5s

    #run second block
    run_trials(items, trial_order, practice=False)

    #practice end
    test_end_screen.draw()
    exp_win.flip()
    event.waitKeys(keyList=['space'])


exp_win.close()
core.quit()
