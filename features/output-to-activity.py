from typing import List, Dict, Optional
import re
from datetime import datetime
from Scheduling import Activity

class ActivityConverter:
    @staticmethod
    def parse_price_range(price_str: str) -> tuple[float, float]:
        """Extract price range from string format like '$30-40' or '$30 - $40'."""
        numbers = re.findall(r'\d+', price_str)
        if len(numbers) >= 2:
            return (float(numbers[0]), float(numbers[1]))
        elif len(numbers) == 1:
            # If only one number is found, use it as both min and max
            return (float(numbers[0]), float(numbers[0]))
        else:
            raise ValueError(f"Could not parse price range from: {price_str}")

    @staticmethod
    def parse_duration(duration_str: str) -> float:
        """Convert duration string to hours (float)."""
        if 'day' in duration_str.lower():
            # Full day activities are considered 8 hours
            return 8.0
        
        # Extract numbers and determine if it's a range
        numbers = re.findall(r'\d+(?:\.\d+)?', duration_str)
        if len(numbers) >= 2:
            # If it's a range (e.g., "2-3 hours"), take the average
            return (float(numbers[0]) + float(numbers[1])) / 2
        elif len(numbers) == 1:
            return float(numbers[0])
        else:
            raise ValueError(f"Could not parse duration from: {duration_str}")

    @staticmethod
    def determine_preferred_time(time_str: str) -> Optional[str]:
        """Determine preferred time from description."""
        time_str = time_str.lower()
        
        # Define time-related keywords
        morning_keywords = ['morning', 'sunrise', 'early', 'breakfast']
        afternoon_keywords = ['afternoon', 'lunch', 'noon', 'midday']
        evening_keywords = ['evening', 'sunset', 'night', 'dinner']
        
        # Check for time keywords
        for keyword in morning_keywords:
            if keyword in time_str:
                return 'morning'
        for keyword in afternoon_keywords:
            if keyword in time_str:
                return 'afternoon'
        for keyword in evening_keywords:
            if keyword in time_str:
                return 'evening'
        
        return None

    @staticmethod
    def convert_llm_activity(activity_dict: Dict) -> Activity:
        """
        Convert a single activity from LLM format to Activity object.
        
        Expected activity_dict format:
        {
            'name': 'Activity Name',
            'description': 'Description...',
            'duration': '2-3 hours',
            'price_range': '$30-40',
            'category': 'Category',
            'best_time': 'Morning recommended'
        }
        """
        try:
            name = activity_dict['name']
            duration = ActivityConverter.parse_duration(activity_dict['duration'])
            price_range = ActivityConverter.parse_price_range(activity_dict['price_range'])
            category = activity_dict['category']
            preferred_time = ActivityConverter.determine_preferred_time(activity_dict['best_time'])
            
            return Activity(
                name=name,
                duration=duration,
                category=category,
                price=price_range,
                preferred_time=preferred_time
            )
        except KeyError as e:
            raise ValueError(f"Missing required field in activity data: {e}")

    @staticmethod
    def parse_llm_response(llm_text: str) -> List[Dict]:
        """
        Parse the LLM response text into a list of activity dictionaries.
        This is a simple implementation - you might need to adjust based on your exact LLM output format.
        """
        activities = []
        current_activity = {}
        
        # Split text into lines and process
        lines = llm_text.split('\n')
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Check for new activity (assumes activities start with a name)
            if line and not line.startswith('-') and ':' not in line:
                if current_activity:
                    activities.append(current_activity)
                current_activity = {'name': line}
                continue
                
            # Parse activity details
            if line.startswith('-'):
                line = line.lstrip('- ')
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    # Map keys to our expected format
                    key_mapping = {
                        'duration': 'duration',
                        'price': 'price_range',
                        'category': 'category',
                        'best time': 'best_time',
                        'time': 'best_time'
                    }
                    
                    mapped_key = key_mapping.get(key)
                    if mapped_key:
                        current_activity[mapped_key] = value
        
        # Don't forget the last activity
        if current_activity:
            activities.append(current_activity)
            
        return activities