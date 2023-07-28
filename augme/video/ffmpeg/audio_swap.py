from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter
from augme.video.helpers import (
    get_audio_info,
    get_video_info,
    validate_path,
)


class VideoAugmenterByAudioSwap(BaseFFMPEGAugmenter):
    def __init__(self, audio_path: str, audio_offset: float):
        validate_path(audio_path)
        assert audio_offset >= 0, "Offset cannot be a negative number"

        self.audio_path = audio_path
        self.audio_offset = audio_offset

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Swaps the audio of a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        audio_info = get_audio_info(self.audio_path)
        video_info = get_video_info(video_path)

        audio_duration = float(audio_info["duration"])
        audio_sample_rate = float(audio_info["sample_rate"])

        start = self.audio_offset
        end = start + float(video_info["duration"])

        audio_filters = f"atrim={start}:{end},asetpts=PTS-STARTPTS"

        if end > audio_duration:
            pad_len = (end - audio_duration) * audio_sample_rate
            audio_filters += f",apad=pad_len={pad_len}"

        filters = [
            "-i", self.audio_path,
            "-vf", "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-af", audio_filters,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:a", "aac",
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
