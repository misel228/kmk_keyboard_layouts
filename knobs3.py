# My Keyboard definition for an Anavi Knobs 3 - https://anavi.technology
import board

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.extensions.LED import LED
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.encoder import EncoderHandler
from kmk.scanners.keypad import KeysScanner
from kmk.modules.layers import Layers as _Layers
from kmk.modules.mouse_keys import MouseKeys

knob = KMKKeyboard()

# use Putty and connect with 9600 8N1
#knob.debug_enabled = True

# enable special keys
knob.modules.append(MouseKeys())
knob.extensions.append(MediaKeys())

knob.matrix = KeysScanner([])

# Rotary encoders that also acts as keys
encoder_handler = EncoderHandler()
encoder_handler.divisor = 2 # default 4 makes rotaries skippy
encoder_handler.pins = (
    (board.D1, board.D2, board.D0),
    (board.D9, board.D10, board.D3),
    (board.D7, board.D8, board.D6),
)

rgb_ext = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    val_limit=100,
    val_default=25,
    hue_default=85,
)
knob.extensions.append(rgb_ext)

led_ext = LED(led_pin=board.LED,brightness=75)
knob.extensions.append(led_ext)


# switch between red green and blue for layers
class Layers(_Layers):
    last_top_layer = 0
    hues = (85, 0, 14)
    
    def after_hid_send(self, knob):
        if knob.active_layers[0] != self.last_top_layer:
            self.last_top_layer = knob.active_layers[0]
            rgb_ext.set_hsv_fill(self.hues[self.last_top_layer], 255, 25)

knob.modules.append(Layers())

encoder_handler.map = [ 
    # Layer 1
    (
        (KC.VOLD, KC.VOLU, KC.MUTE), 
        (KC.MW_DOWN, KC.MW_UP, KC.MPLY),
        (KC.RIGHT, KC.LEFT, KC.TO(1))
    ),

    # Video controls for YT in a browser or Video LAN Client
    # Top Click = Play/Pause
    # Top rotate = control playback speed
    # Middle Click = TBD
    # Middle Rotate = next/prev frame (VLC doesn't have prev frame so rewind 3s)
    # Bottom Click = Change Layer
    # Bottom Rotate = rew/forward 10s

    # Layer 2 "youtube"
    (
        (KC.LEFT_ANGLE_BRACKET, KC.RIGHT_ANGLE_BRACKET, KC.SPACE),
        (KC.COMMA, KC.DOT, KC.K), 
        (KC.L, KC.J, KC.TO(2))
    ),
    
    # Layer 3 "VLC"
    (
        (KC.KP_MINUS, KC.KP_PLUS, KC.SPACE),
        (KC.E, KC.LSHIFT(KC.LEFT), KC.TRNS),
        (KC.LALT(KC.RIGHT), KC.LALT(KC.LEFT), KC.TO(0))
    ),
]
knob.modules.append(encoder_handler)

print('ANAVI Knobs 3')

# this is just placebo
knob.keymap = [
    [KC.MUTE],
]

# kick off everything
if __name__ == '__main__':
    knob.go()
