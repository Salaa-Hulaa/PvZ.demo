import numpy as np
from scipy.io import wavfile
import os

def generate_tone(freq, duration, amplitude=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave

def generate_sound_effects():
    if not os.path.exists('sounds'):
        os.makedirs('sounds')
        
    # 植物放置音效
    plant_sound = generate_tone(440, 0.1) * np.exp(-3 * np.linspace(0, 1, 4410))
    wavfile.write('sounds/plant.wav', 44100, plant_sound.astype(np.float32))
    
    # 收集阳光音效
    collect_sound = generate_tone(880, 0.15) * np.exp(-5 * np.linspace(0, 1, 6615))
    wavfile.write('sounds/collect_sun.wav', 44100, collect_sound.astype(np.float32))
    
    # 僵尸被击中音效
    hit_sound = generate_tone(220, 0.1) * np.exp(-10 * np.linspace(0, 1, 4410))
    wavfile.write('sounds/zombie_hit.wav', 44100, hit_sound.astype(np.float32))
    
    # 僵尸吃植物音效
    eat_sound = generate_tone(110, 0.2) * np.exp(-3 * np.linspace(0, 1, 8820))
    wavfile.write('sounds/zombie_eat.wav', 44100, eat_sound.astype(np.float32))
    
    # 射击音效
    shoot_sound = generate_tone(660, 0.05) * np.exp(-20 * np.linspace(0, 1, 2205))
    wavfile.write('sounds/shoot.wav', 44100, shoot_sound.astype(np.float32))
    
    # 菜单点击音效
    menu_sound = generate_tone(550, 0.05) * np.exp(-15 * np.linspace(0, 1, 2205))
    wavfile.write('sounds/menu_click.wav', 44100, menu_sound.astype(np.float32))
    
    # 游戏结束音效
    game_over_sound = np.concatenate([
        generate_tone(440, 0.2),
        generate_tone(330, 0.2),
        generate_tone(220, 0.4)
    ]) * 0.5
    wavfile.write('sounds/game_over.wav', 44100, game_over_sound.astype(np.float32))
    
    # 胜利音效
    victory_sound = np.concatenate([
        generate_tone(440, 0.2),
        generate_tone(550, 0.2),
        generate_tone(660, 0.4)
    ]) * 0.5
    wavfile.write('sounds/victory.wav', 44100, victory_sound.astype(np.float32))
    
    # 背景音乐
    duration = 10.0  # 10秒循环
    t = np.linspace(0, duration, int(44100 * duration))
    music = (0.3 * np.sin(2 * np.pi * 220 * t) + 
             0.2 * np.sin(2 * np.pi * 440 * t) +
             0.1 * np.sin(2 * np.pi * 880 * t))
    wavfile.write('sounds/background.wav', 44100, music.astype(np.float32))

if __name__ == '__main__':
    generate_sound_effects()
