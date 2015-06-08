# -*- coding: utf-8 -*-
'''
@author: Florian Niefind
@contact: nifflor@googlemail.com
@date: 2014-07-15
'''

from psychopy import visual, core, event, gui, data
from random import shuffle
import string, codecs, sys


# ===============================================================================
# global variables: INTERFACE
# ===============================================================================

# PATH = 'Y:/Florian/FaceRecognitionBattery_Andrea/04/04_tasks_retention'
PATH = "C:\\pythonProjects\\2_AcquisitionCurve_F-H\\1_ACF\\task_retention1"
CHAR_SIZE = 60 #character size for text
OUTPATH = '%s/results/'%(PATH) #output path for storing the results
AVAILABLE_KEYS = ['lctrl', 'rctrl', 'q']
LANGUAGE = 'DE_K' # which language is the experiment in: 'DE'=German. 'CN'=Chinese
MATCHING = {'lctrl':'0', 'rctrl':'1'} #matching of buttons to answers
SCREEN_SIZE = [1366, 768] #what is your screen resolution?
LANG_FONT_MAP = {'DE':'Courier New', 'CN':'SimSun'} #what font is used for what language?
BLOCK_SIZE = 42  # number of trial per block


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

#===============================================================================
# prepare psychopy
#===============================================================================

#create a window
exp_win = visual.Window(size=SCREEN_SIZE, monitor="testMonitor", color=(230,230,230), fullscr=True,
                        colorSpace='rgb255', units=u'pix')

#gather experiment and subject information
exp_name = 'Compare_Letters'
# exp_info = {'Subject': str(sys.argv[1])}
exp_info = {'Subject': str(45)}

#dictionary with additional info about the experiment
exp_info['date'] = data.getDateStr()#add a simple timestamp
exp_info['exp_name'] = exp_name


#===============================================================================
# read stimuli
#===============================================================================

def read_stims(stim_file):
    item_list = []
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
            item_list.append(line)  # write entire rest of the line
    return item_list, file_header


items_letters, header = read_stims('%s/stimuli/Compare_Letters_1.txt'%(PATH))
# Edit header line for using in the output
header[0][0:0] = ["Subject_ID"]
header[0].extend(["ans", "correct", "rt"])

# ===============================================================================
# Other preparations
# ===============================================================================

#width for text wrapping
wrap_width = SCREEN_SIZE[0]-100
font = LANG_FONT_MAP["DE"] #font based on language selection

output_file = OUTPATH + exp_info['exp_name'] + "DE_K" + '_%02i.txt'%(int(exp_info['Subject']))
rt_clock = core.Clock() # reaction time clock

#------------------------------------------------------------------------------
#load instructions and other pictures
instructions = []
try:
    for i in range(6):
        num = str(i+1)
        image_name = "1Vergleichen_Kinder_fin_Kl_0" + num
        instructions.append(Image(image_name).buffer())

except IOError:
    print 'Error: Language option set to unknown language. Choose DE for German or CN for Chinese.'
    exp_win.close()
    core.quit()

def match_answer(answer_given, condition):
    '''
    Function to match the answer of the participant with the correct answer.
    lctrl: different
    rctrl: same
    '''
    return int(MATCHING.get(answer_given, 'escape') == condition)

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

        target_left = visual.TextStim(exp_win, pos=[-200, 0], text=''.join(item[3:6]), font=font, color=-1,
                                      height=CHAR_SIZE, alignHoriz='center', wrapWidth=wrap_width, units=u'pix')
        target_right = visual.TextStim(exp_win, pos=[200, 0], text=''.join(item[6:]), font=font, color=-1,
                                       height=CHAR_SIZE, alignHoriz='center', wrapWidth=wrap_width, units=u'pix')

        #pre-stimulus interval
        exp_win.flip() #flip blank screen
        core.wait(0.5) #500 ms

        #draw to back buffer
        target_left.draw()
        target_right.draw()
        #present
        exp_win.flip()

        #start reaction time clock and collect answer
        rt_clock.reset()
        ans = event.waitKeys(keyList=AVAILABLE_KEYS)

        #get reaction time
        rt = rt_clock.getTime()
        rt *= 1000

        item.extend([str(ans[-1]), str(match_answer(ans[-1], item[2])), str(rt)])
        outfile.write(exp_info['Subject'] + ";" + ";".join(item) + ";" + "\n")

        #write out answers
        #string_output = [exp_info['Subject'], str(trial_count)] #initialize output list: subject ID, trial number (in exp)
        #string_output.extend([str(x) for x in item]) #add trial infos
        #string_output.extend([str(ans[-1]), str(match_answer(ans[-1], item[2])), str(rt)]) #add answer infos
        #outfile.write(';'.join(string_output) + '\n') #write to file

        #check if experiment was aborted
        if len(ans) == 2:
            if ans[-2] == 'lctrl' and ans[-1] == 'q':
                exp_win.close()
                core.quit()

        # check for quit
        if ans[-1] == "q":
            core.quit()


#===============================================================================
# experiment
#===============================================================================

#------------------------------------------------------------------------------
# present instructions
for ii in range(6):
    instructions[ii].draw()
    exp_win.flip()
    event.waitKeys(keyList=['space'])

#------------------------------------------------------------------------------
# run experiment
with open(output_file, 'w') as outfile:
    outfile.write(";".join(header[0]) + "\n")
    #run trials
    run_trials(items_letters, 1, BLOCK_SIZE)

exp_win.close()
core.quit()