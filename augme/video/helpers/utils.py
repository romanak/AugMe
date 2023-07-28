import tempfile
import os
from pathlib import Path
import shutil
from typing import Any, Callable, Dict, List, Optional, Union, Tuple
from PIL import Image
import numpy as np
from augme.video.helpers.constants import EMOJI_DIR, FONTS_DIR


def validate_path(file_path: Path) -> None:
    assert Path(file_path).is_file(), f"Path is invalid: {file_path}"


def make_output_dir(file_path: Path) -> None:
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)


def validate_rgb_color(color: Tuple[int, int, int]) -> None:
    correct_len = len(color) == 3
    correct_values = all(0 <= c <= 255 for c in color)
    assert correct_len and correct_values, "Invalid RGB color specified"


def validate_input_and_output_paths(
    video_path: str, output_path: Optional[str]
) -> Tuple[str, str]:
    validate_path(video_path)
    output_path = output_path or video_path
    make_output_dir(output_path)

    return video_path, output_path


# https://stackoverflow.com/questions/23212435/permission-denied-to-write-to-my-temporary-file
class CustomNamedTemporaryFile:
    """
    This custom implementation is needed because of the following limitation of tempfile.NamedTemporaryFile:

    > Whether the name can be used to open the file a second time, while the named temporary file is still open,
    > varies across platforms (it can be so used on Unix; it cannot on Windows NT or later).
    """
    def __init__(self, mode='wb', suffix=None, delete=True):
        self._mode = mode
        self._delete = delete
        self.suffix = suffix

    def __enter__(self):
        # Generate a random temporary file name
        file_name = os.path.join(
            tempfile.gettempdir(),
            os.urandom(24).hex() + self.suffix
        )
        # Ensure the file is created
        open(file_name, "x").close()
        # Open the file in the given mode
        self._tempFile = open(file_name, self._mode)
        return self._tempFile

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tempFile.close()
        if self._delete:
            os.remove(self._tempFile.name)


def resize_image(
    image: Union[str, Image.Image],
    output_path: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    resample: Any = Image.BILINEAR,
) -> Image.Image:
    
    validate_path(image)
    image = Image.open(image)
    src_mode = image.mode
    im_w, im_h = image.size
    aug_image = image.resize((width or im_w, height or im_h), resample)

    aug_image = aug_image.convert(src_mode)

    JPEG_EXTENSIONS = [".jpg", ".JPG", ".jpeg", ".JPEG"]

    if output_path is not None:
        if (
            any(output_path.endswith(extension) for extension in JPEG_EXTENSIONS)
            or aug_image.mode == "CMYK"
        ):
            aug_image = aug_image.convert("RGB")

        aug_image.save(output_path)


def opacity_image(
    image: Union[str, Image.Image],
    output_path: Optional[str] = None,
    level: float = 1.0,
) -> Image.Image:
    """
    Alter the opacity of an image

    @param image: the path to an image or a variable of type PIL.Image.Image
        to be augmented

    @param output_path: the path in which the resulting image will be stored.
        If None, the resulting PIL Image will still be returned

    @param level: the level the opacity should be set to, where 0 means
        completely transparent and 1 means no transparency at all

    @returns: the augmented PIL Image
    """
    assert 0 <= level <= 1, "level must be a value in the range [0, 1]"

    validate_path(image)
    image = Image.open(image)
    src_mode = image.mode

    image = image.convert(mode="RGBA")
    mask = image.getchannel("A")
    mask = Image.fromarray((np.array(mask) * level).astype(np.uint8))
    background = Image.new("RGBA", image.size, (0, 0, 0, 0))
    aug_image = Image.composite(image, background, mask)

    aug_image = aug_image.convert(src_mode)

    JPEG_EXTENSIONS = [".jpg", ".JPG", ".jpeg", ".JPEG"]

    if output_path is not None:
        if (
            any(output_path.endswith(extension) for extension in JPEG_EXTENSIONS)
            or aug_image.mode == "CMYK"
        ):
            aug_image = aug_image.convert("RGB")

        aug_image.save(output_path)

    return aug_image


def select_random_emoji(emoji_path=EMOJI_DIR, rng=np.random.default_rng()):
    emoji_dir_list = list(Path(emoji_path).glob("*"))
    emoji_dir = rng.choice(emoji_dir_list)
    emoji_picture_list = list(emoji_dir.glob("*.png"))
    emoji_picture = rng.choice(emoji_picture_list)

    return str(emoji_picture)


def select_random_font(font_path=FONTS_DIR, rng=np.random.default_rng()):
    font_path_list = list(Path(font_path).glob("*.otf"))
    font = rng.choice(font_path_list)
    
    return str(font)
