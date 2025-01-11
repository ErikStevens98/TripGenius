from datetime import datetime, timedelta
import random
from typing import List, Dict, Tuple

class Activity:
    def __init__(self, name: str, duration: float, category: str, 
                 price: Tuple[float, float], preferred_time: str = None):
        self.name = name
        self.duration = duration  # in hours
        self.category = category
        self.price = price  # (min_price, max_price)
        self.preferred_time = preferred_time  # 'morning', 'afternoon', 'evening', or None

class TripScheduler:
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date
        self.activities = []
        self.daily_schedule = {
            'morning': (9, 12),    # 9 AM to 12 PM
            'afternoon': (13, 17), # 1 PM to 5 PM
            'evening': (18, 22)    # 6 PM to 10 PM
        }

    def add_activity(self, activity: Activity):
        """Add an activity to the pool of selected activities."""
        self.activities.append(activity)

    def _can_fit_in_timeblock(self, activity: Activity, timeblock: str) -> bool:
        """Check if an activity can fit in a given timeblock."""
        block_start, block_end = self.daily_schedule[timeblock]
        block_duration = block_end - block_start
        
        # If activity has a preferred time and this isn't it, return False
        if activity.preferred_time and activity.preferred_time != timeblock:
            return False
            
        return activity.duration <= block_duration

    def generate_schedule(self) -> Dict:
        """Generate a daily schedule for the trip duration."""
        trip_duration = (self.end_date - self.start_date).days + 1
        schedule = {}
        available_activities = self.activities.copy()
        
        for day_num in range(trip_duration):
            current_date = self.start_date + timedelta(days=day_num)
            day_schedule = {'morning': None, 'afternoon': None, 'evening': None}
            
            # Try to fit activities into each timeblock
            for timeblock in self.daily_schedule.keys():
                if not available_activities:
                    break
                    
                # Filter activities that can fit in this timeblock
                suitable_activities = [
                    activity for activity in available_activities
                    if self._can_fit_in_timeblock(activity, timeblock)
                ]
                
                if suitable_activities:
                    # Prioritize activities with preferred time matching current timeblock
                    preferred_activities = [
                        activity for activity in suitable_activities
                        if activity.preferred_time == timeblock
                    ]
                    
                    selected_activity = random.choice(
                        preferred_activities if preferred_activities else suitable_activities
                    )
                    
                    day_schedule[timeblock] = selected_activity
                    available_activities.remove(selected_activity)
            
            schedule[current_date.strftime('%Y-%m-%d')] = day_schedule
            
        return schedule

    def calculate_trip_stats(self, schedule: Dict) -> Dict:
        """Calculate statistics for the generated schedule."""
        total_activities = 0
        total_cost_min = 0
        total_cost_max = 0
        activities_by_category = {}
        
        for day_schedule in schedule.values():
            for timeblock, activity in day_schedule.items():
                if activity:
                    total_activities += 1
                    total_cost_min += activity.price[0]
                    total_cost_max += activity.price[1]
                    
                    if activity.category not in activities_by_category:
                        activities_by_category[activity.category] = 0
                    activities_by_category[activity.category] += 1
        
        return {
            'total_activities': total_activities,
            'cost_range': (total_cost_min, total_cost_max),
            'activities_by_category': activities_by_category
        }