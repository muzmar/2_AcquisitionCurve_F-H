# -*- coding: utf-8 -*-
'''
@author: Florian Niefind
@contact: nifflor@googlemail.com
@date: 2014-07-15
'''

#TO DO: will there be chinese pictures? yes!
#TO DO: Practice Liste brauch ich noch
#TO DO: wrap width in allen exp überdenken!!!

from psychopy import visual, core, event, gui, data
from random import shuffle
import string, codecs, sys


#===============================================================================
# global variables: INTERFACE
#===============================================================================

# PATH = 'D:/Forschung/Tests/____TASKs_FACEProject/___Reprogramming/vonFlorian/vonFlorian/FaceRecognitionBattery_Andrea/04'
PATH = "C:\\pythonProjects\\2_AcquisitionCurve_F-H\\1_ACF"
FIXCROSS_SIZE = 40  # size of the fixation cross (the character '+' in Arial)
CHAR_SIZE = 18  # character size for text
OUTPATH = '%s/results/'%(PATH)  # output path for storing the results
AVAILABLE_KEYS = ['lctrl', 'rctrl', 'q']
LANGUAGE = 'DE_K'  # which language is the experiment in: 'DE'=German. 'CN'=Chinese
MATCHING = {'lctrl':'left', 'rctrl':'right'} #matching of buttons to answers
SCREEN_SIZE = [1366, 768]  # what is your screen resolution?
LANG_FONT_MAP = {'DE': 'Courier New', 'CN': 'SimSun'}  # what font is used for what language?


class Image():  # class that creates ....

    def __init__(self, name, **kwargs):

        # ** if the format of images are different(ie. .png, .jpg, .gif) give the complete name with extension and
        # remove the ".png" from self.path
        # :param name: name of the image
        # :param type: can be "load", "arrow", "questionMark", "questionLoad"
        # :return:

        self.path = '{0}/instructions/{1}/{2}.png'.format(PATH, LANGUAGE, name)
        if 'loc' in kwargs:
            self.loc = kwargs['loc']

    def buffer(self, **kwargs):

        buffer_image = visual.ImageStim(exp_win, image=self.path, units=u'pix')
        if 'factor' in kwargs:
            buffer_image.setSize(kwargs['factor'], '*')
        return buffer_image
# ===============================================================================
# prepare psychopy
# ===============================================================================

# create a window
exp_win = visual.Window(size=SCREEN_SIZE, monitor="testMonitor", color=(230, 230, 230), fullscr=True,
                        colorSpace='rgb255', units=u'pix')

# gather experiment and subject information
exp_name = 'AcquisitionCurve'
# exp_info = {'Subject': str(sys.argv[1])}
exp_info = {'Subject': str(45)}

# dictionary with additional info about the experiment
exp_info['date'] = data.getDateStr()  # add a simple timestamp
exp_info['exp_name'] = exp_name

# ===============================================================================
# read stimuli
# ===============================================================================


def read_stims(stim_file):
    item_list = []
    trial_order = []  # order of the trials in the experiment (hard-coded in the trial file)
    file_header = []
    with codecs.open(stim_file, 'rb', encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if '###' in line:  # its the header
                line = line.split(';')
                file_header.append(line[0:len(line)-1])
                continue
            elif len(line) == 0:  # last line if an empty one
                break
            line = line.split(';')
            trial_order.append(int(line[11]))  # trial order
            item_list.append(line[0:8]+line[9:11])  # write entire rest of the line
    return item_list, trial_order, file_header

practice_items, practice_trial_order, prac_header = read_stims(
    '%s/stimuli/PracticeTrials_AcquisitionCurve_Faces.txt'%(PATH))
# Edit header line for using in the output
# header[0][0:0] = ["Subject_ID"]
# header[0].extend(["ans", "correct", "rt"])

# ===============================================================================
# Other preparations
# ===============================================================================

# width for text wrapping
wrap_width = SCREEN_SIZE[0]-100
font = LANG_FONT_MAP["DE"]  # font based on language selection

output_file = OUTPATH + exp_info['exp_name'] + 'DE_K' + '_%02i.txt'%(int(exp_info['Subject']))
rt_clock = core.Clock()  # reaction time clock

# fixation cross
fix_cross = visual.TextStim(exp_win, pos=[0, 0], text='+', font='Arial', color=-1, height=FIXCROSS_SIZE,
                            alignHoriz='center', units=u'pix')


# ------------------------------------------------------------------------------
# load instructions and other pictures
instructions = []
try:
    for i in range(12):
        num = str(i+1)
        image_name = "AC_F_1_0" + num
        instructions.append(Image(image_name).buffer())

    instructions.append(Image("Matrixen_Gesichter_01").buffer())

    correct_frame_l = visual.ImageStim(exp_win, image='{0}/instructions/{1}/Correct_Frame.png'.format(PATH, LANGUAGE),
                                       size=(205, 305), pos =  (-200,0), units=u'pix')
    incorrect_frame_l = visual.ImageStim(exp_win, image='{0}/instructions/{1}/Incorrect_Frame.png'.format(PATH, LANGUAGE),
                                         size=(205, 305), pos =  (-200,0), units=u'pix')
    correct_frame_r = visual.ImageStim(exp_win, image='{0}/instructions/{1}/Correct_Frame.png'.format(PATH, LANGUAGE),
                                       size=(205, 305), pos =  (200,0), units=u'pix')
    incorrect_frame_r = visual.ImageStim(exp_win, image='{0}/instructions/{1}/Incorrect_Frame.png'.format(PATH, LANGUAGE),
                                         size=(205, 305), pos =  (200,0), units=u'pix')

    # instr_screen_1 = visual.SimpleImageStim(exp_win, image='%s/%s/Instruction_Screen_1_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    # instr_screen_2 = visual.SimpleImageStim(exp_win, image='%s/%s/Instruction_Screen_2_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    # practice_start_screen = visual.SimpleImageStim(exp_win, image='%s/%s/Practice_Start_Screen_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    # practice_matrix = visual.SimpleImageStim(exp_win, image='%s/%s/Practice_Matrix_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    # target_matrix = visual.SimpleImageStim(exp_win, image='%s/%s/Matrix_01_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    # attention_screen = visual.SimpleImageStim(exp_win, image='%s/%s/Attention_Screen_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    # practice_end_screen = visual.SimpleImageStim(exp_win, image='%s/%s/Practice_End_Screen_%s.png'%(PATH, LANGUAGE, LANGUAGE))
    # correct_frame_l = visual.ImageStim(exp_win, image='%s/%s/Correct_Frame.png'%(PATH, LANGUAGE), size= (205, 305), pos =  (-200,0), units=u'pix')
    # incorrect_frame_l = visual.ImageStim(exp_win, image='%s/%s/Incorrect_Frame.png'%(PATH, LANGUAGE), size= (205, 305), pos =  (-200,0), units=u'pix')
    # correct_frame_r = visual.ImageStim(exp_win, image='%s/%s/Correct_Frame.png'%(PATH, LANGUAGE), size= (205, 305), pos =  (200,0), units=u'pix')
    # incorrect_frame_r = visual.ImageStim(exp_win, image='%s/%s/Incorrect_Frame.png'%(PATH, LANGUAGE), size= (205, 305), pos =  (200,0), units=u'pix')
    with codecs.open('%s/Reminder_DE.txt'%(PATH), 'rb', encoding='utf-8') as infile:
        rem_text = infile.read()
except IOError:
    print 'Error: Language option set to unknown language. Choose DE for German or CN for Chinese.'
    exp_win.close()
    core.quit()

# task question shown again
reminder_screen = visual.TextStim(exp_win, pos=[0, -300], text=rem_text, font=font, color=-1,
                                  height=CHAR_SIZE, alignHoriz='center', wrapWidth=wrap_width, units=u'pix')


def match_answer(answer_given, condition):
    '''
    Function to match the answer of the participant with the correct answer.
    '''
    return int(MATCHING.get(answer_given, 'escape') == condition)

# ------------------------------------------------------------------------------
# define trial procedure


def run_trials(items, trial_order, practice=False):

    # ## NOTE: If one wants a random order each time, uncomment the following two lines
    # trial_order = range(len(items)) #NOTE: initial seed is system time, so it is different each time
    # shuffle(trial_order)

    # dictionary defining the picture position on the screen based on trial info
    position_dict = {'left': (-200,0), 'right': (200,0)}
    position_dict_target = {'left': correct_frame_l, 'right': correct_frame_r}
    position_dict_distractor = {'left': incorrect_frame_r, 'right': incorrect_frame_l}

    trial_count = 1

    # loop through trials
    for i in trial_order:

        item = items[i-1]

        # prepare feedback frames
        target_pos = item[7]
        correct_frame = position_dict_target.get(target_pos, None)
        incorrect_frame = position_dict_distractor.get(target_pos, None)

        # prepare stimulus and draw on screen
        target_pos_px = position_dict.get(target_pos, None)
        distractor_pos_px = tuple([i*-1 for i in target_pos_px])  # by multiplying with -1 the position is mirrored on the screen center
        target = visual.ImageStim(exp_win, image='%s/stimuli/%s'%(PATH, item[8]),
                                  pos=target_pos_px, units=u'pix')
        distractor = visual.ImageStim(exp_win, image='%s/stimuli/%s'%(PATH, item[9]),
                                      pos=distractor_pos_px, units=u'pix')

        # pre-stimulus interval
        exp_win.flip()  # flip blank screen
        core.wait(1.3)  # 1300 ms

        # fix_cross
        fix_cross.draw()
        exp_win.flip()
        core.wait(0.2)  # 200 ms

        # draw to back buffer
        target.draw()
        distractor.draw()
        reminder_screen.draw()
        # present
        exp_win.flip()

        # start reaction time clock and collect answer
        rt_clock.reset()
        ans = event.waitKeys(keyList=AVAILABLE_KEYS)

        # get reaction time
        rt = rt_clock.getTime()
        rt *= 1000

        if not practice:
            item.extend([str(ans[-1]), str(match_answer(ans[-1], item[6])), str(rt)])
            # outfile.write(exp_info['Subject'] + ";" + ";".join(item) + ";" + "\n")

        target.draw()
        distractor.draw()
        reminder_screen.draw()
        correct_frame.draw()

        if not match_answer(ans[-1], target_pos):  # if answer is wrong
            incorrect_frame.draw()
        exp_win.flip()
        core.wait(1)

        # check if experiment was aborted
        if len(ans) == 2:
            if ans[-2] == 'lctrl' and ans[-1] == 'q':
                exp_win.close()
                core.quit()

        # check for quit
        if ans[-1] == "q":
            core.quit()

        trial_count += 1


# ===============================================================================
# experiment
# ===============================================================================

# ------------------------------------------------------------------------------
# present instructions
for ii in range(9):
    instructions[ii].draw()
    exp_win.flip()
    event.waitKeys(keyList=['space'])

# ------------------------------------------------------------------------------
# run experiment

# show matrix with target faces
instructions[9].draw()
exp_win.flip()
core.wait(20.0)  # 20s

run_trials(practice_items, practice_trial_order, practice=True)

# stop Image
instructions[10].draw()
exp_win.flip()
event.waitKeys(keyList=['space'])

# blank
exp_win.flip()
core.wait(0.5)

# capture attention
instructions[11].draw()
exp_win.flip()
core.wait(5.0)  # 5s

# run practice trials
# run_trials(practice_items, practice_trial_order, practice=True)


# show matrix with target faces
instructions[-1].draw()
exp_win.flip()
core.wait(60.0)  # 45s

exp_win.close()
core.quit()
