import speech_recognition as sr
import pyttsx3
import openai

# Set your OpenAI API key
openai.api_key = ""

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping. Error!")
        
def generate_response(prompt):
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response['choices'][0]['text']

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()


def chat_gpt_voice_assistant():
    while True:
        print("Say 'START' to start the assistant...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "start":
                    # Record audio
                    filename = "inout.wav"
                    print("Ask your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                            
                    # Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")
                        
                        # Send text to GPT-3 
                        response = generate_response(text)
                        print(f"ChatGPT says: {response}")
                        
                        # Read response using text-to-speech
                        text_to_speech(response)
                        
            except Exception as e:
                print(f"Error: {e}")
                
if __name__ == "__main__":
    chat_gpt_voice_assistant()