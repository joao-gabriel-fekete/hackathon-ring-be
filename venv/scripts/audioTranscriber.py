import whisper

def generateAudioTranscription(audio_path):
    """
    Generate an audio transcription from the given audio file.

    Args:
        audio_path (str): The path to the audio file.

    Returns:
        str: The transcribed text from the audio.
    """
    model = whisper.load_model("base") #Using a larger model makes it take longer to complete
    result = model.transcribe(audio_path)
    return result["text"]