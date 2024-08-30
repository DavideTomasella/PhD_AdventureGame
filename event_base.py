from abc import ABC, abstractmethod
from enum import Enum
import json
from random import randint

class EventBase(ABC):
    class EventType(Enum):
        NOTHING = 0
        FRIDGE = 1
        COURSE = 2
        PHD = 3
        LIFE = 4

    @staticmethod
    def getEventType(type):
        if type == "NOTHING":
            return EventBase.EventType.NOTHING
        elif type == "FRIDGE":
            return EventBase.EventType.FRIDGE
        elif type == "COURSE":
            return EventBase.EventType.COURSE
        elif type == "PHD":
            return EventBase.EventType.PHD
        elif type == "LIFE":
            return EventBase.EventType.LIFE
        else:
            return None


    def __init__(self, type : EventType, **kwargs):
        self.type = type
        self.group = kwargs["group"]
        self.text = kwargs["text"]
        self.option1 = kwargs["option1"]
        self.option2 = kwargs["option2"]
        self.duration = kwargs["duration"]
        self.wait1 = kwargs["wait1"]
        self.wait2 = kwargs["wait2"]

    @abstractmethod
    def selectOption1(self):
        pass

    @abstractmethod
    def selectOption2(self):
        pass

    def __lt__(self, other : 'EventBase'):
        return self.duration < other.duration
        
class EventNothing(EventBase):
    _listTasks : list[dict] = json.load(open("tasksNothing.json"))

    def __init__(self):
        super().__init__(EventBase.EventType.NOTHING, **EventNothing._listTasks[randint(0, len(EventNothing._listTasks)-1)])
    
    def selectOption1(self):
        return EventNothing()
    
    def selectOption2(self):
        return EventNothing()

class EventFridge(EventBase):
    #read from json file
    _listTasks : list[dict] = json.load(open("tasksFridge.json"))

    _progressFridge = 0

    @staticmethod
    def getProgressCount():
        return EventFridge._progressFridge
    
    @staticmethod
    def addProgress():
        EventFridge._progressFridge += 1
    
    def __init__(self):
        super().__init__(EventBase.EventType.FRIDGE, **EventFridge._listTasks[EventFridge._progressFridge])

    def selectOption1(self):
        return EventFridge()
    
    def selectOption2(self):
        EventFridge.addProgress()
        return EventFridge()
        
class EventCourse(EventBase):
    _listTasks : list[dict] = json.load(open("tasksCourse.json"))

    _progressCourse = 0

    @staticmethod
    def getProgressCount():
        return EventCourse._progressCourse
    
    @staticmethod
    def addProgress():
        EventCourse._progressCourse += 1
    
    def __init__(self):
        super().__init__(EventBase.EventType.COURSE, **EventCourse._listTasks[EventCourse._progressCourse])

    def selectOption1(self):
        return EventCourse()
    
    def selectOption2(self):
        EventCourse.addProgress()
        return EventCourse()
    
class EventPhd(EventBase):
    _listTasks : list[dict] = json.load(open("tasksPhd.json"))

    _progressPhd = 0

    @staticmethod
    def getProgressCount():
        return EventPhd._progressPhd
    
    @staticmethod
    def addProgress():
        EventPhd._progressPhd += 1
    
    def __init__(self):
        super().__init__(EventBase.EventType.PHD, **EventPhd._listTasks[EventPhd._progressPhd])

    def selectOption1(self):
        return EventPhd()
    
    def selectOption2(self):
        EventPhd.addProgress()
        return EventPhd()