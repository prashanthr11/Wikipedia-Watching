import json
from sseclient import SSEClient as EventSource
from collections import defaultdict
from collections import deque
from datetime import *


class Weekly_Reports:
    """
    A Class to store the previous domains reports and users reports.
    """

    def __init__(self, domains=None, user=None):
        self.domains = domains
        self.users = user


url = 'https://stream.wikimedia.org/v2/stream/revision-create'


def print_user_report(minutes, reports):
    """
    Template for printing Users Report.
    """
    start = 0 if minutes <= 5 else minutes - 5
    end = minutes
    tmp = defaultdict(int)  # Temporary dictionary for storing the users values (edit count).
    print("Minute {0} Report - Minute {1}-{2} date\n".format(end, start, end))
    print("Users who made changes to en.wikipedia.org")
    print("-----------------------------------")
    print(''' Users Report ''')
    for i in reports:  # For Each report from the past 5 reports
        for v in i.users:  # For user in the report
            tmp[v] = max(tmp[v], i.users[v])

    # Sorting the data on values(Edit count).
    for k, v in sorted(tmp.items(), key=lambda v: v[1], reverse=True):
        if v != 0:
            print("{0}: {1}".format(k, v))

    print("-----------------------------------")


def print_domain_report(minutes, reports):
    """
    Template for printing Domains Report.
    """
    start = 0 if minutes <= 5 else minutes - 5
    end = minutes
    tmp = defaultdict(int)
    print("Minute {0} Report - Minute {1}-{2} date\n".format(end, start, end))
    for i in reports:  # For each report from the last 5 reports
        for v in i.domains:  # Iterate through the domains which are updated on each report.
            tmp[v] = max(tmp[v], i.domains[v])

    print(f'Total number of Wikipedia Domains Updated: {len(tmp)} \n')
    print("-----------------------------------")
    print(''' Domains Report ''')

    # Sorting the dictionary on unique pages updated.
    for k, v in sorted(tmp.items(), key=lambda v: v[1], reverse=True):
        print("{0}: {1} pages updated".format(k, v))

    print("-----------------------------------")


def helper(change):
    """
    This function takes the json file as input and return the the list which consists of name of the domain, userid,
    title of the page updated.
    User name and edit count will be returned only when the user is not bot and the domain is en.wikipedia.org. Only, In
    this occassion, function returns list of length 5. which includes userid, title of the page, domain name, user name
    and the edit count.
    """
    required = ["meta", "performer"]
    title, pid = change["page_title"], change["page_id"]

    for i in required:
        x = change[i]
        try:
            if i == 'meta':
                domain = x['domain']
            elif i == 'performer':
                name, Isbot, edit_cnt = x['user_text'], x['user_is_bot'], x['user_edit_count']
                if not Isbot and domain == 'en.wikipedia.org':
                    return [pid, title, domain, name,
                            edit_cnt]  # Only when The user in not bot and he edited en.wikipedia.org domain.
        except KeyError:
            pass

    return [pid, title, domain]


def found(d, domain, pid, title):
    """
    This function Returns True only when there are no duplicates in the domain at d. In other words, Either the id or the
    title of the page is present in the domain[d] which is already updated is ignored.
    """
    for k, v in domain[d]:
        if k == pid or v == title:
            return False

    return True


def generate_report():
    """
    This function returns the two dictionaries, domains and users.
    First, we iterate through each event till 1 minute. For each event, we update the domain count and the user
    edit counts (iff domain is en.wikipedia.org). If we encounter multiple users or page titles in the same domain
    we ignore this entry.
    """
    domain, user = defaultdict(set), defaultdict(int)
    now = datetime.now()
    for event in EventSource(url):  # Iterating through the events in the url.
        tmp = datetime.now() - now
        if tmp.seconds > 60:  # If we exceed one minute just return the domains and users dictionaries.
            for i in domain:
                domain[i] = len(domain[i])  # Converting the values of the dictionaries to the length of the set.
            return (domain, user)
        if event.event == 'message':
            try:
                change = json.loads(event.data)
                res = helper(change)  # converting json file to the list with the required fields in json file.
                if len(res) == 3:  # only when user is bot or domain is not en.wikipedia.org
                    pid, title, d = res
                else:
                    pid, title, d, name, cnt = res
                    user[name] = max(user[name], cnt)  # update the users dicti0nary with the maximum edit counts.

                if found(d, domain, pid, title):  # if the user id or the title of the page is already present in the
                    # same domain.
                    domain[d].add((pid, title))
            except ValueError:
                pass

    return (domain, user)


def main():
    minutes_cnt = 0
    reports = deque()
    limit = 10  # Time in minutes
    limit *= 60  # Converting limit to seconds
    now = datetime.now()  # Store present time

    while True:
        tmp = datetime.now() - now
        if tmp.seconds > limit:
            break  # When we exceed the limit which is 5 minutes in this case
        domain, user = generate_report()
        reports.append(Weekly_Reports(domain, user))
        while len(
                reports) > 5:  # There is no need to store the previous data, as we are only concerned with the past 5
            # minutes. So, we just remove the unused data.
            reports.popleft()

        minutes_cnt += 1
        print_user_report(minutes_cnt, reports)  # function for generating the users report.
        print_domain_report(minutes_cnt, reports)  # function for generating the domains report.

    print("End of Report!!")
    

if __name__ == '__main__':
    main()