from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class Alert:
    def __init__(self, title: str, description: str, date: datetime, 
                 alert_type: str, priority: str = "normal"):
        self.title = title
        self.description = description
        self.date = date
        self.alert_type = alert_type  # 'trip_start', 'booking_deadline', 'activity', 'preparation'
        self.priority = priority      # 'high', 'normal', 'low'
        self.acknowledged = False

    def to_dict(self) -> Dict:
        """Convert alert to dictionary for storage."""
        return {
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat(),
            'alert_type': self.alert_type,
            'priority': self.priority,
            'acknowledged': self.acknowledged
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Alert':
        """Create alert from dictionary."""
        alert = cls(
            title=data['title'],
            description=data['description'],
            date=datetime.fromisoformat(data['date']),
            alert_type=data['alert_type'],
            priority=data['priority']
        )
        alert.acknowledged = data['acknowledged']
        return alert

class TripAlertManager:
    def __init__(self, trip_start: datetime, trip_end: datetime):
        self.trip_start = trip_start
        self.trip_end = trip_end
        self.alerts: List[Alert] = []

    def generate_trip_alerts(self, schedule: Dict, booking_info: Dict):
        """Generate all necessary alerts for the trip."""
        # Trip preparation alerts
        self._add_preparation_alerts()
        
        # Booking deadline alerts
        self._add_booking_deadline_alerts(booking_info)
        
        # Activity alerts
        self._add_activity_alerts(schedule)

    def _add_preparation_alerts(self):
        """Add standard trip preparation alerts."""
        # 1 month before
        self.add_alert(
            "Start Trip Planning",
            "Time to start planning your trip! Check passport validity and travel requirements.",
            self.trip_start - timedelta(days=30),
            "preparation",
            "high"
        )

        # 2 weeks before
        self.add_alert(
            "Trip Preparation",
            "Check weather forecast and start packing list.",
            self.trip_start - timedelta(days=14),
            "preparation",
            "normal"
        )

        # 3 days before
        self.add_alert(
            "Final Preparation",
            "Confirm all reservations and prepare travel documents.",
            self.trip_start - timedelta(days=3),
            "preparation",
            "high"
        )

    def _add_booking_deadline_alerts(self, booking_info: Dict):
        """Add alerts for booking deadlines."""
        for activity_name, info in booking_info.items():
            # Assuming we want to book activities at least 2 weeks in advance
            first_occurrence = datetime.fromisoformat(info['occurrences'][0]['date'])
            booking_deadline = first_occurrence - timedelta(days=14)
            
            if booking_deadline > datetime.now():
                self.add_alert(
                    f"Book {activity_name}",
                    f"Time to book {activity_name}! Price range: {info['price_range']}\n"
                    f"Booking link: {info['booking_url']}",
                    booking_deadline,
                    "booking_deadline",
                    "high"
                )

    def _add_activity_alerts(self, schedule: Dict):
        """Add alerts for scheduled activities."""
        for date_str, day_schedule in schedule.items():
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            for timeblock, activity in day_schedule.items():
                if activity:
                    # Get the start time for the timeblock
                    if timeblock == 'morning':
                        alert_time = date.replace(hour=8)  # Alert 1 hour before
                    elif timeblock == 'afternoon':
                        alert_time = date.replace(hour=12)
                    else:  # evening
                        alert_time = date.replace(hour=17)

                    self.add_alert(
                        f"Upcoming: {activity.name}",
                        f"Reminder: {activity.name} ({activity.duration} hours)\n"
                        f"Category: {activity.category}\n"
                        f"Price range: ${activity.price[0]}-${activity.price[1]}",
                        alert_time,
                        "activity",
                        "normal"
                    )

    def add_alert(self, title: str, description: str, date: datetime, 
                 alert_type: str, priority: str = "normal"):
        """Add a new alert."""
        alert = Alert(title, description, date, alert_type, priority)
        self.alerts.append(alert)
        self._sort_alerts()

    def _sort_alerts(self):
        """Sort alerts by date."""
        self.alerts.sort(key=lambda x: x.date)

    def get_upcoming_alerts(self, days: int = 7) -> List[Alert]:
        """Get alerts for the next X days."""
        current_date = datetime.now()
        end_date = current_date + timedelta(days=days)
        
        return [
            alert for alert in self.alerts
            if current_date <= alert.date <= end_date
            and not alert.acknowledged
        ]

    def acknowledge_alert(self, alert: Alert):
        """Mark an alert as acknowledged."""
        alert.acknowledged = True

    def save_alerts(self, filename: str):
        """Save alerts to a file."""
        with open(filename, 'w') as f:
            json.dump(
                {
                    'trip_start': self.trip_start.isoformat(),
                    'trip_end': self.trip_end.isoformat(),
                    'alerts': [alert.to_dict() for alert in self.alerts]
                },
                f,
                indent=2
            )

    @classmethod
    def load_alerts(cls, filename: str) -> 'TripAlertManager':
        """Load alerts from a file."""
        with open(filename, 'r') as f:
            data = json.load(f)
            
        manager = cls(
            trip_start=datetime.fromisoformat(data['trip_start']),
            trip_end=datetime.fromisoformat(data['trip_end'])
        )
        
        manager.alerts = [Alert.from_dict(alert_data) for alert_data in data['alerts']]
        return manager