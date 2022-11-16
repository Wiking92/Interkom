import os
from os import walk
import numpy as np
import soundfile as sf
from functools import reduce


class Add_noise:
    def __init__(self, dir_path, min_freq, max_freq):
        self.dir_path = dir_path
        self.min_freq = min_freq
        self.max_freq = max_freq

    def files_list(self):
        files = []

        for (dir_path, dir_names, file_names) in walk(self.dir_path):
            for file in file_names:
                filename_ext = ['.flac', '.wav', '.mp3']
                if file.endswith(tuple(filename_ext)):
                    files.append(os.path.join(dir_path, file))

        return files

    # band limited white noise, min and max freq with 8 different steps
    def band_limited_noise(self, samplerate, samples):
        t = np.linspace(0, samples / samplerate, samples)
        freqs = np.arange(self.min_freq, self.max_freq + 1, 8)
        phases = np.random.rand(len(freqs)) * 2 * np.pi
        signals = [np.sin(2 * np.pi * freq * t + phase) for freq, phase in zip(freqs, phases)]
        noise = reduce(lambda a, b: a + b, signals)
        noise /= np.max(noise)
        return noise

    def add_noise_to_file(self):
        files = self.files_list()
        for file in files:
            signal, sr = sf.read(file)

            print(len(signal))
            print(sr)

            noise = self.band_limited_noise(sr, samples=len(signal))

            # adjustment the noise to the maximum amplitude of signal
            signal_noise = signal + noise * abs(signal).max()

            # Write to wav the signal_noise value
            file_name = os.path.split(file)
            print(file_name[0])
            print(file_name[1])
            if not os.path.exists(file_name[0]):
                os.makedirs(file_name[0])
            sf.write(file_name[0] + os.path.splitext(file_name[1])[0] +
                     '_noise.wav', signal_noise, sr, 'PCM_24')


add_noise = Add_noise('/Users/Wiking/Desktop/LibriSpeech', 50, 800)
add_noise.files_list()
add_noise.add_noise_to_file()
