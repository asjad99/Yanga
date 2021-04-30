# coding: utf-8

import pdb
import json
import time
import re
import sys
import pandas as pd
from optparse import OptionParser
import datetime
import os
from pytz import timezone


#BALANCER IPS
balancer_ips = ["104.200.23.105"]


import csv
csvfile = open('sorted_events.csv', 'wb')
csvfilewriter = csv.writer(csvfile)
csvfilewriter.writerow(["UserID", "SongID", "AlbumID", "ArtistID", "TimeStamp", "UNIXTIME", "SessionID"])

def apply_blocklist_policy(li, cutoff_time=10):
    """

    :param li:
    :param cutoff_time:
    :return:
    """
    clean_list = []
    policy_violating_users = set([])
    policy_violating_ips = set([])
    current_item = None

    current_window = []
    remainder_window = []

    # while moving through all the operations
    for elem in li:
        # For common user initiated actions
        (_et, _user, _, _, _, _dt, _ip) = elem
        if not (_et in ('trackPlaybackEnded', 'startTrackPlayback', \
                        'trackShared', 'trackFavorite', 'playlistSavePopupOpen')):
            continue
        #Structure of current item (user_id, time, element, whitelisted)
        current_item = [_user, _dt, list(elem), True]
        # Add the initiated action into a window
        current_window.append(current_item)

        #Get Remainder Items from previous current_window
        remainder_window = [x for x in current_window if (current_item[1] - x[1]).total_seconds() >= cutoff_time]

        # And remove items not within the cutoff time
        current_window = [x for x in current_window if (current_item[1] - x[1]).total_seconds() < cutoff_time]

        # Find all the users that execute double the number of actions as there are seconds
        users_in_current_window = [x[0] for x in current_window if x[0] is not None]

        # Find all ips of unregistered users that execute double the number of actions as there are seconds
        unreg_ips_in_current_window = [x[2][6] for x in current_window if \
                                            x[0] is None \
                                            and x[2][6] != "UNKNOWN" \
                                            and x[2][6] not in balancer_ips]

        violator_users = set([x for x in set(users_in_current_window) \
                              if users_in_current_window.count(x) > cutoff_time * 1])

        violator_ips = set([x for x in set(unreg_ips_in_current_window) \
                              if unreg_ips_in_current_window.count(x) > cutoff_time * 1])

        for i in xrange(len(current_window)):
            if current_window[i][0] in violator_users:
                current_window[i][3] = False
            if current_window[i][2][6] in violator_ips:
                current_window[i][3] = False

        #if violator_users:
        #    print [(x, users_in_current_window.count(x)) for x in violator_users]

        # Update these violators to a global list
        policy_violating_users.update(violator_users)
        policy_violating_ips.update(violator_ips)

        #Update Clean List with events by clean users in window
        clean_list += [x[2] for x in remainder_window if x[3] == True]
    clean_list += [x[2] for x in current_window if x[3] == True]


    # And return all the input records that do not violate policy
    #print(repr(policy_violators))
    clean_list_daily_ban = [x for x in li if x[1] not in policy_violating_users]
    print len(clean_list_daily_ban), len(clean_list)
    return (clean_list, policy_violating_users, policy_violating_ips)


def insert_into_mongo(event, criteria, criteria_value, count, date):
    (year, month, day) = (date[0], date[1], date[2])
    search_criteria = {"year": year, "month": month, "day": day, "label": None,\
        "criteria": criteria, "criteria_value": criteria_value, "event": event}
    inserted_id = None
    if True:

        pass

def panda_stash_dates(dates, base_path):
    for date in dates:
        date = date.split("-")
        date_list = [int(x) for x in date]

        print "Running against BasePath %s and Date %s"%(base_path, date)

        #base_path = "/Users/afrobeard/Scratch/pataridbfiles"
        #date = (2015, 3, 11)

        date1 = datetime.datetime(year = date_list[0], month = date_list[1], day = date_list[2], tzinfo=PAK_TIME)
        date2 = datetime.datetime(year = date_list[0], month = date_list[1], day = date_list[2], tzinfo=PAK_TIME)-datetime.timedelta(days=1)
        test_files = ["events-%(year)d-%(month)02d-%(day)02d.json"%    {'year': x.year,'month': x.month, 'day': x.day}    for x in (date2, date1)]
        test_files = [os.path.join(base_path, x) for x in test_files]
        test_files = filter(lambda x: os.path.exists(x), test_files)


        li = []
        i = 0

        checkpoint = time.time()
        for test_file in test_files:
            with open(test_file) as f:
                for line in f:
                    i += 1
                    line = re.sub(r'transaction_id.*exc_info', 'exc_info', line)
                    d = {}
                    try:
                        d = json.loads(line)
                    except:
                        continue
                    tags = d.get('tags')
                    if type(tags) != type({}):
                        try:
                            tags = json.loads(tags)
                        except:
                            continue
                    event_type = tags.get('eventtype')
                    if event_type in ('trackPlaybackEnded',):
                        artist = tags.get('artist')
                        album = tags.get('album')
                        user = tags.get('user')
                        song = tags.get('song')
                        ts = d.get('timestamp')
                        ip = d.get('client')
                        date = datetime.datetime.fromtimestamp(int(ts), tz=PAK_TIME)
                        if date.day == date_list[2]:
                            li.append((event_type, user, song, artist, album, date, ip))

        print "Time elapsed in Load Routine 1: Parse json and dates %d"%(time.time()-checkpoint)
        print "There are %d relevant events in the processing pipeline out of %d lines" % (len(li), i)

        (li, violating_users, violating_ips) = apply_blocklist_policy(li)

        print "After removing blocklisted users this count comes down to {}".format(len(li))

        print "Violating Users", repr(violating_users)
        print "Violating IPS", repr(violating_ips)

        #print "I'm exiting before I hit the database"
        #return None

        if len(li) == 0:
            print "Nothing to do here. "
            continue

        unzipped_li = zip(*li)
        d = {"$event": unzipped_li[0], "$user": unzipped_li[1], "$song": unzipped_li[2],     "$artist": unzipped_li[3], "$album": unzipped_li[4], "$date": unzipped_li[5]}

        checkpoint = time.time()
        df = pd.DataFrame(d)
        print "Time elapsed in Load Routine 2: Dataframing %d"%(time.time()-checkpoint)


        print "Unspecified users %d"%len(df[df['$user'] != df['$user']])
        print "Unspecified albums %d"%len(df[df['$album'] != df['$album']])
        print "Unspecified artists %d"%len(df[df['$artist'] != df['$artist']])

        event_counts = df.groupby(['$event', '$user'])

        import uuid
        def new_session_id():
            return str(uuid.uuid4())



        for user_events in event_counts:
            (group_headers, user_events_data) = user_events
            user_id = group_headers[1]
            event_type = group_headers[0]
            user_events_list = zip(user_events_data['$date'], user_events_data['$song'], user_events_data['$album'], user_events_data['$artist'])
            user_events_list.sort()

            user_events_list = [[user_id, uel[1], uel[2], uel[3], uel[0], time.mktime(uel[0].to_datetime().timetuple()), None]
                                    for uel in user_events_list]

            t = None
            for i in xrange(len(user_events_list)):
                user_events_item = user_events_list[i]
                if t is None:
                    t = user_events_item[5]
                    session_id = new_session_id()
                    user_events_item[6] = session_id
                else:
                    time_delta = user_events_item[5] - t
                    if time_delta < 10*60:
                        user_events_list[i][6] = user_events_list[i-1][6]
                    else:
                        session_id = new_session_id()
                        user_events_list[i][6] = session_id
                        pass
                    t = user_events_item[5]

            for entry in user_events_list:
                csvfilewriter.writerow(entry)
        print "I'm having a cold beer now. I've earned it"

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--date", dest="date",
                      help="Date to compute e.g. 2015-3-11")
    parser.add_option("-t", "--todate", dest="todate",
                      help="Inclusion makes it a date range")
    parser.add_option("-b", "--basepath", dest="basepath",
                      help="Path to base", metavar="PATH")

    (options, args) = parser.parse_args()

    if not(options.basepath) or not(options.date):
        print "use -h for options"
        exit(0)

    dates = None
    base_path = options.basepath
    if(options.todate):
        dates = []
        (f_y, f_m, f_d) = [int(x) for x in options.date.split("-")]
        (t_y, t_m, t_d) = [int(x) for x in options.todate.split("-")]
        from datetime import date, timedelta as td
        f_dobj = datetime.date(f_y, f_m, f_d)
        t_dobj = datetime.date(t_y, t_m, t_d)
        d_dobj = t_dobj - f_dobj
        for i in xrange(d_dobj.days + 1):
            c_dobj = f_dobj + datetime.timedelta(days=i)
            dates.append("%d-%d-%d"%(c_dobj.year, c_dobj.month, c_dobj.day))
        print repr(dates)

    else:
        dates = options.date.split(",")

    panda_stash_dates(dates, base_path)
