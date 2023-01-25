import os
from os import walk
import librosa
import math
import numpy as np
from matplotlib import pyplot as plt
import soundfile as sf


class BabbleAdd:

    def __init__(self, bubble_file_path, org_file_path, snr):
        self.bubble_file_path = bubble_file_path
        self.org_file_path = org_file_path
        self.snr = snr

    def files_list(self):
        files = []
        for (dir_path, dir_names, file_names) in walk(self.org_file_path):
            for file in file_names:
                filename_ext = ['.flac', '.wav', '.mp3']
                if file.endswith(tuple(filename_ext)):
                    files.append(os.path.join(dir_path, file))

        return files

    def add_babble_noise(self):
        files = self.files_list()
        babble_file_path = self.bubble_file_path
        babble_audio, sr = librosa.load(babble_file_path)

        snr = self.snr
        babble_audio_RMS = np.mean(librosa.feature.rms(y=babble_audio))
        for file in files:
            org_audio, sr = librosa.load(file)

            org_audio_RMS = np.mean(librosa.feature.rms(y=org_audio))
            babble_audio = babble_audio[np.arange(len(org_audio) % len(babble_audio))]

            req_RMS = math.sqrt((org_audio_RMS**2)/(10**(snr/10)))

            alfa = req_RMS/babble_audio_RMS
            signal_noise = org_audio + alfa * babble_audio

            plt.plot(org_audio)
            plt.show()

            plt.plot(signal_noise)
            plt.show()

            file_name = os.path.split(file)
            if file.endswith('.wav'):
                pass
            else:
                sf.write(file_name[0] + '/' + os.path.splitext(file_name[1])[0] +
                         '_babble_' + str(snr) + '_.wav', signal_noise, sr, 'PCM_24')
                print('File saved: ', os.path.splitext(file_name[1])[0], '_babble_' + str(snr) + '_.wav')

add_babble_noise = BabbleAdd('noise_test_Babble_1.wav',
                             '/Users/Wiking/Desktop/LibriSpeech', 10)
add_babble_noise.files_list()
add_babble_noise.add_babble_noise()