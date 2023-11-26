from string import Template


def getPromptChoser():
    return Template( """
Given a description of a person's working routine, your task is to ascertain whether the actions described occurred today, yesterday, future or on a different day. 

Instructions:
0. This rules over all of the below: If the actions takes place in the future (a moment ahead of the current moment), return "Future".
1. Examine the text for explicit or implicit references to timeframes or dates.
2. If the actions clearly took place earlier today, return "Today". Unless the moment is ahead of $current_date, in which case, return "Future".
3. If the actions occurred the day before the current day, return "Yesterday".
4. If the actions happened on a day that is not today, yesterday, or in the future, return "Another day".
5. If there is no explicit or implicit reference to timeframes or dates, return "Unknown".

Note: Today's date is $current_date (yyyy/mm/dd hh:mm). Use this as a reference to determine the timeframe of the actions described.

Please analyze the following text and determine the timing of the actions:
$text
    """)

def getSummarizerCurrentDay():
    return Template( """
Given a description of a person's working routine for today, your task is to identify and summarize the actions performed and their corresponding time frames from earlier in the day.

Instructions:
1. Identify each action along with its specific time period from earlier today. Time periods should be exact (e.g., 9am to 11am, 1:30pm to 3:45pm).  Make sure to use the time period explicitly or implicitly mentioned in the description.
2. Group actions that occur within the same time span.
3. Output the date in the format: day, month and year (%d/%m/%Y %H:%M). For actions that occurred today, the date is $current_date (yyyy/mm/dd hh:mm). Include only the time for today's actions.
4. Ensure clarity and conciseness in summarizing the actions.

Now, extract and summarize the information from the following description of today's activities:
$text
""")

def getSummarizerDayBefore():
    return Template( """
Given a description of a person's working routine for yesterday, your task is to identify and summarize the actions performed and their corresponding time frames from that day.

Instructions:
1. Identify each action along with its specific time period from yesterday. Time periods should be exact (e.g., 9am to 11am, 1:30pm to 3:45pm). Make sure to use the time period explicitly or implicitly mentioned in the description.
2. Group actions that occur within the same time span.
3. Output the date in the format: day, month and year (%d/%m/%Y %H:%M). Today's date is $current_date (yyyy/mm/dd hh:mm). Calculate yesterday's date by subtracting one day from today's date and use it for the actions that occurred yesterday.
4. Ensure clarity and conciseness in summarizing the actions.

Now, extract and summarize the information from the following description of yesterday's activities:
$text
""")
def getSummarizerOtherDays():
    return Template("""
Given a narrative of a person's working routine within the current week, your task is to identify and summarize the actions performed and their corresponding time frames.

Instructions:
1. Identify each action along with its specific time period. The time periods should be exact (e.g., 9am to 11am, 1:30pm to 3:45pm). Make sure to use the time period explicitly or implicitly mentioned in the description.
2. If the text mentions a day of the week (e.g., Monday, Tuesday), determine the date by matching it with the corresponding date of the current week.
3. If the text mentions a date (e.g., 21st, 22nd), ensure this date falls within the range of the current week's dates.
4. Group actions that occur within the same time span.
5. Output the date in the format: day, month and year (%d/%m/%Y %H:%M). Today's date is $current_date (yyyy/mm/dd hh:mm). Use this as a reference to calculate the dates for the current week.
6. Ensure clarity and conciseness in summarizing the actions.

Based on the description, determine the specific day (or date) of the current week to which the actions are associated, and summarize the activities accordingly.

Now, extract and summarize the information from the following description of the work activities:
$text
""")

# def getNoAvailablePrompt():
#     return """
#     Create a sentence telling the user of an application that the message the person sent was not valid for the application. Tell them to try again.
#     """

def getBaseKnowledgePrompt():
    return Template("""
    For the following demand have the following as baseline knowledge:
    1.Each description presents the activity a person has done in the day.
    2. A person has a group of activities they perform. Each description has direct relation with one of the activities within this group. Usually, the names are the clients for which this person works. Try to match the activities and the correct clients, if the information is available.
    3. The list of activities may contain one or more names.
    4. If the text does not contain a clear instruction about which activity from the group the task belong to, then, use always the first option.
    
    Among the options, there might be a "BetaSeeker". "BetaSeeker" is an initiative in which people help hiring new employees. If there are references to interviews or candidate's form, associate that with "BetaSeeker".
    
    5. For the following description, this is the list of activities for the person: $activities
    
    6. Each person has a default starting time to start their activities. The default starting time has to be used only if there is no reference to a specific starting time for an activity in the description. The default starting time for the following description is: $defaultStartingTime. Starting and ending time are mandatory to each activity.
    7. Each person has a default ending time to end their activities.The default ending time has to be used only if there is no reference to a specific ending time for an activity in the description. The default ending time for the following description is: $defaultEndingTime. Starting and ending time are mandatory to each activity.
    Unless explicitly informed the opposite, people's activities will always be performed between $defaultStartingTime and $defaultEndingTime.
    
    8. People are obliged to have a break between activities. If no reference to a break, lunch break, or coffee break has been made in the description, understand that there is a break between $breakDefaultStartTime and $breakDefaultEndTime. 
    The only case you will not consider a break to exist is if the person explicitly states that they do not have a break in the day.

    """)

# def getThingsNotToInclude():
#     return """
#     MUST NOT INCLUDE IN THE OUTPUT:
#     - Lunch breaks;
#     - Coffee breaks;
#     - Leaves.
#     If these informations are in the description, then, do not include them in the output.
#     """
def sampleFormat():
    return """
    
    Please generate the response as a JSON object with an array of activities. Each activity should have the keys: 'activity', 'date', 'startingTime', 'endingTime', and 'description'. Fill in the 'activity' with the name of the activity which has to be one of the activities in the list, the 'date' with the specific date in the format DD/MM/YYYY (do not include the hours in the date field), and the 'description' with the description of the activity. Fill in the 'startingTime' and 'endingTime' with the specific time in the format HH:MM.
    The output must contain only the JSON, starting with '{' and ending with '}'.
   Sample JSON:
    {
  "activities": [
    {
      "activity": "<Fill with specific activity name>",
      "date": "<Fill with specific date in DD/MM/YYYY (day, month and year)>",
      "startingTime": "<Fill with starting time in HH:MM format>",
      "endingTime": "<Fill with ending time in HH:MM format>",
      "description": "<Fill with detailed description of the activity>"
    },
    {
      "activity": "<Fill with specific activity name>",
      "date": "<Fill with specific date in DD/MM/YYYY (day, month and year)>",
      "startingTime": "<Fill with starting time in HH:MM format>",
      "endingTime": "<Fill with ending time in HH:MM format>",
      "description": "<Fill with detailed description of the activity>"
    },
    {
      "activity": "<Fill with specific activity name>",
      "date": "<Fill with specific date in DD/MM/YYYY (day, month and year)>",
      "startingTime": "<Fill with starting time in HH:MM format>",
      "endingTime": "<Fill with ending time in HH:MM format>",
      "description": "<Fill with detailed description of the activity>"
    }
  ]
}
   Sample JSON with fake data:
    {
  "activities": [
    {
      "activity": "CompanyX",
      "date": "24/11/2023",
      "startingTime": "09:00",
      "endingTime": "12:00",
      "description": "Did some things"
    }
  ]
}

    """