# speech_transcription
Speech to Text using different available APIs

* Initial Experiments
* We did some initial experiments using personal demo audio using different APIs such as Google's Speech API and IBM Watson's API.
* We also did some experiments using the open source software of CMU know as CMU Sphinx.
* We found that Google and IBM's API were working robustly in comparison to Sphinx for transcription.
* About 8 different APIs (both paid and unpaid) are available on Pythons library known as SpeechRecognition - Install using: !pip install SpeechRecognition
* Further analysis has to be done to choose API/Open Source Software for transcription of multiple people during a live video call as well as for local languages like Hindi.
* Further integration of Python transcription file is needed with VidFor.

Speech to Text for Multiple Speakers 

* The APIs available on Python's SpeechRecognition library cannot provide speaker diarization (detection of multiple speakers during video calls).
* For Speaker Diarization , different cloud based Speech to Text APIs such as Google Cloud Platform and AWS can be used.
* These can be used to create an API client on respective cloud platforms and then use a bucket for transcription of audio speech files (.wav format) using Speaker diarization for multiple speakers. 
* The input files can be saved in the buckets and transcribed files can be directly saved separately.
* [AWS_Speech2Txt_diarization](https://github.com/animeshrdso/speech_transcription/blob/main/AWS_Speech2Txt_diarization.ipynb) and [Google_Speech2Txt_diarization](https://github.com/animeshrdso/speech_transcription/blob/main/Google_Speech2Txt_diarization.ipynb) are initial code implementations for detecting multiple speakers, the files can be run on Colaboratory or Local Server.
* [Sample_Speaker_Diarization_Results](https://github.com/animeshrdso/speech_transcription/blob/main/Sample%20_Results_Speaker_Diarization_Google.txt) shows an example of how we get the transcribed files using Google's Cloud Based API.

# How to Run
* Download the repository and root the working directory to final_packet folder.
* Run the python file (google_final.py) in final_packet to get the transcription results in output folder for input audio files in input folder (Required format: .mp3).
* Note: Need to provide a private Google API Credential as a json file in final_packet folder to create environment, running the .py file will automatically create the environment.
Dependencies needed to be installed beforehand:
* Numpy: Install using - pip install numpy
* Google-Cloud-Speech: Install using - pip install --upgrade google-cloud-speech
* Google-Gapic-v1 : Install using - pip install gapic-google-cloud-speech-v1
* Pydub: Install using - pip install pydub

If conda based environment is used to run .py file then similar dependencied are required to install using conda.
