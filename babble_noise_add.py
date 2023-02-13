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

        for file in files:
            org_audio, sr = librosa.load(file)
            babble_audio_cut = babble_audio[np.arange(len(org_audio) % len(babble_audio))]

            org_audio = org_audio.astype(np.float32)
            babble_audio_cut = babble_audio_cut.astype(np.float32)

            signal_energy = np.mean(org_audio ** 2)
            noise_energy = np.mean(babble_audio_cut ** 2)
            gain = np.sqrt(10.0 ** (-snr / 10) * signal_energy / noise_energy)

            alfa = np.sqrt(1 / (1 + gain ** 2))
            beta = np.sqrt(gain ** 2 / (1 + gain ** 2))

            org_audio_RMS = np.mean(librosa.feature.rms(y=(alfa * org_audio)))

            babble_audio_RMS = np.mean(librosa.feature.rms(y=(beta * babble_audio_cut)))

            print("SNR: ", 10 * math.log10((org_audio_RMS ** 2) / (babble_audio_RMS ** 2)))

            signal_noise = alfa * org_audio + beta * babble_audio_cut

            """
            plt.plot(signal_noise, color='r')
            plt.plot(org_audio, color='b')
            plt.show()
            """

            file_name = os.path.split(file)
            if file.endswith('.wav'):
                pass
            else:
                sf.write(file_name[0] + '/' + os.path.splitext(file_name[1])[0] +
                         '_babble_' + str(snr) + '.wav', signal_noise, sr, 'PCM_24')
                print('File saved: ', os.path.splitext(file_name[1])[0], '_babble_' + str(snr) + '.wav')


# Funkcja przyjmuje wartości:
# - ścieżka do pliku z babble_speech
# - ścieżka do folderu gdzie znajdują się nagrania mówców
# - wartość SNR

add_babble_noise = BabbleAdd('noise_test_Babble_4.wav',
                             '/Users/Wiking/Desktop/LibriSpeech', snr=40)
add_babble_noise.files_list()
add_babble_noise.add_babble_noise()
