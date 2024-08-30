import heapq
from event_base import EventBase, EventNothing, EventFridge, EventCourse, EventPhd

class Game:
    def __init__(self):
        self.day : int = 0
        self.workedDays : int = 0
        self.eventQueue : heapq[EventBase] = []
        self.currentEvent : EventBase = None
        self.initQueue()

    def initQueue(self):
        heapq.heappush(self.eventQueue, (1, EventCourse()))
        heapq.heappush(self.eventQueue, (10, EventFridge()))
        heapq.heappush(self.eventQueue, (20, EventPhd()))

    def runDay(self):
        while not self.currentEvent or self.currentEvent.duration<=0:
            # see if you have events to do today
            if not len(self.eventQueue):
                # add random event
                heapq.heappush(self.eventQueue, (self.day, EventNothing()))
            scheduled_day, event = heapq.heappop(self.eventQueue)
            if scheduled_day > self.day:
                self.currentEvent = EventNothing()
                heapq.heappush(self.eventQueue, (scheduled_day, event))
            else:
                self.currentEvent = event
                new_scheduled_day, new_event = self.runEvent()
                heapq.heappush(self.eventQueue, (new_scheduled_day, new_event))
        self.currentEvent.duration -= 1

    def runEvent(self):
        print(f"{self.currentEvent.text}")
        print(f"Option 1: {self.currentEvent.option1}")
        print(f"Option 2: {self.currentEvent.option2}")
        #get user input
        sel = self.get_user_input()
        if sel == 1:
            try:
                newEvent = self.currentEvent.selectOption1()
            except:
                newEvent = EventNothing()
            return (self.day + self.currentEvent.wait1, newEvent)
        else:
            try:
                newEvent = self.currentEvent.selectOption2()
            except:
                newEvent = EventNothing()
            return (self.day + self.currentEvent.duration + self.currentEvent.wait2, newEvent)
        
    def get_user_input(self):
        ins = "2"#input("Select your option: ")
        if ins == "1":
            return 1
        elif ins == "2":
            return 2
        else:
            print("Invalid input")
            return self.get_user_input()
        
    def mainLoop(self):
        self.day += 1
        print(f"Day {self.day}:")
        self.runDay()
        if self.currentEvent.type != EventBase.EventType.NOTHING:
            self.workedDays += 1
            print("Well done: you have worked hard today!")
        else:
            print("Nothing to do today: you can enjoy life and the danish weather!")

        print(f"Progress Project: {int(EventFridge.getProgressCount()/len(EventFridge._listTasks)*100)}%")
        print(f"Progress Study: {int(EventCourse.getProgressCount()/len(EventCourse._listTasks)*100)}%")
        print(f"Progress PhD tasks: {int(EventPhd.getProgressCount()/len(EventPhd._listTasks)*100)}%")


if __name__ == "__main__":
    game = Game()
    while True:
        game.mainLoop()
        if game.day > 200:
            break
    print("You have finished your PhD!")
    print(f"You have worked for {game.workedDays}/{game.day} days.")
    fridgeCompleted = EventFridge.getProgressCount() >= len(EventFridge._listTasks)
    courseCompleted = EventCourse.getProgressCount() >= len(EventCourse._listTasks)
    phdCompleted = EventPhd.getProgressCount() >= len(EventPhd._listTasks)
    if fridgeCompleted:
        print("You have completed all the project tasks!")
    else:
        print("You have not completed all the project tasks!")
    if courseCompleted:
        print("You have completed all the courses!")
    else:
        print("You have not completed all the courses!")
    if phdCompleted:
        print("You have completed all the PhD mandatory tasks!")
    else:
        print("You have not completed all the PhD mandatory tasks!")
    if fridgeCompleted and courseCompleted and phdCompleted:
        print("You have successfully graduated!")
    else:
        print("...")
        print("You couldn't graduate in time. Your academic life is over.")

