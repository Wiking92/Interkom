import math
import os
from os import walk
import soundfile as sf
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal


class NotchFiltered:

    def __init__(self, dir_path, freqs):
        self.dir_path = dir_path
        self.freqs = freqs

    def files_list(self):
        files = []
        for (dir_path, dir_names, file_names) in walk(self.dir_path):
            for file in file_names:
                filename_ext = ['.flac', '.wav', '.mp3']
                if file.endswith(tuple(filename_ext)):
                    files.append(os.path.join(dir_path, file))

        return files

    # Function to create notched filteres
    def notch_filtered(self, notch_freq, quality_factor, sample_rate, output_signal):
        b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, sample_rate)
        output_signal = signal.filtfilt(b_notch, a_notch, output_signal)

        return output_signal

    def add_noise_to_file(self):
        files = self.files_list()
        freqs = self.freqs

        for file in files:
            output_signal, sr = sf.read(file)
            original_signal, sr = sf.read(file)

            print(len(output_signal))
            print(sr)

            # Creating additive gaussian white noise
            rms = math.sqrt(np.mean(original_signal ** 2))
            original_noise = np.random.normal(0, rms, original_signal.shape[0])

            # Output signal is a sum of original signal notched where in place witch filtered frequencies
            # is additive white gaussian noise
            # Normalization of noise signal is create on a base of maximum amplitude of original signal

            for freq in freqs:
                notched_noise = original_noise - self.notch_filtered(freq, 5, sr, original_noise)
                output_signal = self.notch_filtered(freq, 5, sr, output_signal)
                output_signal = output_signal + notched_noise * abs(original_noise).max()

                """
                plt.specgram(notched_noise, Fs=sr)
                plt.show()
                plt.specgram(output_signal, Fs=sr)
                plt.show()
                """

            # Write to wav the signal_noise value
            file_name = os.path.split(file)
            sf.write(file_name[0] + '/' + os.path.splitext(file_name[1])[0] +
                     '_notched.wav', output_signal, sr, 'PCM_24')


# Class  NotchFiltered arguments are: directory path, list of frequencies to create notched filters
notchedFiltered = NotchFiltered('/Users/Wiking/Desktop/LibriSpeech', [500, 1000, 3000, 5000])
notchedFiltered.files_list()
notchedFiltered.add_noise_to_file()
