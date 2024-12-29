import numpy as np
from scipy.io import wavfile
import os

def note(freq, duration, amplitude=0.3, sample_rate=44100):
    """生成一个音符"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    # 添加泛音使声音更丰富
    wave = (amplitude * np.sin(2 * np.pi * freq * t) +
            amplitude/2 * np.sin(4 * np.pi * freq * t) +
            amplitude/4 * np.sin(6 * np.pi * freq * t))
    # 添加淡入淡出效果
    fade = 0.02  # 20ms淡入淡出
    fade_len = int(fade * sample_rate)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    wave[:fade_len] *= fade_in
    wave[-fade_len:] *= fade_out
    return wave

def chord(freqs, duration, amplitude=0.3):
    """生成一个和弦"""
    return sum(note(f, duration, amplitude/len(freqs)) for f in freqs)

def generate_background_music():
    # 音符频率
    C4 = 261.63
    D4 = 293.66
    E4 = 329.63
    F4 = 349.23
    G4 = 392.00
    A4 = 440.00
    B4 = 493.88  # 添加B4音符
    
    # 创建一个欢快的旋律
    melody = []
    
    # 第一部分
    pattern1 = [
        (E4, 0.25), (G4, 0.25), (E4, 0.25), (D4, 0.25),
        (C4, 0.5), (D4, 0.5),
        (E4, 0.25), (G4, 0.25), (E4, 0.25), (D4, 0.25),
        (C4, 1.0)
    ]
    
    # 第二部分
    pattern2 = [
        (D4, 0.25), (F4, 0.25), (D4, 0.25), (C4, 0.25),
        (D4, 0.5), (E4, 0.5),
        (F4, 0.25), (A4, 0.25), (G4, 0.25), (F4, 0.25),
        (E4, 1.0)
    ]
    
    # 组合旋律
    for _ in range(2):  # 重复两次
        for freq, dur in pattern1:
            melody.append(note(freq, dur))
        for freq, dur in pattern2:
            melody.append(note(freq, dur))
    
    # 添加和弦伴奏
    chords = []
    chord_progression = [
        ([C4, E4, G4], 2.0),  # C major
        ([G4, B4, D4], 2.0),  # G major
        ([A4, C4, E4], 2.0),  # A minor
        ([F4, A4, C4], 2.0)   # F major
    ]
    
    for freqs, dur in chord_progression * 2:  # 重复两次
        chords.append(chord(freqs, dur, 0.15))  # 降低和弦音量
    
    # 合并旋律和和弦
    melody_wave = np.concatenate(melody)
    chord_wave = np.concatenate(chords)
    
    # 确保两个波形长度相同
    min_len = min(len(melody_wave), len(chord_wave))
    combined = melody_wave[:min_len] + chord_wave[:min_len]
    
    # 标准化音量
    combined = combined / np.max(np.abs(combined))
    
    # 保存音乐
    if not os.path.exists('sounds'):
        os.makedirs('sounds')
    wavfile.write('sounds/background.wav', 44100, (combined * 0.7).astype(np.float32))

if __name__ == '__main__':
    generate_background_music()
