# tasks.py - 150 Daily Tasks List
# Starting from October 04, 2025

DAILY_TASKS = [
    # Week 1: Health & Fitness
    "Drink 8 glasses of water today",
    "Do 20 push-ups",
    "Walk for 30 minutes",
    "Stretch for 10 minutes",
    "No junk food today",
    "Sleep 8 hours tonight",
    "Do 50 jumping jacks",
    
    # Week 2: Productivity
    "Read 20 pages of a book",
    "Learn 5 new words",
    "Organize your workspace",
    "Plan tomorrow's schedule",
    "Complete a pending task",
    "Write in a journal",
    "Practice a skill for 30 minutes",
    
    # Week 3: Mental Health
    "Meditate for 10 minutes",
    "Practice gratitude - write 3 things",
    "Call a friend or family member",
    "Listen to calming music",
    "Take a digital detox for 2 hours",
    "Do something creative",
    "Help someone today",
    
    # Week 4: Learning & Growth
    "Watch an educational video",
    "Practice a new language for 15 minutes",
    "Solve 3 math problems",
    "Write a short story or poem",
    "Learn a new recipe",
    "Take an online quiz on any topic",
    "Research something you're curious about",
    
    # Week 5: Social & Relationships
    "Send a motivational message to 3 friends",
    "Compliment someone genuinely",
    "Share something helpful on social media",
    "Make someone smile today",
    "Express appreciation to someone",
    "Listen actively without interrupting",
    "Spend quality time with family",
    
    # Week 6: Financial & Career
    "Review your expenses",
    "Save money - skip one unnecessary purchase",
    "Update your resume or portfolio",
    "Learn about a career skill",
    "Network with someone new",
    "Set a financial goal",
    "Read about personal finance",
    
    # Week 7: Home & Environment
    "Clean your room thoroughly",
    "Organize one drawer or shelf",
    "Do laundry and fold clothes",
    "Water plants or care for pets",
    "Recycle or donate unused items",
    "Fix something broken",
    "Make your bed neatly",
    
    # Week 8: Fitness Challenges
    "Do 30 squats",
    "Hold a plank for 1 minute",
    "Climb stairs for 10 minutes",
    "Do 25 sit-ups",
    "Try a new exercise",
    "Dance for 15 minutes",
    "Do yoga for 20 minutes",
    
    # Week 9: Creative Tasks
    "Draw or sketch something",
    "Take 10 creative photos",
    "Write a letter to your future self",
    "Create a playlist of favorite songs",
    "Design something on paper",
    "Try origami or paper crafts",
    "Paint or color for 30 minutes",
    
    # Week 10: Self-Care
    "Take a relaxing bath",
    "Do a face mask or skincare routine",
    "Get a haircut or groom yourself",
    "Wear your favorite outfit",
    "Practice positive affirmations",
    "Treat yourself to something small",
    "Take a nature walk",
    
    # Week 11: Technology & Skills
    "Learn a keyboard shortcut",
    "Clean up your phone storage",
    "Unsubscribe from 5 emails",
    "Learn basic coding concept",
    "Backup important files",
    "Update all your apps",
    "Organize your desktop files",
    
    # Week 12: Food & Nutrition
    "Cook a healthy meal",
    "Try a new fruit or vegetable",
    "Pack lunch instead of buying",
    "Avoid sugar for the day",
    "Eat breakfast within 1 hour of waking",
    "Try meal prepping",
    "Drink green tea",
    
    # Week 13: Adventure & Fun
    "Visit a new place in your city",
    "Try something you've never done",
    "Play a board game or puzzle",
    "Watch a documentary",
    "Start a new hobby",
    "Teach someone something",
    "Have a picnic outdoors",
    
    # Week 14: Mindfulness
    "Practice deep breathing for 5 minutes",
    "Write down your feelings",
    "Do a body scan meditation",
    "Practice mindful eating",
    "Observe nature for 10 minutes",
    "Do a random act of kindness",
    "Reflect on your day",
    
    # Week 15: Knowledge
    "Read a news article",
    "Learn a historical fact",
    "Study a new concept",
    "Watch a TED talk",
    "Take notes from something you learned",
    "Quiz yourself on a topic",
    "Teach someone what you learned",
    
    # Week 16: Physical Challenges
    "Do 40 burpees",
    "Run or jog for 15 minutes",
    "Do 100 jumping jacks",
    "Try a new sport or game",
    "Do a full body workout",
    "Practice balance exercises",
    "Do flexibility training",
    
    # Week 17: Social Media Detox
    "Limit screen time to 2 hours",
    "Don't check phone for 1 hour after waking",
    "Post something positive",
    "Unfollow negative accounts",
    "Turn off notifications for the day",
    "Use phone only for productive tasks",
    "Delete unused apps",
    
    # Week 18: Personal Development
    "Set 3 goals for next month",
    "Review your progress",
    "Create a vision board",
    "Listen to a motivational podcast",
    "Write your 5-year plan",
    "Identify and work on a weakness",
    "Celebrate a small win",
    
    # Week 19: Relationships
    "Apologize if you've wronged someone",
    "Forgive someone",
    "Plan a hangout with friends",
    "Write a thank you note",
    "Share your feelings honestly",
    "Be fully present in conversations",
    "Make a new friend",
    
    # Week 20: Adventure Continues
    "Try a new cafe or restaurant",
    "Explore a park or trail",
    "Attend a local event",
    "Take a different route home",
    "Try street food",
    "Visit a museum or gallery",
    "Stargaze for 15 minutes",
    
    # Week 21: Final Push
    "Reflect on your 147-day journey",
    "Write what you've learned",
    "Share your experience with someone",
    "Plan your next 150 days",
    "Celebrate your consistency",
    "Thank yourself for showing up",
    "Set new challenging goals"
]

def get_task_for_day(start_date, current_date):
    """
    Get the task for a specific day based on the start date.
    start_date and current_date should be date objects.
    """
    from datetime import timedelta
    
    delta = current_date - start_date
    day_index = delta.days
    
    if day_index < 0:
        return None
    elif day_index >= len(DAILY_TASKS):
        # Cycle through tasks if beyond 150 days
        day_index = day_index % len(DAILY_TASKS)
    
    return DAILY_TASKS[day_index]
