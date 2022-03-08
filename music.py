import pygame, numpy, time

def fade_music(volume_in, direction):
    """ Function to fade in/out music on mayor screen changes

        Args:
            volume_in: Float                - startvalue for the volume
            direction: String 'in'/'out'    - decides if music fades in or out
    """

    if direction == 'out':      # Fade out Backtrack
        for volume in numpy.arange(volume_in, volume_in - 0.15, -0.01):
            pygame.mixer.music.set_volume(volume)
            time.sleep(0.03)

    if direction == 'in':       # Fade in Backtrack
        for volume in numpy.arange(volume_in - 0.15, volume_in, 0.01):
            pygame.mixer.music.set_volume(volume)
            time.sleep(0.03)