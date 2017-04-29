import icalendar
from datetime import datetime
import vobject
import sys
from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC # timezone

def get_test_file(path):
    """
    Helper function to open and read test files.
    """
    filepath = "test_files/{}".format(path)
    if sys.version_info[0] < 3:
        # On python 2, this library operates on bytes.
        f = open(filepath, 'r')
    else:
        # On python 3, it operates on unicode. We need to specify an encoding
        # for systems for which the preferred encoding isn't utf-8 (e.g windows)
        f = open(filepath, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    return text

g = open('test_files/calendar.ics','rb')
gcal = Calendar.from_ical(g.read())
for component in gcal.walk():
    if component.name == "VEVENT":
        x = component.get('summary')
        print x
        y = component.get('dtend')
        print y.dt
        # print component.get('dtend')
        # print component.get('dtstamp')
g.close()




