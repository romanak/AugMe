from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter
from augme.video.helpers import get_video_info, validate_path, get_audio_info
from math import ceil


class VideoAugmenterByOverlay(BaseFFMPEGAugmenter):
    def __init__(
        self,
        overlay_path: str,
        x_factor: float,
        y_factor: float,
        merge_audio: bool,
    ):
        validate_path(overlay_path)
        assert 0 <= x_factor <= 1, "x_factor must be a value in the range [0, 1]"
        assert 0 <= y_factor <= 1, "y_factor must be a value in the range [0, 1]"

        self.overlay_path = overlay_path
        self.x_factor = x_factor
        self.y_factor = y_factor
        self.merge_audio = merge_audio

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Overlays media onto the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        video_info = get_video_info(video_path)
        audio_info = get_audio_info(video_path)
        overlay_audio_info = get_audio_info(self.overlay_path)

        x = int(video_info["width"] * self.x_factor)
        y = int(video_info["height"] * self.y_factor)

        audio_filter = ""
        audio_codec = ["-c:a", "copy",]
        if (self.merge_audio and audio_info and overlay_audio_info):
            audio_filter = ";[0:a:0][1:a:0]amerge=inputs=2,pan=stereo|c0<c0+c2|c1<c1+c3[a]"
            audio_map = ["-map",  "[a]",]
            audio_codec = [
                "-c:a", "aac", # audio encoder
                "-r:a", "44100", # audio sample rate
                "-b:a", "128k", # audio bit rate
                "-ac", "2", # audio channels
            ]
        elif (self.merge_audio and overlay_audio_info):
            audio_map = ["-map", "1:a",]
        else:
            audio_map = ["-map", "0:a?",]

        filters = [
            "-i", self.overlay_path,
            "-t", str(video_info["duration"]),
            "-filter_complex", f"[0:v][1:v]overlay=x={x}:y={y}[ov];"
            + "[ov]pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2[v]"
            + audio_filter,
            "-map", "[v]",
            *audio_map,
            *audio_codec,
            "-fps_mode", "cfr", # duplicate and drop frames for constant frame rate
            "-r", str(video_info['r_frame_rate']),
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
