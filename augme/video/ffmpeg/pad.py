from typing import List, Tuple
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter
from augme.video.helpers import get_video_info, validate_rgb_color


class VideoAugmenterByPadding(BaseFFMPEGAugmenter):
    def __init__(self, w_factor: float, h_factor: float, color: Tuple[int, int, int]):
        assert w_factor >= 0, "w_factor cannot be a negative number"
        assert h_factor >= 0, "h_factor cannot be a negative number"
        validate_rgb_color(color)

        self.w_factor = w_factor
        self.h_factor = h_factor
        self.hex_color = "%02x%02x%02x" % color

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Adds padding to the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        video_info = get_video_info(video_path)

        left = int(video_info["width"] * self.w_factor)
        top = int(video_info["height"] * self.h_factor)

        filters = [
            "-vf",  f"pad=width={left*2}+ceil(iw/2)*2:height={top*2}+ceil(ih/2)*2"
            + f":x={left}:y={top}:color={self.hex_color}",
            "-c:a", "copy",
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
