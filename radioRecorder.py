# encoding: utf-8
"""
radioRecorder -- record internet radio streams to mp3 files according
to a schedule.
This version works on shows produced daily (e.g. every day from
7PM to 8PM.
It also works on shows with a weekly schedule (e.g. every Friday from
7PM to 10PM
It also works for "weekdays" and "weekends"
requires: python-vlc (pip3 install python-vlc)
I also had to perform a sudo apt-get install vlc on my Ubuntu box
even though I had installed vlc from the Ubuntu software store.
"""

__author__ = "KJ McClaning"
__created__ = "2021-06-03"
__updated__ = "2021-11-10"
__version__ = "0.0.5"

import datetime
import glob
import os
import time

import vlc

# behavior contol flags
# how often do we tell the user what's up?
NOTIFICATION_INTERVAL_SEC = 5

# recording destination
RECORD_DIR = r'/home/kevin/Desktop/radioRecordings'

# a list of radio program descriptors
# name: descriptive string displayed to user
# station: descriptive string displayed to user
# url: source of audio from the Internet
# schedule: a dictionary describing the particular broaccast you want
#   to record.
#    dayOfWeek: can be one of 'everyday', 'mon', 'tue', 'wed',
#               'thu', 'fri', 'sat', 'sun','weekdays','weekends',
#               'everyday',
#     startTimeHM: local time to start recording. Format is HHMM,
#     durationHM: length of recording. Format is HHMM
# startTimeDT: datetime object, generated programmatically. start time
#     for the next recording event
# stopTimeDT: datetime object, generated programmatically. stop time
#     for the next recording event
# currentlyRecordingFlag: boolean, generated programmatically. are we
#     currently recording this audio?
# vlcPlayer': vlc player object, generated programmatically. the vlc object
#     that's currently recording this audio
# vlcMedia': returned from the vlc player initialization, , generated
#     programmatically.
# fileRoot: string used in the base file name. should be unique among
#     all the channels you want to record.
# destDir: destination directory, set to RECORD_DIR,
# currentFQFN': the fully-qualified filename, generated programmatically.
# example:
# radioProgramL = [
#   {   'name': "Weasel's Wild Weekend",
#       'station': "WTMD",
#       'url': r'http://wtmd-ice.streamguys1.com:80/wtmd',
#       'schedule': {
#           'dayOfWeek': 'fri',
#           'startTimeHM': 1850,
#           'durationHM': 320,
#       },
#       'startTimeDT': None,
#       'stopTimeDT': None,
#       'currentlyRecordingFlag': False,
#       'vlcPlayer': None,
#       'vlcMedia': None,
#       'fileRoot': '_WTMD_WWW1_',
#       'destDir': RECORD_DIR,
#       'currentFQFN': None,
#   },
#   {   'name': "Young at Heart",
#       'station': "WTMD",
#       'url': r'http://wtmd-ice.streamguys1.com:80/wtmd',
#       'schedule': {
#           'dayOfWeek': 'sat',
#           'startTimeHM': 750,
#           'durationHM': 120,
#       },
#       'startTimeDT': None,
#       'stopTimeDT': None,
#       'currentlyRecordingFlag': False,
#       'vlcPlayer': None,
#       'vlcMedia': None,
#       'fileRoot': '_WTMD_YAH_',
#       'destDir': RECORD_DIR,
#       'currentFQFN': None,
#    },
# ]
#
# record a show called Weasel's Wild Weekend, from station
# WTMD, from the url given. This show occurs every friday. Start recording
# at HHMM = 1850 (10 minutes early for a 7PM show). The show lasts three
# hours, but but record for HHMM = 0320 to account for starting 10 minutes
# early and ending 10 minutes past when the show is supposed to end.
# The filename will be 20211029_WTMD_WWW_000.mp3 and will be placed in the
# RECORD_DIR directory,
#
# also record a show called Young at Heart from WTMD at the given url.
# This show starts on Saturday morning at 8AM and runs for an hour, but
# start the recording 10 minutes early and run 10 minutes past the end of
# the show. The file name will be 20211030_WTMD_YAH_000.mp3 and will be
# placed in the RECORD_DIR directory,

radioProgramL = [
    {'name': "Yacht Club",
     'station': "WTMD",
     'url': r'http://wtmd-ice.streamguys1.com:80/wtmd',
     'schedule': {
         'dayOfWeek': 'sun',
         'startTimeHM': 1050,
         'durationHM': 220,
     },
     'startTimeDT': None,
     'stopTimeDT': None,
     'currentlyRecordingFlag': False,
     'vlcPlayer': None,
     'vlcMedia': None,
     'fileRoot': '_WTMD_YC_',
     'destDir': RECORD_DIR,
     'currentFQFN': None,
     },

    {'name': "Weasel's Wild Weekend 1",
     'station': "WTMD",
     'url': r'http://wtmd-ice.streamguys1.com:80/wtmd',
     'schedule': {
         'dayOfWeek': 'fri',
         'startTimeHM': 1850,
         'durationHM': 320,
     },
     'startTimeDT': None,
     'stopTimeDT': None,
     'currentlyRecordingFlag': False,
     'vlcPlayer': None,
     'vlcMedia': None,
     'fileRoot': '_WTMD_WWW1_',
     'destDir': RECORD_DIR,
     'currentFQFN': None,
     },

    {'name': "Weasel's Wild Weekend 2",
     'station': "WTMD",
     'url': r'http://wtmd-ice.streamguys1.com:80/wtmd',
     'schedule': {
         'dayOfWeek': 'sat',
         'startTimeHM': 1150,
         'durationHM': 320,
     },
     'startTimeDT': None,
     'stopTimeDT': None,
     'currentlyRecordingFlag': False,
     'vlcPlayer': None,
     'vlcMedia': None,
     'fileRoot': '_WTMD_WWW2_',
     'destDir': RECORD_DIR,
     'currentFQFN': None,
     },

    {'name': "Young at Heart",
     'station': "WTMD",
     'url': r'http://wtmd-ice.streamguys1.com:80/wtmd',
     'schedule': {
         'dayOfWeek': 'sat',
         'startTimeHM': 750,
         'durationHM': 120,
     },
     'startTimeDT': None,
     'stopTimeDT': None,
     'currentlyRecordingFlag': False,
     'vlcPlayer': None,
     'vlcMedia': None,
     'fileRoot': '_WTMD_YAH_',
     'destDir': RECORD_DIR,
     'currentFQFN': None,
     },

    {'name': "Afternoon Drive w Carrie Evans",
     'station': "WTMD",
     'url': r'http://wtmd-ice.streamguys1.com:80/wtmd',
     'schedule': {
         'dayOfWeek': 'weekdays',
         'startTimeHM': 1355,
         'durationHM': 510,
     },
     'startTimeDT': None,
     'stopTimeDT': None,
     'currentlyRecordingFlag': False,
     'vlcPlayer': None,
     'vlcMedia': None,
     'fileRoot': '_WTMD_ADCE_',
     'destDir': RECORD_DIR,
     'currentFQFN': None,
     },

]

# dictionary needed to translate 'mon','tue','wed', etc to
# day of week 0, 1, 2, ...
dOWDict = {
    'mon': 0,
    'tue': 1,
    'wed': 2,
    'thu': 3,
    'fri': 4,
    'sat': 5,
    'sun': 6,
}

# datetime format string, presented to the user
dateTimeFormatS = "%a %Y-%m-%d %H:%M"

# vlc stuff
VLC_VOLUME = 85


def getNewFileName(radioProgramD):
    """
    converts a single radio program dictionary (one element from the
    radioProgramL list) into a suitable filename. handles file name
    confliction by appending a number to the end of the filename
    :param dictionary radioProgramD: radio program dictionary
    :return string newFN: new filename for the recorded audio
    """
    # get current time
    cDT = datetime.datetime.now()
    cDTYYYYHHMM = cDT.strftime('%Y%m%d')

    # search the dest directory for a filename similar to the one
    # we want to generate.
    baseFNGlob = cDTYYYYHHMM + radioProgramD['fileRoot'] + '*.mp3'
    fnGlob = os.path.join(radioProgramD['destDir'], baseFNGlob)
    fnL = glob.glob(fnGlob)

    # generate a new filename, appending an integer to make the new
    # filename unique
    nextIdx = len(fnL)
    newBaseFN = cDTYYYYHHMM + radioProgramD['fileRoot'] + '%03i.mp3' % nextIdx
    newFN = os.path.join(radioProgramD['destDir'], newBaseFN)
    return newFN


def initVLCPlayer(radioProgramD):
    """
    initialize a vlc player object for a radio program
    :param dictionary radioProgramD: radio program dictionary
    (one element from the radioProgramL list)
    :return player,mediaVLC: vlc player and media objects
    """
    # fire up a vlc instance
    instVLC = vlc.Instance()
    player = instVLC.media_player_new()

    # this command string comes from VLC itself. Set up vlc to record
    # the stream, then ask it for an equivalent command string.
    cmdS = "sout=#transcode{vcodec=none,acodec=mp3,ab=128,channels=2,samplerate=44100,scodec=none}:std{access=file{no-overwrite},mux=mp3,dst='%s'}" % \
           radioProgramD['currentFQFN']

    mediaVLC = instVLC.media_new(radioProgramD['url'], cmdS)
    mediaVLC.get_mrl()
    player.set_media(mediaVLC)
    return player, mediaVLC


def calcStartStopDT(radioProgramD):
    """
    calculates the next start and stop times for the passed program
    recording task
    :param dictionary radioProgramD: radio program dictionary
    (one element from the radioProgramL list)
    :return datetime recordStartDT, recordStopDT: the next recording
    start and stop datetimes for this radio program
    """
    # get current datetime
    currentDT = datetime.datetime.now()

    # current day of week, as an integer and string
    currentDTDOWI = currentDT.weekday()
    currentDTDOWS = currentDT.strftime('%a')[0:3].lower()

    # get start Hours and start Minutes
    recordStartH = radioProgramD['schedule']['startTimeHM'] // 100
    recordStartM = radioProgramD['schedule']['startTimeHM'] % 100

    # generate number of seconds to record
    secondsToRecord = (
            3600 * (radioProgramD['schedule']['durationHM'] // 100) +
            60 * (radioProgramD['schedule']['durationHM'] % 100)
    )

    # generate start and stop datetimes if we were to record today
    todaysStartDT = currentDT.replace(
        hour=recordStartH,
        minute=recordStartM,
        second=0,
        microsecond=0,
    )
    todaysStopDT = todaysStartDT + datetime.timedelta(seconds=secondsToRecord)

    # build datetime start and stop times based upon the radio program
    # dictionary entry

    # calculate the number of days in the future this recording
    # will occur. Must accommodate
    #   'everyday', 'weekdays', 'weekends',
    #   'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'

    # if 'everyday'
    if radioProgramD['schedule']['dayOfWeek'] == 'everyday':

        # start recording tomorrow, if it's currently too late
        # to start recording today. If the start time hasn't
        # passed, we can record today.
        if currentDT > todaysStopDT:
            daysInFuture = 1
        else:
            daysInFuture = 0

    # if enumerated day
    elif radioProgramD['schedule']['dayOfWeek'] in [
        'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',
    ]:

        # if we're recording today ..
        if currentDTDOWS == radioProgramD['schedule']['dayOfWeek']:

            # if we're not out of the recording window yet, set day = today
            # else set day = one week from today
            if currentDT > todaysStopDT:
                daysInFuture = 7
            else:
                daysInFuture = 0

        # if we're not recording today, set day to next valid day
        else:
            daysInFuture = (dOWDict[radioProgramD['schedule']['dayOfWeek']] - currentDTDOWI) % 7

    # if 'weekdays'
    elif radioProgramD['schedule']['dayOfWeek'] == 'weekdays':

        # handle each day to account for weekends. if it's sunday, recording
        # starts one day from today. if it's saturday, recording starts
        # two days from today.
        if currentDTDOWS == 'sun':
            daysInFuture = 1

        elif currentDTDOWS == 'sat':
            daysInFuture = 2

        elif currentDTDOWS == 'fri':

            # if today is friday and we're past the recording stop time,
            # set the next recording to be monday (3 days from today),
            # If we're not out of the recording window yet, set day = today
            if currentDT > todaysStopDT:
                daysInFuture = 3
            else:
                daysInFuture = 0

        # mon, tue, wed, thu
        else:
            # if we're not out of the recording window yet, set day = today
            # else set day = tomorrow
            if currentDT > todaysStopDT:
                daysInFuture = 1
            else:
                daysInFuture = 0

    # otherwise assume 'weekends' recording
    else:

        # if 'weekends' and today is a weekend
        if currentDTDOWS in ['sat', 'sun', ]:

            # if we're not out of the recording window yet, set day = today
            # else set day = tomorrow
            if currentDT > todaysStopDT:
                daysInFuture = 1
            else:
                daysInFuture = 0

        # if 'weekends' and today is a weekday, schedule recording for 'sat'
        else:
            daysInFuture = (dOWDict['sat'] - currentDTDOWI) % 7

    # calculate the reording start and end times
    recordStartDT = todaysStartDT + datetime.timedelta(days=daysInFuture)
    recordStopDT = todaysStopDT + datetime.timedelta(days=daysInFuture)

    # return the start and stop recording times for the radio program
    return recordStartDT, recordStopDT


if __name__ == "__main__":

    # it's a forever loop!
    while True:

        # see if it's time to record, or to stop recording.
        # get current datetime in various formats
        currentDT = datetime.datetime.now()
        currentDTHHMM = int(currentDT.strftime('%H%M'))
        currentDTH = int(currentDT.strftime('%H'))
        currentDTM = int(currentDT.strftime('%M'))
        currentDTDOWI = currentDT.weekday()
        currentDTDOWS = currentDT.strftime('%a')[0:2].lower()

        # loop through each program to record
        for thisRadioProgramD in radioProgramL:

            # generate start and stop times in datetime formats, if we
            # aren't currently recording this program
            if not (thisRadioProgramD['currentlyRecordingFlag']):
                thisRadioProgramD['startTimeDT'], thisRadioProgramD['stopTimeDT'] = \
                    calcStartStopDT(thisRadioProgramD)

            # see if we should start recording.
            # Are we in the record window and not recording?
            if (
                    (currentDT >= thisRadioProgramD['startTimeDT']) and
                    (currentDT <= thisRadioProgramD['stopTimeDT']) and
                    not (thisRadioProgramD['currentlyRecordingFlag'])
            ):
                # Set recording flag
                thisRadioProgramD['currentlyRecordingFlag'] = True

                # get new file name
                thisRadioProgramD['currentFQFN'] = getNewFileName(thisRadioProgramD)

                # init the player and start recording
                (
                    thisRadioProgramD['vlcPlayer'],
                    thisRadioProgramD['vlcMedia'],
                ) = initVLCPlayer(thisRadioProgramD)
                thisRadioProgramD['vlcPlayer'].play()

                # inform the user
                S = '%s\n' % currentDT
                S = S + "  Start recording %s - %s ...\n" % (thisRadioProgramD['station'], thisRadioProgramD['name'])
                S = S + "  Ending at %s" % thisRadioProgramD['stopTimeDT']
                print(S)

            # see if we should stop recording.
            # Are we outside the record window and recording?
            if (
                    (currentDT >= thisRadioProgramD['stopTimeDT']) and
                    (thisRadioProgramD['currentlyRecordingFlag'])
            ):
                # Reset recording flag, start and stop DT, and file name
                thisRadioProgramD['currentlyRecordingFlag'] = False
                thisRadioProgramD['startTimeDT'] = None
                thisRadioProgramD['stopTimeDT'] = None
                thisRadioProgramD['currentFQFN'] = None

                # stop recording and reset the player pointers
                thisRadioProgramD['vlcPlayer'].pause()
                thisRadioProgramD['vlcPlayer'].release()

                thisRadioProgramD['vlcPlayer'] = None
                thisRadioProgramD['vlcMedia'] = None

                # generate new start and stop datetimes for the next recording
                # of this program
                time.sleep(0.5)
                thisRadioProgramD['startTimeDT'], thisRadioProgramD['stopTimeDT'] = \
                    calcStartStopDT(thisRadioProgramD)

                # inform the user
                S = '%s\n' % currentDT
                S = S + "  Ceased recording %s - %s ...\n" % (thisRadioProgramD['station'], thisRadioProgramD['name'])
                print(S)

        # inform the user of status
        currentDT = datetime.datetime.now()
        print("-------------------")
        print(currentDT.strftime(dateTimeFormatS))

        for thisRadioProgramD in radioProgramL:
            if thisRadioProgramD['currentlyRecordingFlag']:
                S = "  Active: %s - %s" % (
                    thisRadioProgramD['station'],
                    thisRadioProgramD['name'],
                )
                S = S + " (%s - %s)" % (thisRadioProgramD['startTimeDT'].strftime(dateTimeFormatS),
                                        thisRadioProgramD['stopTimeDT'].strftime(dateTimeFormatS))
                S = S + "\n          -> %s" % os.path.basename(thisRadioProgramD['currentFQFN'])
                print(S)
            else:
                S = '  Queued: %s - %s' % (
                    thisRadioProgramD['station'],
                    thisRadioProgramD['name'],
                )
                S = S + " (%s - %s)" % (
                    thisRadioProgramD['startTimeDT'].strftime(dateTimeFormatS),
                    thisRadioProgramD['stopTimeDT'].strftime(dateTimeFormatS),
                )
                print(S)

        # wait for a while
        time.sleep(NOTIFICATION_INTERVAL_SEC)

# we'll never get here, but I like the assurance
print('Everything is OK')

# ===========================================================================
