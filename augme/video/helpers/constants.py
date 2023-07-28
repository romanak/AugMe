import os

MODULE_BASE_DIR = os.path.dirname((os.path.dirname(os.path.dirname(__file__))))

# asset paths
ASSETS_BASE_DIR = os.path.join(MODULE_BASE_DIR, "assets")
AUDIO_ASSETS_DIR = os.path.join(ASSETS_BASE_DIR, "audio")
VIDEO_ASSETS_DIR = os.path.join(ASSETS_BASE_DIR, "video")
TEXT_DIR = os.path.join(ASSETS_BASE_DIR, "text")
EMOJI_DIR = os.path.join(ASSETS_BASE_DIR, "twemojis")
FONTS_DIR = os.path.join(ASSETS_BASE_DIR, "fonts")
IMG_MASK_DIR = os.path.join(ASSETS_BASE_DIR, "masks")

# color constants
DEFAULT_COLOR = (0, 0, 0)
WHITE_RGB_COLOR = (255, 255, 255)
RED_RGB_COLOR = (255, 0, 0)

# audio & video rate constants
DEFAULT_FRAME_RATE = 10
DEFAULT_SAMPLE_RATE = 44100

# audio assets
SILENT_AUDIO_PATH = os.path.join(AUDIO_ASSETS_DIR, "silent.flac")

# image augmentation assets
IMG_MASK_PATH = os.path.join(IMG_MASK_DIR, "dfdc_mask.png")
SMILEY_EMOJI_DIR = os.path.join(EMOJI_DIR, "smileys")
EMOJI_PATH = os.path.join(SMILEY_EMOJI_DIR, "smiling_face_with_heart_eyes.png")
FONT_PATH = os.path.join(FONTS_DIR, "NotoNaskhArabic-Regular.ttf")

# text augmentation assets
ENGLISH_WORDLIST = os.path.join(TEXT_DIR, "Longman_Communication_3000.txt")
RUSSIAN_WORDLIST = os.path.join(TEXT_DIR, "RU_10000.txt")
CHINESE_WORDLIST = os.path.join(TEXT_DIR, "TOCFL_7517.txt")
