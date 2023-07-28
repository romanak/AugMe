from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter


class VideoAugmenterByAddingSilentAudio(BaseFFMPEGAugmenter):
    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Adds silent audio to a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        return [
            *self.input_fmt(video_path),
            "-f", "lavfi",
            "-i", "anullsrc",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path,
        ]
