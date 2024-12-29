import pygame
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music = None
        self.sound_enabled = True
        self.music_enabled = True
        self.load_sounds()
        
    def load_sounds(self):
        # 加载音效
        sound_files = {
            'plant': 'plant.wav',
            'collect_sun': 'collect_sun.wav',
            'zombie_hit': 'zombie_hit.wav',
            'chomp': 'zombie_eat.wav',
            'plant_death': 'plant.wav',
            'shoot': 'shoot.wav',
            'menu_click': 'menu_click.wav',
            'game_over': 'game_over.wav',
            'victory': 'victory.wav'
        }
        
        for sound_name, file_name in sound_files.items():
            try:
                sound_path = resource_path(os.path.join('sounds', file_name))
                if os.path.exists(sound_path):
                    sound = pygame.mixer.Sound(sound_path)
                    # 调整音量
                    if sound_name in ['chomp', 'plant_death']:
                        sound.set_volume(0.3)  # 降低啃食和植物死亡的音量
                    elif sound_name in ['shoot', 'zombie_hit']:
                        sound.set_volume(0.5)  # 适当降低射击和僵尸受击的音量
                    elif sound_name in ['game_over', 'victory']:
                        sound.set_volume(0.8)  # 保持游戏结束和胜利音效响亮
                    self.sounds[sound_name] = sound
            except Exception as e:
                print(f"Could not load sound: {sound_path} - {str(e)}")
                
    def play_sound(self, sound_name):
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
            
    def play_music(self, music_file):
        if self.music_enabled:
            try:
                music_path = resource_path(os.path.join('sounds', music_file))
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            except Exception as e:
                print(f"Could not load music: {music_path} - {str(e)}")
                
    def stop_music(self):
        pygame.mixer.music.stop()
        
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()
        else:
            self.play_music('background.wav')
