from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter
from augme.video.helpers import get_audio_info


class VideoAugmenterByNoise(BaseFFMPEGAugmenter):
    def __init__(self, level: int, add_audio_noise: bool):
        self.level = level
        self.add_audio_noise = add_audio_noise

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Adds noise to the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        # video_path, ["-vf", f"boxblur=lr=1.2,noise=c0s={self.level}:allf=t"], output_path
        audio_info = get_audio_info(video_path)
        audio_filter = [
            "-c:a", "copy",
        ]

        if audio_info and self.add_audio_noise:
            audio_filter = [
                "-bsf:a", f"noise={int(self.level / 8)}",
                "-c:a", "aac",
            ]

        filters = [
            "-vf", "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-bsf:v", f"noise={self.level}",
            *audio_filter,
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
