from math import ceil
from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter
from augme.video.helpers import (
    get_video_info,
    get_audio_info,
    validate_path,
)


class VideoAugmenterByBlending(BaseFFMPEGAugmenter):
    def __init__(self, overlay_path: str, opacity: float, merge_audio: bool):
        validate_path(overlay_path)

        self.overlay_path = overlay_path
        self.opacity = opacity
        self.merge_audio = merge_audio


    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Blends two videos together

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        video_info = get_video_info(video_path)
        audio_info = get_audio_info(video_path)
        overlay_video_info = get_video_info(self.overlay_path)
        overlay_audio_info = get_audio_info(self.overlay_path)

        duration = video_info['duration']
        n_loops = ceil(duration / overlay_video_info['duration'])

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
            "-stream_loop", str(n_loops),
            "-i", self.overlay_path,
            "-t", f"{video_info['duration']}",
            "-filter_complex",
            f"[1:v:0]scale=w={video_info['width']}:h={video_info['height']}[1v];"
            + f"[0:v:0][1v]blend=all_mode=overlay:all_opacity={self.opacity}[bv];"
            + "[bv]pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2[v]"
            + audio_filter,
            "-map", "[v]",
            *audio_map,
            "-fps_mode", "cfr", # duplicate and drop frames for constant frame rate
            "-r", str(video_info['r_frame_rate']),
            *audio_codec,
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
