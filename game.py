import heapq
from event_handler import EventBase, EventNothing, EventFridge, EventCourse, EventPhd

class Game:
    def __init__(self):
        self.day : int = 1
        self.worked_days : int = 0
        self.max_day : int = 500
        self.event_queue : heapq[EventBase] = []
        self.current_event : EventBase = None
        self.started_new_event : bool = False
        self.progress : float = 0
        self.next_print : str = ""
        self.log_filename : str = "game.log"
        self.is_running : bool = False

    def start_game(self):
        self.__init__()
        with open(self.log_filename, "w") as f:
            f.write("Log file\n")
        self.init_queue()
        self.is_running = True
        self.add_to_print("Welcome to our game!")
        self.add_to_print()
        self.add_to_print("Starting today, you are a new PhD student @ QPIT. "+
                          "During the next 1000 days, your job is managing your time to complete your PhD studies. "+
                          "Each day, you have to work on your project, take courses, and complete the tasks from DTU Fysik. "+
                          "Don't forget to spend some time having fun otherwise your stress level will increase and you'll risk burn out. ")
        self.add_to_print("Will you be able to complete all your goals and graduate in time?")
        self.add_to_print()
        self.add_to_print("Good luck!")
        return self.get_print()
    
    def init_queue(self):
        heapq.heappush(self.event_queue, (1, EventCourse()))
        heapq.heappush(self.event_queue, (10, EventFridge()))
        heapq.heappush(self.event_queue, (20, EventPhd()))

    def advance_game(self, choice):
        self.process_previous_day_choice(choice)
        self.add_to_print(f"Day {self.day}:")
        completed = EventFridge.getProgressCount() + EventCourse.getProgressCount() + EventPhd.getProgressCount()
        total = len(EventFridge._listTasks) + len(EventCourse._listTasks) + len(EventPhd._listTasks)
        self.progress = completed/total
        self.add_to_print(f"Progress: {int(self.progress*100)}%")
        #self.add_to_print(f"Progress Project: {int(EventFridge.getProgressCount()/len(EventFridge._listTasks)*100)}%")
        #self.add_to_print(f"Progress Study: {int(EventCourse.getProgressCount()/len(EventCourse._listTasks)*100)}%")
        #self.add_to_print(f"Progress PhD tasks: {int(EventPhd.getProgressCount()/len(EventPhd._listTasks)*100)}%")
        self.add_to_print()
        if self.day < self.max_day and self.progress<1:
            self.run_day()
        else:
            self.end_game()
        return self.get_print()
    
    def process_previous_day_choice(self, choice):
        if not self.current_event:
            return
        self.update_current_and_next_events(choice)
        self.advance_days(choice)

    def run_day(self):
        if not len(self.event_queue):
            # add random nothing event
            heapq.heappush(self.event_queue, (self.day, EventNothing()))
        if self.current_event and self.current_event.duration>0:
            raise Exception("This should not happen because I'm skipping the empty days")
        # see if you have events to do today
        scheduled_day, event = heapq.heappop(self.event_queue)
        if scheduled_day > self.day:
            self.current_event = EventNothing(duration=scheduled_day-self.day)
            heapq.heappush(self.event_queue, (scheduled_day, event))
            
            self.add_to_print(f"{self.current_event.text}")
            self.add_to_print()
            self.add_to_print(f"Accept task ({self.current_event.duration} days):")
            self.add_to_print(f"{self.current_event.option1}")
            self.add_to_print(f"Reschedule task ({self.current_event.duration} days):")
            self.add_to_print(f"{self.current_event.option2}")
        else:
            self.current_event = event
            self.started_new_event = True
            self.add_to_print(f"{self.current_event.text}")
            self.add_to_print()
            self.add_to_print(f"Accept task ({self.current_event.duration} days):")
            self.add_to_print(f"{self.current_event.option2}")
            self.add_to_print(f"Reschedule task:")
            alt_message = f"{self.current_event.option1}"
            if len(self.event_queue):
                next_day, next_event = heapq.heappop(self.event_queue)
                heapq.heappush(self.event_queue, (next_day, next_event))
                if next_day <= self.day:
                    alt_message =f"Reschedule the task and check the other tasks for today."
            self.add_to_print(alt_message)
        
        #self.add_to_print("You are still working on the current task.")
        #self.add_to_print(f"Daily task:")
        #self.add_to_print(f"Skip forward until the end of the task ({self.current_event.duration} days)")
        #self.add_to_print(f"Alternative:")
        #self.add_to_print(f"Advance to tomorrow")

    def update_current_and_next_events(self,choice:int):
        if not self.started_new_event:
            return
        try:
            if choice == 1:
                next_event = self.current_event.selectOption1()
                next_scheduled_day = self.day + self.current_event.wait1
                # remove current event because I'm rescheduling it
                self.current_event = None
            else:
                next_event = self.current_event.selectOption2()
                next_scheduled_day = self.day + self.current_event.duration + self.current_event.wait2
            heapq.heappush(self.event_queue, (next_scheduled_day, next_event))
        except:
            pass
        finally:
            self.started_new_event = False

        
    def advance_days(self, choice:int):
        # If I still have an active event, fast forward until the end of the event
        if self.current_event and self.current_event.duration>0:
            self.day += self.current_event.duration
            if self.current_event.type != EventBase.EventType.NOTHING:
                self.worked_days += self.current_event.duration
            self.current_event.duration = 0

    def end_game(self):
        self.add_to_print("You have finished your PhD!")
        self.add_to_print(f"You have worked for {self.worked_days}/{self.day} days.")
        fridgeCompleted = EventFridge.getProgressCount() >= len(EventFridge._listTasks)
        courseCompleted = EventCourse.getProgressCount() >= len(EventCourse._listTasks)
        phdCompleted = EventPhd.getProgressCount() >= len(EventPhd._listTasks)
        if fridgeCompleted:
            self.add_to_print("You have completed all the project tasks!")
        else:
            self.add_to_print("You have not completed all the project tasks!")
        if courseCompleted:
            self.add_to_print("You have completed all the courses!")
        else:
            self.add_to_print("You have not completed all the courses!")
        if phdCompleted:
            self.add_to_print("You have completed all the PhD mandatory tasks!")
        else:
            self.add_to_print("You have not completed all the PhD mandatory tasks!")
        if fridgeCompleted and courseCompleted and phdCompleted:
            self.add_to_print("You have successfully graduated!")
        else:
            self.add_to_print("...")
            self.add_to_print("You couldn't graduate in time. Your academic life is over.")
        self.is_running = False

    def add_to_print(self, text=""):
        self.next_print += text + "\n"

    def get_print(self):
        # TODO manage html tags
        to_print = self.next_print
        with open(self.log_filename, "a") as f:
            f.write(to_print)
        self.next_print = ""
        return to_print
    


if __name__ == "__main__":
    game = Game()
    mes = game.start_game()
    print(mes)
    count=0
    while game.day<game.max_day and game.progress<1:
        print(game.get_print())
        #choice = input("Enter choice: ")
        choice = 2
        count += 1
        mes = game.advance_game(int(choice))
        print(mes)
    print(count)
    