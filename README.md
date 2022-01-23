
# Purpose

Uses python-vlc to record Internet radio streams. You can record shows produced:
* daily - Every day from 7PM to 8PM.
* weekly - Every Friday from 7PM to 10PM.
* weekends and weekdays - Sat and Sun from 4PM to 6:30 PM, or Mon - Fri from 6AM to 10AM

You specify a directory to be the destination for the recordings (e.g. /home/user/Desktop/My Radio Recordings) and
a list of dictionaries which describe the programs you'd like to record. Each dictionary
contains the keys:

* name - a human-readable string describing the particular program. 
* station - another human-readable string for the user
* url - the url of broadcast
* schedule - a dictionary describing the schedule of this partupresented to the user
    * dayOfWeek: one of 'everyday', 'mon', 'tue', 'wed', 'thu', 'fri', 
      'sat', 'sun','weekdays','weekends', or 'everyday'
    * startTimeHM: an integer describing the local time to start recording. The format is
        HHMM. For example, the integer 0830 is 8:30AM, while the integer 1345 is
        1:45PM
    * durationHM: the length of recording. Same format as startTimeHM e.g. 
        320 records for 3 hours and 20 minutes.

Each list entry in the radio program list (radioProgramL) also contains several
programmatically-generated variables. They are:
* startTimeDT: datetime object, generated programmatically. The start time
    for the next recording event
* stopTimeDT: datetime object, generated programmatically. The stop time
    for the next recording event
* currentlyRecordingFlag: boolean, generated programmatically. Are we
    currently recording this audio?
* vlcPlayer: vlc player object, generated programmatically. The vlc object
    that's currently recording this audio
* vlcMedia: returned from the vlc player initialization, generated
    programmatically.
* fileRoot: A user-entered string used in the base file name. This string should 
   be unique among all the channels you want to record.
* destDir: destination directory, programatically set to RECORD_DIR,
* currentFQFN: The fully-qualified filename to which the audio is being recorded. This 
   string is generated programmatically at the start of recording.

# Example

Let's say you want to record two shows:

* Weasel's Wild Weekend, from station WTMD, from the url 'http://wtmd-ice.streamguys1.com:80/wtmd'
This show airs every Friday from 7PM to 10PM. We'd like to start recording
10 minutes before the show starts and end 10 minutes after the show finishes, 
so we set the start time to 1900 and the duration to 320 (3 hours for the 
show and an extra 20 minutes to account for starting 10 minutes early and 
recording for 10 minutes after the show ends. We want each recorded file
to be marked with the string "_WTMD_WWW_" so we enter that string in 
the `fileRoot` key. If the show records on Oct 29, 2021, the 
file name will be "20211029_WTMD_WWW_000.mp3" and will be placed in the directory 
specified by the RECORD_DIR directory
* Young at Heart, also from WTMD at the same url. This show starts on 
Saturday morning at 8AM and runs for an hour. We'd also like to start recording
10 minutes early and record for 10 minutes over. We want the file to be marked with 
"_WTMD_YAH_". If the show records on Oct 30, 2021, the file name will 
be 20211030_WTMD_YAH_000.mp3 in the RECORD_DIR directory,

The user fills in the `radioProgramL` list  as follows:
```python
RECORD_DIR = r'/home/user/Desktop/radioRecordings'
radioProgramL = [
    {  'name': "Weasel's Wild Weekend",
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
       'fileRoot': '_WTMD_WWW_',
       'destDir': RECORD_DIR,
       'currentFQFN': None,
   },
   {   'name': "Young at Heart",
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
]
```

# Installation

This program requires the python-vlc plug-in: `pip install python-vlc`

# Use 

Fill in the `RECORD_DIR` and `radioProgramL` variables with the appropriate 
data. Optionally, edit the `NOTIFICATION_INTERVAL_SEC` variable to set how
often the program wakes up to check the time and take action. 

# Notes

The three-digit number at the end of the filename (e.g. the 000 in 
20211029_WTMD_WWW_000.mp3) accounts for Internet outages during a recording. 
If the Internet connection goes down and restarts, the integer will 
increment to avoid overwriting previously-recorded material.

# Contributions

Contributions are welcome.  Feel free to make feature requests in the issues.
