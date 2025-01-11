from typing import Dict, Optional
from llama_cpp import Llama
from datetime import datetime

class ReservationManager:
    def __init__(self, model_path: str = "llama-2-13b-chat.gguf"):
        """Initialize the Reservation Manager with Llama model."""
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_batch=512,
            n_threads=4
        )
        
    def _get_booking_url(self, activity_name: str, destination: str) -> str:
        """
        Get booking URL suggestion from Llama for a specific activity.
        """
        prompt = f"""Give the URL of the webpage where I could most certainly buy tickets or make a reservation for this activity: '{activity_name}' in {destination}. 
        
Consider official websites, major booking platforms (like Viator, GetYourGuide, etc.), or local tour operators.
Only return a single, most reliable URL. If you're not completely sure about the specific URL, suggest the main booking platform's search page for this destination."""

        response = self.llm(
            prompt,
            max_tokens=100,
            temperature=0.3,  # Lower temperature for more focused responses
            top_p=0.95,
            repeat_penalty=1.1
        )
        
        # Extract URL from response
        response_text = response['choices'][0]['text'].strip()
        # Basic URL extraction - you might want to add more sophisticated URL validation
        if 'http' in response_text:
            url = response_text.split('\n')[0].strip()
            return url
        return response_text

    def get_booking_information(self, schedule: Dict, destination: str) -> Dict:
        """
        Generate booking information for all activities in the schedule.
        
        Args:
            schedule: The schedule dictionary from TripScheduler
            destination: The trip destination
            
        Returns:
            Dictionary with booking information for each activity
        """
        booking_info = {}
        processed_activities = set()  # To avoid duplicate lookups
        
        # Process each day in the schedule
        for date, day_schedule in schedule.items():
            for timeblock, activity in day_schedule.items():
                if activity and activity.name not in processed_activities:
                    booking_url = self._get_booking_url(activity.name, destination)
                    
                    booking_info[activity.name] = {
                        'booking_url': booking_url,
                        'price_range': f"${activity.price[0]}-${activity.price[1]}",
                        'duration': f"{activity.duration} hours",
                        'category': activity.category,
                        'preferred_time': activity.preferred_time or 'Flexible',
                        'occurrences': []  # Will store all date/time occurrences
                    }
                    processed_activities.add(activity.name)
                
                # Add occurrence information
                if activity:
                    booking_info[activity.name]['occurrences'].append({
                        'date': date,
                        'timeblock': timeblock
                    })
        
        return booking_info

    def print_booking_summary(self, booking_info: Dict):
        """Print a user-friendly summary of booking information."""
        print("\n=== Booking Information for Your Activities ===\n")
        
        for activity_name, info in booking_info.items():
            print(f"\n📍 {activity_name}")
            print(f"   Price Range: {info['price_range']}")
            print(f"   Duration: {info['duration']}")
            print(f"   Category: {info['category']}")
            
            print("\n   Scheduled Times:")
            for occurrence in info['occurrences']:
                print(f"   - {occurrence['date']} ({occurrence['timeblock']})")
            
            print(f"\n   🔗 Booking Link:")
            print(f"   {info['booking_url']}")
            print("\n   ---")