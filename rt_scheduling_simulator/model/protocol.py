from enum import Enum

class Protocol(str, Enum):
    # no deadlock avoidance strategy is used
    NONE = 'none'
    # priority ceiling protocol is used
    PCP = 'pcp'
    # priority inheritance protocol is used
    PIP = 'pip'