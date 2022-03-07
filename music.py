import pygame, numpy, time

def fade_music(volume_in, direction):
    # Fade out Backtrack
    if direction == 'out':
        for volume in numpy.arange(volume_in, volume_in - 0.3, -0.01):
            pygame.mixer.music.set_volume(volume)
            time.sleep(0.03)

    # Fade in Backtrack
    if direction == 'in':
        for volume in numpy.arange(volume_in, volume_in + 0.3, 0.01):
            pygame.mixer.music.set_volume(volume)
            time.sleep(0.03)