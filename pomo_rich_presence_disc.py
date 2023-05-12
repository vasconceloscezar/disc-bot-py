import time 
from datetime import datetime, timedelta
from plyer import notification
from pypresence import Presence

class PomodoroTimer:
    def __init__(self):
        self.timer = None
        self.start_time = None
        self.end_time = None

    def start_timer(self, timer_type):
        if timer_type == "work":
            self.timer = 25 * 60
        elif timer_type == "short_break":
            self.timer = 5 * 60
        elif timer_type == "long_break":
            self.timer = 15 * 60
        self.initial_timer = self.timer
        self.start_time = datetime.now()

    def check_timer(self):
        if self.timer is not None and self.timer > 0:
            self.timer -= 1
            if self.timer == 0:  # timer ended
                self.end_time = datetime.now()
                notification.notify(
                    title = "Pomodoro Update",
                    message = "Session ended",
                    timeout = 10
                )
                # log the session
                with open("pomodoro_log.txt", "a") as file:
                    file.write(f"Session started at {self.start_time} and ended at {self.end_time}\n")
                self.start_time = None
                self.end_time = None
                return False
            else:
                return True
        else:
            return False
          
    def time_left(self):
      minutes, seconds = divmod(self.timer, 60)
      return f"{minutes:02d}:{seconds:02d}"
    
    def target_time(self):
      if self.start_time is not None:
          end_time = self.start_time + timedelta(seconds=self.initial_timer)
          return end_time.strftime("%H:%M:%S")
      else:
          return "Not set"

    def notify(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_icon=None,
            timeout=10,
        )


client_id = "1106342718248075335"  # replace with your app's client id
RPC = Presence(client_id)
RPC.connect()

def pomodoro_sessions(pomodoro):
    work_sessions = 2
    while True:
        pomodoro.start_timer("work")
        end_timestamp = time.time() + pomodoro.initial_timer
        RPC.update(state="Focusing", start=time.time(), end=end_timestamp, large_image="pomo", large_text="Pomodoro Timer")
        while pomodoro.check_timer():
            print(f"Target time: {pomodoro.target_time()} | Time left: {pomodoro.time_left()}")
            time.sleep(1)
        work_sessions += 1
        if work_sessions % 4 == 0:  # time for a long break
            pomodoro.start_timer("long_break")
            end_timestamp = time.time() + pomodoro.initial_timer
            RPC.update(state="On a Long Break", start=time.time(), end=end_timestamp, large_image="pause", large_text="Pomodoro Timer")
        else:  # time for a short break
            pomodoro.start_timer("short_break")
            end_timestamp = time.time() + pomodoro.initial_timer
            RPC.update(state="On a Short Break", start=time.time(), end=end_timestamp, large_image="pause", large_text="Pomodoro Timer")
        while pomodoro.check_timer():
            print(f"Target time: {pomodoro.target_time()} | Time left: {pomodoro.time_left()}")
            time.sleep(1)


pomodoro = PomodoroTimer()
pomodoro_sessions(pomodoro)
