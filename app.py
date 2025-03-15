# Application 
from datetime import datetime, timedelta

class SmartMeetingScheduler:
    def _init_(self):
        self.working_hours = (9, 17)
        self.holidays = {"2025-01-01", "2025-12-25", "2025-01-24"}
        self.schedules = {}

    def is_working_day(self, date):
        return date.weekday() < 5 and date.strftime("%Y-%m-%d") not in self.holidays

    def schedule_meeting(self, user, date_str, start_time, end_time):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if not self.is_working_day(date):
            return "Cannot schedule on weekends or holidays."

        start_dt = datetime.strptime(start_time, "%H:%M").time()
        end_dt = datetime.strptime(end_time, "%H:%M").time()

        if not (self.working_hours[0] <= start_dt.hour < self.working_hours[1] and
                self.working_hours[0] < end_dt.hour <= self.working_hours[1] and
                start_dt < end_dt):
            return "Invalid time slot. Must be within working hours."

        self.schedules.setdefault(user, {}).setdefault(date_str, [])
        for existing_start, existing_end in self.schedules[user][date_str]:
            if not (end_dt <= existing_start or start_dt >= existing_end):
                return "Time slot overlaps with an existing meeting."

        self.schedules[user][date_str].append((start_dt, end_dt))
        self.schedules[user][date_str].sort()
        return "Meeting scheduled successfully."

    def check_available_slots(self, user, date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if not self.is_working_day(date):
            return "No available slots on weekends or holidays."

        booked = sorted(self.schedules.get(user, {}).get(date_str, []))
        available_slots = []
        start = datetime.strptime(f"{self.working_hours[0]}:00", "%H:%M").time()

        for existing_start, _ in booked:
            if start < existing_start:
                available_slots.append((start, existing_start))
            start = booked.pop(0)[1] if booked else existing_start

        if start < datetime.strptime(f"{self.working_hours[1]}:00", "%H:%M").time():
            available_slots.append((start, datetime.strptime(f"{self.working_hours[1]}:00", "%H:%M").time()))

        return [f"{s.strftime('%I:%M %p')} – {e.strftime('%I:%M %p')}" for s, e in available_slots] or ["No available slots"]

    def view_meetings(self, user, date_str):
        meetings = self.schedules.get(user, {}).get(date_str, [])
        if not meetings:
            return "No meetings scheduled."

        return [f"{s.strftime('%I:%M %p')} – {e.strftime('%I:%M %p')}" for s, e in meetings]

    def cancel_meeting(self, user, date_str, start_time, end_time):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if user not in self.schedules or date_str not in self.schedules[user]:
            return "No meetings found."

        start_dt = datetime.strptime(start_time, "%H:%M").time()
        end_dt = datetime.strptime(end_time, "%H:%M").time()
        meeting = (start_dt, end_dt)

        if meeting in self.schedules[user][date_str]:
            self.schedules[user][date_str].remove(meeting)
            if not self.schedules[user][date_str]:
                del self.schedules[user][date_str]
            return "Meeting cancelled successfully."
        return "Meeting not found."


scheduler = SmartMeetingScheduler()
print(scheduler.schedule_meeting("Lybra", "2025-03-18", "10:00", "11:00"))
print(scheduler.check_available_slots("Lybra", "2025-04-15"))
print(scheduler.view_meetings("Lybra", "2025-03-17"))
print(scheduler.cancel_meeting("Lybra", "2025-03-18", "10:00", "11:00"))
print(scheduler.view_meetings("Lybra", "2025-03-18"))



