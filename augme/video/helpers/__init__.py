from augme.video.helpers.utils import (
    validate_path,
    validate_input_and_output_paths,
    CustomNamedTemporaryFile,
    validate_rgb_color,
    resize_image,
    opacity_image,
    select_random_emoji,
    select_random_font,
)

from augme.video.helpers.ffmpeg import (
    execute_ffmpeg_cmd,
    execute_ffprobe_cmd,
    get_video_info,
    get_audio_info,
    get_precise_duration,
    extract_frames,
)

from augme.video.helpers.metadata import (
    get_func_kwargs,
    get_metadata,
)

from augme.video.helpers.constants import (
    ASSETS_BASE_DIR,
    AUDIO_ASSETS_DIR,
    VIDEO_ASSETS_DIR,
    TEXT_DIR,
    EMOJI_DIR,
    FONTS_DIR,
    IMG_MASK_DIR,
    DEFAULT_COLOR,
    DEFAULT_FRAME_RATE,
    DEFAULT_SAMPLE_RATE,
    EMOJI_PATH,
    FONT_PATH,
    IMG_MASK_PATH,
    SILENT_AUDIO_PATH,
    SMILEY_EMOJI_DIR,
)

__all__ = [
    # -- utils --
    "validate_path",
    "validate_input_and_output_paths",
    "CustomNamedTemporaryFile",
    "validate_rgb_color",
    "resize_image",
    "opacity_image",
    "select_random_emoji",
    "select_random_font",
    # -- ffmpeg --
    "execute_ffmpeg_cmd",
    "execute_ffprobe_cmd",
    "get_video_info",
    "get_audio_info",
    "get_precise_duration",
    "extract_frames",
    # -- metadata --
    "get_func_kwargs",
    "get_metadata",
    # -- constants --
    "ASSETS_BASE_DIR",
    "AUDIO_ASSETS_DIR",
    "VIDEO_ASSETS_DIR",
    "TEXT_DIR",
    "EMOJI_DIR",
    "FONTS_DIR",
    "IMG_MASK_DIR",
    "DEFAULT_COLOR",
    "DEFAULT_FRAME_RATE",
    "DEFAULT_SAMPLE_RATE",
    "EMOJI_PATH",
    "FONT_PATH",
    "IMG_MASK_PATH",
    "SILENT_AUDIO_PATH",
    "SMILEY_EMOJI_DIR",
]
