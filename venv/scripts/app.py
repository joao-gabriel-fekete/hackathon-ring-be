from time import sleep

from flask import Flask, request, jsonify
from responseGenerator import generateSummary
from audioTranscriber import generateAudioTranscription
import os
import uuid
import json

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    """
        A function that summarizes the given data.

        Args:
            None

        Returns:
            str: The generated summary of the data.
    """
    return generateSummary(request.form)


@app.route('/audioSummary', methods=['POST'])
def summarizeAudio():
    """
       Generates an audio summary based on the provided audio file.

       Parameters:

       Returns:
       - A JSON object containing the generated audio summary.

       Example usage:
       summarizeAudio()
   """
    audio_filename = f"audio{uuid.uuid4()}.mp3"
    audio_path = os.path.join("recordings/", audio_filename)
    audio_file = request.files['audio']
    audio_file.save(audio_path)

    transcription = generateAudioTranscription(audio_path)
    transcriptionDict = {"text": transcription}
    transcriptionDict.update(request.form)
    print(type(transcriptionDict))
    print("\n\n")

    return jsonify(generateSummary(transcriptionDict))

if __name__ == '__main__':
    app.run(port=8080)