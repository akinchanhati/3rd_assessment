"""
Bug Fix Task #4 – Support Ticket SLA Breach Checker (Medium–High)

Scenario:
You have raw support tickets exported as text lines.

Format:
<TICKET_ID>|<priority>|<created_hh:mm>|<first_response_hh:mm>|<status>

priority: P1, P2, P3
status: OPEN or CLOSED

SLA (first response max minutes):
P1: 15 minutes
P2: 60 minutes
P3: 240 minutes

Rules:
- If first_response is '-' then treat as not responded yet, count as SLA breached.
- Only consider tickets with status OPEN.
- Print:
  - total_open
  - breached_open
  - unique_priorities_in_breach
  - top_priority_breaches (priority with most breaches)

This file includes intentional bugs. Fix them.
"""

import re

RAW = """
T1001|P1|10:00|10:10|OPEN
T1002|P2|09:00|10:30|OPEN
T1003|P3|08:00|-|OPEN
T1004|P1|11:00|11:40|CLOSED
T1005|P2|12:00|12:30|OPEN
T1006|P1|13:00|13:20|OPEN
BAD|ROW
""".strip()

SLA = {"P1": 15, "P2": 60, "P3": 240}

class TicketError(Exception):
    pass

class InvalidTicket(TicketError):
    pass

def to_minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)

def parse_ticket(line):
    # BUG: priority pattern too loose, status misspelled
    pat = r"^(T\d+)\|(P\d)\|(\d{2}:\d{2})\|([\d:-]{1,5})\|(OPNE|CLOSED)$"
    #solution
    pat = r"^(T\d+)\|(P[1-3])\|(\d{2}:\d{2})\|(\d{2}:\d{2}|-)\|(OPEN|CLOSED)$"
    m = re.match(pat, line.strip())
    if not m:
        raise InvalidTicket("Invalid ticket row")
    return {
        "id": m.group(1),
        "priority": m.group(2),
        "created": m.group(3),
        "first_response": m.group(4),
        "status": m.group(5),
    }

def is_breached(t):
    """
    Return True if breached based on SLA.
    """
    if t["first_response"] == "-":
        # return False # BUG: should be breached
        return True    # Solution
    
    # BUG: time diff direction wrong
    # diff = to_minutes(t["created"]) - to_minutes(t["first_response"])
    # Solution
    diff = to_minutes(t["first_response"]) - to_minutes(t["created"])
    
    if diff < 0: 
        return False
    
    return diff > SLA.get(t["priority"], 0)

def top_key(counter):
    if not counter:
        return None
    # BUG: returns wrong key due to sorting by key not value
    # return sorted(counter.keys())[-1]
    # Solution
    max_count = max(counter.values())
    for key in counter:
        if counter[key] == max_count:
            return key

def main():
    total_open = 0
    breached_open = 0
    priorities = set()
    breach_counts = {}
    invalid = 0

    for line in RAW.split("\n"):
        try:
            t = parse_ticket(line)
        except InvalidTicket:
            invalid += 1
            continue

        if t["status"] != "OPEN":
            continue

        total_open += 1

        if is_breached(t):
            breached_open += 1
            priorities.add(t["priority"])
            breach_counts[t["priority"]] = breach_counts.get(t["priority"], 0) + 1

    print("=== SLA BREACH REPORT ===")
    print("Total Open:", total_open)
    print("Breached Open:", breached_open)
    print("Unique Priorities in Breach:", len(priorities))
    print("Top Priority Breaches:", top_key(breach_counts))
    print("Invalid Lines:", invalid)

if __name__ == "__main__":
    main()
