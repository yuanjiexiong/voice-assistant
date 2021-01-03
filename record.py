from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave
from setting import WAV_FILE


class recoder:
    NUM_SAMPLES = 2000  # pyaudio内置缓冲大小
    SAMPLING_RATE = 8000  # 取样频率
    LEVEL = 250  # 声音保存的阈值
    COUNT_NUM = 50  # NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音

    def save_wav(self, voice_string):
        wf = wave.open(WAV_FILE, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.SAMPLING_RATE)
        wf.writeframes(np.array(voice_string).tostring())
        wf.close()

    def recoder(self):
        pa = PyAudio()
        stream = pa.open(
            format=paInt16,
            channels=1,
            rate=self.SAMPLING_RATE,
            input=True,
            frames_per_buffer=self.NUM_SAMPLES,
        )
        end_buffer = []
        save_buffer = []
        last_sample_count = -1
        while True:
            # 读入NUM_SAMPLES个取样
            string_audio_data = stream.read(self.NUM_SAMPLES)
            # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            # 计算大于LEVEL的取样的个数
            sample_count = np.sum(audio_data > self.LEVEL)
            print(sample_count)
            if sample_count > self.COUNT_NUM or last_sample_count > self.COUNT_NUM:
                end_buffer = []
                save_buffer.append(string_audio_data)
            else:
                end_buffer.append(string_audio_data)
                if len(save_buffer) > 3 and len(end_buffer) > 2:
                    self.save_wav(save_buffer + end_buffer)
                    return
            last_sample_count = sample_count


def record():
    r = recoder()
    r.recoder()
