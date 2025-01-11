from llama_cpp import Llama
from typing import Dict

class TripSuggestionGenerator:
    def __init__(self, model_path: str = "llama-2-13b-chat.gguf"):
        """
        Initialize the Llama model for generating trip suggestions.
        Args:
            model_path: Path to the Llama model file
        """
        self.llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_batch=512,
            n_threads=4
        )

    def generate_suggestions(self, answers: Dict) -> str:
        """
        Generate trip suggestions based on questionnaire answers.
        Args:
            answers: Dictionary containing questionnaire responses
        Returns:
            str: Formatted trip suggestions
        """
        prompt = f"""Based on a trip to {answers['destination']} in {answers['startDate']} for {answers['duration']}:

1. First, provide a detailed description of the destination during this season, including:
   - Weather conditions and what to expect
   - General pricing levels for the period (peak vs off-peak)
   - Major events or festivals happening
   - Tourist density and booking recommendations

2. Given that the traveler is interested in {', '.join(answers['interests'])}, 
   with a {answers['budget']} budget, suggest specific activities and experiences.
   For each activity, include:
   - Name and description of the activity
   - Estimated duration (in hours or days)
   - Approximate price range in USD
   - Best time of day/week to do it
   - Any special notes (booking requirements, seasonal availability, etc.)

3. Organize the activities by category (e.g., Cultural, Outdoor, Culinary, etc.)
   and indicate which ones best match the user's stated interests.

Please provide specific, practical suggestions that align with the traveler's interests and budget."""

        # Generate response from Llama
        response = self.llm(
            prompt,
            max_tokens=2048,
            temperature=0.7,
            top_p=0.95,
            repeat_penalty=1.2
        )

        return response['choices'][0]['text']