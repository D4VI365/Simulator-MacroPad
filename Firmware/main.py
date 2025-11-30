import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeyMatrix, DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.macros import Macros # Importa Macros

# Inizializza la tastiera
keyboard = KMKKeyboard()

# Aggiunge il supporto per i tasti multimediali (Volume, etc.)
keyboard.extensions.append(MediaKeys())

# -----------------------------------------------------------
# 1. CONFIGURAZIONE MATRICE (BUTTON GRID)
# -----------------------------------------------------------
# Rows (Output/Input): Pin 1(A0), Pin 2(A1), Pin 3(A2)
# Cols (Input/Output): Pin 4(A3), Pin 5(D6), Pin 6(D7), Pin 7(D0)
# Diodi: Anodo su Switch, Catodo su Row -> COL2ROW

keyboard.matrix = KeyMatrix(
    rows=(board.A0, board.A1, board.A2),
    cols=(board.A3, board.D6, board.D7, board.D0),
    diode_orientation=DiodeOrientation.COL2ROW
)

# -----------------------------------------------------------
# 2. CONFIGURAZIONE LED (SK6812)
# -----------------------------------------------------------
# Pin D2, 2 LED totali.
# Usiamo l'estensione RGB di KMK.

rgb = RGB(
    pixel_pin=board.D2,
    num_pixels=2,
    val_limit=255,
    hue_default=85,  # Parte VERDE (85/255 nel ciclo colore KMK)
    sat_default=255,
    val_default=150, # Luminosità iniziale
    rgb_order=(0, 1, 2, 3), # Ordine per SK6812/RGBW
)
keyboard.extensions.append(rgb)

# -----------------------------------------------------------
# 3. LOGICA CUSTOM: ENCODER E GRADAZIONE COLORE
# -----------------------------------------------------------
# Questa classe gestisce il cambio colore da Verde a Rosso (Hue 85 -> 0)
class VolumeColorControl:
    def __init__(self, rgb_ext):
        self.rgb = rgb_ext
        self.level = 0
        self.max_level = 20 

    def update_color(self):
        if self.level > self.max_level: self.level = self.max_level
        if self.level < 0: self.level = 0
        
        ratio = self.level / self.max_level
        new_hue = int(85 * (1 - ratio))
        
        self.rgb.set_hsv_fill(new_hue, 255, 150)

    def vol_up(self, *args, **kwargs):
        self.level += 1
        self.update_color()
        keyboard.tap_key(KC.VOLU) # Invia segnale volume al PC

    def vol_down(self, *args, **kwargs):
        self.level -= 1
        self.update_color()
        keyboard.tap_key(KC.VOLD) # Invia segnale volume al PC

# Inizializziamo il controller
vol_ctrl = VolumeColorControl(rgb)

# Aggiungiamo le macro per il controller colore
keyboard.modules.append(Macros())

# -----------------------------------------------------------
# 4. CONFIGURAZIONE ENCODER
# -----------------------------------------------------------
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

# Pin A = D3, Pin B = D4
encoder_handler.pins = ((board.D3, board.D4, None, False),)

# Mappiamo l'encoder per usare le nostre funzioni custom
encoder_handler.map = [
    (( KC.MACRO(vol_ctrl.vol_up), KC.MACRO(vol_ctrl.vol_down) ),)
]

# -----------------------------------------------------------
# 5. KEYMAP (I TASTI DELLA GRIGLIA)
# -----------------------------------------------------------
# Mappa 3x4: Tasti funzione da F13 a F24.
# RIGA 1 (in alto): F13, F14, F15, F16
# RIGA 2 (al centro): F17, F18, F19, F20
# RIGA 3 (in basso): F21, F22, F23, F24

keyboard.keymap = [
    [
        KC.F13, KC.F14, KC.F15, KC.F16,
        KC.F17, KC.F18, KC.F19, KC.F20,
        KC.F21, KC.F22, KC.F23, KC.F24
    ]
]

if __name__ == '__main__':
    vol_ctrl.update_color() # Inizializza i LED al colore di partenza (Verde)
    keyboard.go()