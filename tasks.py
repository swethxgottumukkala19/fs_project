# tasks.py - 150 Daily Tasks List
# Starting from October 04, 2025

DAILY_TASKS = [
   # Week 1: Health & Fitness
"Drink 8 glasses of water today",
"Do 30 push-ups",
"Walk or jog for 3 km",
"Stretch for 15 minutes",
"No junk food or sugary drinks today",
"Sleep 8 hours without phone distractions",
"Try a 5-minute cold shower",

# Week 2: Productivity
"Read 30 pages of a book",
"Learn 10 new words and use them in sentences",
"Clean and organize your workspace completely",
"Plan tomorrow with time blocks",
"Finish one thing you’ve been procrastinating",
"Write a one-page journal entry before bed",
"Spend 1 hour learning a useful online skill",

# Week 3: Mental Health
"Meditate for 15 minutes without background music",
"Write 5 things you’re grateful for",
"Call or meet an old friend and have a real talk",
"Sit in silence for 10 minutes outdoors",
"Take a complete digital detox for 3 hours",
"Do something creative (draw, write, or play music)",
"Do one unexpected act of kindness",

# Week 4: Learning & Growth
"Watch a TED talk and summarize it",
"Practice a new language for 20 minutes",
"Try solving 5 logical puzzles or riddles",
"Write a short motivational post or poem",
"Learn and cook a completely new recipe",
"Take an online quiz in a random topic",
"Research a life skill (taxes, investing, etc.)",

# Week 5: Social & Relationships
"Send a supportive message to 3 friends",
"Compliment 2 people genuinely today",
"Share a helpful tip or idea online",
"Make someone laugh today",
"Write a thank-you note to someone important",
"Ask someone how they’re really doing and listen",
"Plan a mini hangout with friends or family",

# Week 6: Financial & Career
"Track your expenses for the last 7 days",
"Save ₹100–₹200 by skipping one unnecessary spend",
"Update your resume or LinkedIn profile",
"Watch a video on personal branding or freelancing",
"Reach out to a professional connection",
"Set a realistic financial goal for the month",
"Read one article about investing or savings",

# Week 7: Home & Environment
"Clean your entire room like a reset day",
"Organize one messy shelf or drawer perfectly",
"Do laundry and fold it neatly",
"Water your plants or clean your study area",
"Donate or recycle 3 unused items",
"Fix or repurpose something broken",
"Make your bed as soon as you wake up",

# Week 8: Fitness Challenges
"Do 50 squats",
"Hold a plank for 2 minutes total",
"Climb 20 flights of stairs",
"Do 40 sit-ups",
"Try a completely new workout or sport",
"Dance like crazy for 20 minutes",
"Do a 20-minute yoga or mobility session",

# Week 9: Creative Tasks
"Draw or doodle something abstract",
"Take 5 aesthetic or creative photos",
"Write a letter to your future self (open in a year)",
"Make a custom playlist that boosts your mood",
"Design something on Canva or paper",
"Try making a short video or reel",
"Paint, sketch, or color for 30 minutes",

# Week 10: Self-Care
"Take a long relaxing shower or bath",
"Do a skincare routine and feel refreshed",
"Style yourself in an outfit you love",
"Say 5 positive affirmations in front of the mirror",
"Treat yourself to your favorite snack guilt-free",
"Unplug for an hour and just rest",
"Spend 30 minutes in nature or sunshine",

# Week 11: Technology & Skills
"Learn a new keyboard shortcut or productivity hack",
"Clear 500MB+ of phone storage",
"Unsubscribe from junk emails",
"Build a simple project or code snippet",
"Backup your files or photos",
"Update and organize your apps properly",
"Clean your laptop or phone physically",

# Week 12: Food & Nutrition
"Cook a healthy high-protein meal",
"Try a fruit or food you’ve never eaten before",
"Meal prep for tomorrow",
"Avoid sugar and fried food for the entire day",
"Eat breakfast within 1 hour of waking up",
"Make a smoothie or detox drink yourself",
"Drink green tea or lemon water twice today",

# Week 13: Adventure & Fun
"Explore a new spot in your city",
"Try something totally outside your comfort zone",
"Play a competitive game or challenge with friends",
"Watch a mind-blowing documentary",
"Start a small creative side project",
"Teach a fun skill to a friend",
"Go stargazing or take night photos",

# Week 14: Mindfulness
"Do 10 minutes of deep breathing",
"Write how you feel without filters",
"Do a guided body scan meditation",
"Eat a full meal mindfully without screens",
"Observe your surroundings silently for 10 minutes",
"Do one random act of kindness secretly",
"Reflect on your wins and struggles today",

# Week 15: Knowledge
"Read 2 articles on a random topic",
"Learn one fascinating historical fact",
"Understand one concept deeply (YouTube/Google it)",
"Watch a TED Talk or explainer video",
"Take digital notes of what you learn",
"Quiz yourself on a topic you studied this week",
"Explain something complex to someone else",

# Week 16: Physical Challenges
"Do 60 burpees",
"Run or jog for 2 km non-stop",
"Complete 150 jumping jacks",
"Try a HIIT workout for 15 minutes",
"Do a full-body circuit training",
"Balance on one leg for 1 minute per side",
"Work on your flexibility for 20 minutes",

# Week 17: Social Media Detox
"Limit screen time to 1.5 hours",
"Don’t check your phone for 1 hour after waking",
"Post something inspiring or positive",
"Unfollow 10 negative/unhelpful accounts",
"Turn off all notifications for a day",
"Use your phone only for learning or music",
"Delete or hide distracting apps for 24 hours",

# Week 18: Personal Development
"Write down 3 realistic goals for next month",
"Reflect on your progress and note 2 lessons",
"Create a small vision board (digital or paper)",
"Listen to a motivational podcast or audiobook",
"Write your 1-year roadmap with mini goals",
"Identify 1 weakness and make an improvement plan",
"Celebrate one small achievement meaningfully",

# Week 19: Relationships
"Apologize sincerely to someone you’ve hurt",
"Forgive someone mentally and move on",
"Plan a hangout or video call with friends",
"Write and send a thank-you text or note",
"Share your honest feelings with a close friend",
"Be 100% present in a conversation today",
"Make a new friend through an activity or group",

# Week 20: Adventure Continues
"Try a new food or cafe experience",
"Explore a park, beach, or trail near you",
"Attend a free local event or workshop",
"Take a new walking route or bus route",
"Try street food or a local favorite",
"Visit a museum, gallery, or exhibition",
"Spend 15 minutes stargazing or cloud watching",

# Week 21: Final Push
"Reflect on your 147-day journey so far",
"Write a summary of what you’ve learned",
"Share your experience with a friend or online",
"Plan your next 150-day challenge goals",
"Do something symbolic to celebrate your streak",
"Thank yourself for every small step you took",
"Set one new bold challenge for your future self",

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
