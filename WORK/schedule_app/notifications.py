# notifications.py
import threading
import time
from plyer import notification
from db import SessionLocal
from datetime import datetime, timedelta
from models import Schedule, Homework

class NotificationManager(threading.Thread):
    def __init__(self, interval=60):
        super().__init__(daemon=True)
        self.interval = interval

    def run(self):
        while True:
            now      = datetime.now()
            upcoming = now + timedelta(minutes=30)

            db = SessionLocal()
            try:
                # Уведомления о занятиях сегодня в ближайшие 30 мин
                lessons = db.query(Schedule).filter(
                    Schedule.start_time.between(now.time(), upcoming.time())
                ).all()
                for l in lessons:
                    notification.notify(
                        title="Скоро занятие",
                        message=f"{l.subject} в {l.start_time.strftime('%H:%M')}",
                        timeout=5
                    )

                # Уведомления по домашним заданиям на сегодня
                hws = db.query(Homework).filter(
                    Homework.due_date == now.date()
                ).all()
                for hw in hws:
                    notification.notify(
                        title="Срок ДЗ",
                        message=f"ДЗ «{hw.title}» должно быть выполнено сегодня",
                        timeout=5
                    )
            finally:
                db.close()
                SessionLocal.remove()

            time.sleep(self.interval)
