"""Module using finite state machine model for life simulation"""
import random


def decor(fn):
    """Decorator for coroutines"""
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper


class Life:
    """Class for life simulation"""
    def __init__(self):
        self.start = self._create_start()
        self.work = self._create_work()
        self.sleep = self._create_sleep()
        self.eat = self._create_eat()
        self.funny_night = self._create_funny_night()
        self.deadline_coming = self._create_deadline_coming()
        self.lesson = self._create_lesson()
        self.relax = self._create_relax()

        self.hour = 0
        self.total_time = 0

        self.current_state = self.start
        self.stopped = False

    def send(self, event):
        self.current_state.send((event, self.hour))
        if self.total_time % 24 == 0:
            print("\n" + "New day: " + str(self.total_time//24))
        self.total_time += 1
        self.hour = (self.hour + 1) % 24

    @decor
    def _create_start(self):
        while True:
            event = yield
            self.current_state = self.sleep

    @decor
    def _create_work(self):
        phrase = "Working..."
        while True:
            event = yield
            print(str(self.hour) + ":00\t" + str(phrase))
            if event[0] == 'BURNING DEADLINE':
                self.current_state = self.deadline_coming
            elif event[0] == None and 2 <= event[1] <= 6:
                self.current_state = self.sleep
            elif event[0] == "Exam tomorrow!":
                self.current_state = self.funny_night
            elif event[0] == "Lesson":
                self.current_state = self.lesson
            elif event[1] in [7,11,20,24]:
                self.current_state = self.eat
            elif 19 <= event[1] <= 21:
                self.current_state = self.relax
            else:
                self.current_state = self.work

    @decor
    def _create_relax(self):
        phrase = "Whoa, relaxing!"
        while True:
            event = yield
            print(str(self.hour) + ":00\t" + str(phrase))
            if event[0] == 'BURNING DEADLINE':
                self.current_state = self.deadline_coming
            elif event[0] == None and 2 <= event[1] <= 6:
                self.current_state = self.sleep
            elif event[0] == "Exam tomorrow!":
                self.current_state = self.funny_night
            elif event[0] == "Lesson":
                self.current_state = self.lesson
            elif event[1] in [7, 11, 20, 24]:
                self.current_state = self.eat
            elif 18 <= event[1] <= 20:
                self.current_state = self.relax
            else:
                self.current_state = self.work

    @decor
    def _create_sleep(self):
        phrase = "Sleeping"
        while True:
            event = yield
            print(str(self.hour) + ":00\t" + str(phrase))
            if event[0] == 'BURNING DEADLINE':
                self.current_state = self.deadline_coming
            elif event[0] == None and 2 <= event[1] <= 6:
                self.current_state = self.sleep
            elif event[0] == "Exam tomorrow!":
                self.current_state = self.funny_night
            elif event[0] == "Lesson":
                self.current_state = self.lesson
            elif event[1] in [7,11,20,24]:
                self.current_state = self.eat
            else:
                self.current_state = self.work

    @decor
    def _create_eat(self):
        phrase = "Eating"
        while True:
            event = yield
            print(str(self.hour) + ":00\t" + str(phrase))
            if event[0] == 'BURNING DEADLINE':
                self.current_state = self.deadline_coming
            elif event[0] == None and 1 <= event[1] <= 6:
                self.current_state = self.sleep
            elif event[0] == "Exam tomorrow!":
                self.current_state = self.funny_night
            elif event[0] == "Lesson":
                self.current_state = self.lesson
            else:
                self.current_state = self.work

    @decor
    def _create_funny_night(self):
        phrase = "It's the one of those funny nights before a test!"
        while True:
            event = yield
            print(str(self.hour) + ":00\t" + str(phrase))
            if 0 <= event[1] <= 4 or 22 <= event[1] <= 23:
                self.current_state = self.funny_night
            else:
                self.current_state = self.sleep

    @decor
    def _create_deadline_coming(self):
        phrase = "Deadline is coming! Should work very fast!"
        while True:
            event = yield
            print(str(self.hour) + ":00\t" + str(phrase))
            if 20 <= event[1] <= 24:
                self.current_state = self.deadline_coming
            else:
                self.current_state = self.sleep

    @decor
    def _create_lesson(self):
        phrase = "Listening to a lesson"
        while True:
            event = yield
            print(str(self.hour) + ":00\t" + str(phrase))
            if event[0] == "Lesson":
                self.current_state = self.lesson
            elif event[1] in [7,11,20,24]:
                self.current_state = self.eat
            else:
                self.current_state = self.work


def life_simulation(time):
    """Life simulator func"""
    def events_generator():
        """Generates an events and pushes them into the queue"""
        events_queue = []
        for i in range(24*time):
            events_queue.append(event_random_generation(i % 24))
        return events_queue

    def event_random_generation(hour):
        """Generates an event depending on the random value"""
        random_value = random.random()
        if 0.5 < random_value < 0.6 and 22 <= hour <= 23:
            return "Exam tomorrow!"
        elif 0 <= random_value < 0.1 and 20 <= hour <= 24:
            return "BURNING DEADLINE"
        elif 0.3 <= random_value <= 0.5 and 9 <= hour <= 15:
            return "Lesson"
        return None

    life = Life()
    queue = events_generator()
    print(queue)

    for event in queue:
        life.send(event)


def main():
    """Main/starting func"""
    while True:
        try:
            time = int(input("Enter life simulation length (in days): "))
            break
        except TypeError:
            pass
    life_simulation(time)


if __name__ == """__main__""":
    main()
