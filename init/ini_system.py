import ConfigParser, uuid
import datetime, os

config = ConfigParser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.
config.add_section('Station')
config.set('Station', 'lat', '4.450127')
config.set('Station', 'long', '-75.198839')
config.set('Station', 'h_sonar', '689') #676;715      # distance to zero water's mm
# First datetime
now = str(datetime.datetime.now())
config.set('Station', 'ini_date', now)
# make a UUID based on the host ID and current time
key = uuid.uuid1()
config.set('Station', 'uuid', str(key))      # station key
# sysyem path
config.set('Station','path_sys',str(os.getcwd()))

# Writing our configuration file to 'init.cfg'
with open('init.cfg', 'wb') as configfile:
    config.write(configfile)
