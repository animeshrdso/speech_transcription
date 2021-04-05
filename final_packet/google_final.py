"""from google.cloud import speech_v1 as speech
#from google.cloud.speech_v1 import enums
#from google.cloud.speech_v1.gapic import enums
from google.cloud.gapic.speech.v1 import enums
from google.cloud.speech_v1 import types"""

from pydub import AudioSegment
import io
import os
from google.cloud import speech_v1p1beta1 as speech
#from google.cloud.speech_v1p1beta1 import enums
from google.cloud.gapic.speech.v1 import enums
from google.cloud.speech_v1p1beta1 import types
import wave
from google.cloud import storage

filepath = "input_audio"
output_filepath = "output_audio"

import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="vidfor-39fdc7d43955.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="vidfor-811e69babade.json"

def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'mp3':    
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")

def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate,channels

def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

def google_transcribe(audio_file_name):
    
    file_name = filepath +"/"+ audio_file_name
    mp3_to_wav(file_name)

    # The name of the audio file to transcribe
    file_name = file_name.split('.')[0]+".wav"
    audio_file_name = audio_file_name.split('.')[0]+".wav"
    #frame_rate, channels = frame_rate_channel(wav_path)
    frame_rate, channels = frame_rate_channel(file_name)
    if channels > 1:
        stereo_to_mono(file_name)
        #stereo_to_mono(wav_path)
    
    bucket_name = 'vidfor_speech2text'
    source_file_name = filepath +"/"+ audio_file_name
    destination_blob_name = audio_file_name
    
    upload_blob(bucket_name, source_file_name, destination_blob_name)
    
    gcs_uri = 'gs://vidfor_speech2text/' + audio_file_name
    transcript = ''
    
    client = speech.SpeechClient()
    audio = types.RecognitionAudio(uri=gcs_uri)
    d_config = types.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2
        #max_speaker_count=3 # defaults to 6 speakers
    ) 
    first_alternative = "en-IN"
    config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=frame_rate,
    language_code='en-US',
    #alternative_language_codes=[first_alternative],
    diarization_config=d_config)
    #enable_speaker_diarization=True,
    #diarization_speaker_count=2)
    request = {
        'config': config,
        'audio': audio,
        };
    # Detects speech in the audio file
    #operation = client.long_running_recognize(config, audio)
    operation = client.long_running_recognize(request)
    response = operation.result(timeout=14400)
    result = response.results[-1]
    words_info = result.alternatives[0].words
    
    tag=1
    speaker=""

    for word_info in words_info:
        if word_info.speaker_tag==tag:
            speaker=speaker+" "+word_info.word
        else:
            transcript += "speaker {}: {}".format(tag,speaker) + '\n'
            tag=word_info.speaker_tag
            speaker=""+word_info.word

    transcript += "speaker {}: {}".format(tag,speaker)
    
    delete_blob(bucket_name, destination_blob_name)
    return transcript


def write_transcripts(transcript_filename,transcript):
    f= open(output_filepath +"/"+ transcript_filename,"w+")
    f.write(transcript)
    f.close() 


if __name__ == "__main__":
    for audio_file_name in os.listdir(filepath):
        exists = os.path.isfile(output_filepath + audio_file_name.split('.')[0] + '.txt')
        if audio_file_name.split('.')[1] == "wav":
            continue
        if exists:
            pass
        else:
            print("Name of Audio File:",audio_file_name)
            if audio_file_name==".ipynb_checkpoints":
              continue
            transcript = google_transcribe(audio_file_name)
            transcript_filename = audio_file_name.split('.')[0] + '.txt'
            write_transcripts(transcript_filename,transcript) 
               
            

