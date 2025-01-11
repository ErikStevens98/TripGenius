import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Calendar, MapPin, Clock, Users, Plane } from 'lucide-react';

const TravelQuestionnaire = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState({
    destination: '',
    startDate: '',
    duration: '',
    groupSize: '',
    budget: '',
    tripPurpose: [],
    accommodation: '',
    interests: [],
    transportationPreference: '',
    specialRequirements: ''
  });

  const questions = [
    {
      id: 'destination',
      question: 'Where would you like to go?',
      type: 'text',
      icon: MapPin,
      placeholder: 'Enter city or country'
    },
    {
      id: 'startDate',
      question: 'When are you planning to travel?',
      type: 'month',
      icon: Calendar,
      placeholder: 'Select month and year'
    },
    {
      id: 'duration',
      question: 'How long do you plan to stay?',
      type: 'select',
      icon: Clock,
      options: ['Weekend', '1 week', '2 weeks', '1 month', 'More than 1 month']
    },
    {
      id: 'groupSize',
      question: 'How many people are traveling?',
      type: 'select',
      icon: Users,
      options: ['Solo', 'Couple', 'Family (3-5)', 'Group (6+)']
    },
    {
      id: 'budget',
      question: 'What is your budget range per person?',
      type: 'select',
      options: ['Budget ($0-1000)', 'Moderate ($1000-3000)', 'Luxury ($3000+)']
    },
    {
      id: 'tripPurpose',
      question: 'What is the main purpose of your trip?',
      type: 'multiselect',
      options: ['Relaxation', 'Adventure', 'Cultural', 'Business', 'Food & Dining', 'Nightlife']
    },
    {
      id: 'accommodation',
      question: 'What type of accommodation do you prefer?',
      type: 'select',
      options: ['Hostel', 'Budget Hotel', 'Mid-range Hotel', 'Luxury Resort', 'Vacation Rental']
    },
    {
      id: 'interests',
      question: 'What activities interest you the most?',
      type: 'multiselect',
      options: ['Sightseeing', 'Museums', 'Shopping', 'Outdoor Activities', 'Local Cuisine', 'Beaches']
    },
    {
      id: 'transportationPreference',
      question: 'How do you prefer to get around?',
      type: 'select',
      options: ['Public Transport', 'Rental Car', 'Walking/Biking', 'Guided Tours', 'Mix of Options']
    },
    {
      id: 'specialRequirements',
      question: 'Any special requirements or preferences?',
      type: 'text',
      placeholder: 'E.g., accessibility needs, dietary restrictions, etc.'
    }
  ];

  const handleAnswer = (questionId, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: value
    }));
    if (currentStep < questions.length - 1) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handleSubmit = () => {
    console.log('Final answers:', answers);
  };

  const renderInput = (question) => {
    switch (question.type) {
      case 'text':
        return (
          <input
            type="text"
            className="w-full p-2 border rounded-lg"
            placeholder={question.placeholder}
            value={answers[question.id]}
            onChange={(e) => handleAnswer(question.id, e.target.value)}
          />
        );
      case 'month':
        return (
          <input
            type="month"
            className="w-full p-2 border rounded-lg"
            value={answers[question.id]}
            onChange={(e) => handleAnswer(question.id, e.target.value)}
          />
        );
      case 'select':
        return (
          <select
            className="w-full p-2 border rounded-lg"
            value={answers[question.id]}
            onChange={(e) => handleAnswer(question.id, e.target.value)}
          >
            <option value="">Select an option</option>
            {question.options.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        );
      case 'multiselect':
        return (
          <div className="space-y-2">
            {question.options.map((option) => (
              <label key={option} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={answers[question.id].includes(option)}
                  onChange={(e) => {
                    const newValue = e.target.checked
                      ? [...answers[question.id], option]
                      : answers[question.id].filter(item => item !== option);
                    handleAnswer(question.id, newValue);
                  }}
                  className="form-checkbox"
                />
                <span>{option}</span>
              </label>
            ))}
          </div>
        );
      default:
        return null;
    }
  };

  const CurrentIcon = questions[currentStep].icon;

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Plane className="w-6 h-6 text-blue-500" />
          <span>Travel Planning Questionnaire</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="text-sm text-gray-500">
            Question {currentStep + 1} of {questions.length}
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <CurrentIcon className="w-5 h-5 text-blue-500" />
              <h2 className="text-xl font-semibold">
                {questions[currentStep].question}
              </h2>
            </div>
            {renderInput(questions[currentStep])}
          </div>

          <div className="flex justify-between mt-6">
            <button
              onClick={() => setCurrentStep(prev => Math.max(0, prev - 1))}
              disabled={currentStep === 0}
              className="px-4 py-2 text-sm bg-gray-100 rounded-lg disabled:opacity-50"
            >
              Previous
            </button>
            
            {currentStep === questions.length - 1 ? (
              <button
                onClick={handleSubmit}
                className="px-4 py-2 text-sm text-white bg-blue-500 rounded-lg hover:bg-blue-600"
              >
                Submit
              </button>
            ) : (
              <button
                onClick={() => setCurrentStep(prev => Math.min(questions.length - 1, prev + 1))}
                className="px-4 py-2 text-sm text-white bg-blue-500 rounded-lg hover:bg-blue-600"
              >
                Next
              </button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default TravelQuestionnaire;