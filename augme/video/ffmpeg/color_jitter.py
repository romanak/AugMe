from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter


class VideoAugmenterByColorJitter(BaseFFMPEGAugmenter):
    def __init__(
        self,
        brightness_factor: float,
        contrast_factor: float,
        saturation_factor: float,
    ):
        assert (
            -1.0 <= brightness_factor <= 1.0
        ), "Brightness factor must be a value in the range [-1.0, 1.0]"
        assert (
            -1000.0 <= contrast_factor <= 1000.0
        ), "Contrast factor must be a value in the range [-1000, 1000]"
        assert (
            0.0 <= saturation_factor <= 3.0
        ), "Saturation factor must be a value in the range [0.0, 3.0]"

        self.brightness_factor = brightness_factor
        self.contrast_factor = contrast_factor
        self.saturation_factor = saturation_factor

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Color jitters the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        filters = [
            "-vf", f"eq=brightness={self.brightness_factor}"
            + f":contrast={self.contrast_factor}"
            + f":saturation={self.saturation_factor},"
            + "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-c:a", "copy",
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
