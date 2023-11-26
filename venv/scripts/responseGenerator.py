from datetime import datetime
import json
import re

from palmConfig import *
from promptResources import *


def cleanOutput(response):
    """
    Cleans the output of a response by extracting a JSON-like object from it.

    Parameters:
    - response (str): The response string to be cleaned.

    Returns:
    - str or None: The cleaned JSON-like object if found, None otherwise.
    """
    pattern = r'(?s){.*}'
    match = re.search(pattern, response)
    if match:
        return match.group(0)
    else:
        return None


def generateSummary(jsonInfo):
    """
    Generates a summary based on the given JSON information.

    Args:
        jsonInfo (dict): The JSON object containing the necessary information.

    Returns:
        dict: A dictionary containing the generated summary or an error message if no data is available.
    """
    currentDate = datetime.now().strftime("%Y/%d/%m %H:%M")
    basePrompt = getMostAccuratePrompt(jsonInfo['text'], currentDate)
    if isinstance(basePrompt, dict):
        return basePrompt
    finalPrompt = promptAggregatorWithDateAndBaseKnowledge(jsonInfo, basePrompt, currentDate)
    response = palm.generate_text(prompt=finalPrompt, max_output_tokens=5000)
    print(response.result)
    responseClean = cleanOutput(response.result)
    if responseClean is not None:
        return json.loads(responseClean)
    else:
        return {"error": "no available data"}


def getMostAccuratePrompt(text, date):
    """
    Chooses the appropriate prompt based on the input text.

    Args:
        text (str): The input text.
        date (str): The date.

    Returns:
        String Template: The candidate prompt.

    Raises:
        None
    """
    basePrompt = getPromptChoser()
    finalPrompt = promptAggregatorWithDate(text, basePrompt, date)
    response = palm.generate_text(prompt=finalPrompt, max_output_tokens=5000).result
    if response == "Today":
        candidatePrompt = getSummarizerCurrentDay()
        print("Today")
    elif response == "Yesterday":
        candidatePrompt = getSummarizerDayBefore()
        print("Yesterday")
    elif response == "Future":
       candidatePrompt = {"error": "You should not submit dates ahead of the current moment. Please try again"}
       print("Yesterday")
    elif response == "Another day":
        candidatePrompt = getSummarizerOtherDays()
        print("Another day")
    else:
        candidatePrompt = {"error": "The messsage could not be analyzed correctly. Please try again"}
        print("Unkown")


    return candidatePrompt


def promptAggregatorWithDate(text, basePrompt, date):
    """
    Generates a new prompt by replacing placeholders in the base prompt string with the given text and date.

    Args:
        text (str): The text to substitute in the base prompt string.
        basePrompt (str): The base prompt string containing placeholders.
        date (str): The current date to substitute in the base prompt string.

    Returns:
        str: The new prompt string with the placeholders replaced.
    """
    return basePrompt.substitute(
        text=text,
        current_date=date
    )

def promptAggregatorWithDateAndBaseKnowledge(json, basePrompt, date):
    """
    Generates a complete prompt to be executed by the PALM model.

    Args:
        json (dict): The JSON data used to generate the function comment.
        basePrompt (str): The base prompt for the function comment.
        date (str): The current date.

    Returns:
        str: The generated prompt.
    """
    baseKnowledgePrompt = getBaseKnowledgePrompt().substitute(
        activities=json['activities'],
        defaultStartingTime=json['defaultStartingTime'],
        defaultEndingTime=json['defaultEndingTime'],
        breakDefaultStartTime=json['breakDefaultStartTime'],
        breakDefaultEndTime=json['breakDefaultEndTime']
    )
    return (baseKnowledgePrompt + basePrompt.substitute(
        text=json['text'],
        current_date=date
    ) + sampleFormat())
        # + getThingsNotToInclude())