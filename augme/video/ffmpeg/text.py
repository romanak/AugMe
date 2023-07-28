from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter
from augme.video.helpers import (
    get_video_info,
    validate_rgb_color,
    TEXT_DIR,
    FONTS_DIR,
)
import os
import random
import string
from math import ceil

class VideoAugmenterByText(BaseFFMPEGAugmenter):
    def __init__(self, font: str, fontsize: float, num_lines: int, opacity: float):
        assert (0 <= opacity <= 1), "Opacity must be a value in the range [0, 1]"
        assert (0 < fontsize < 1), "Fontsize must be a value in the range (0, 1)"

        self.font = font
        self.fontsize = fontsize
        self.num_lines = num_lines
        self.opacity = opacity


    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Overlays random text onto a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        video_info = get_video_info(video_path)

        duration = video_info['duration']
        fontsize = int(video_info['height'] * self.fontsize)
        line_width = video_info['height'] / self.num_lines
        
        longman = os.path.join(TEXT_DIR, "Longman_Communication_3000.txt")
        tocfl = os.path.join(TEXT_DIR, "TOCFL_7517.txt")
        ru = os.path.join(TEXT_DIR, "RU_10000.txt")

        with open(tocfl, 'r', encoding="utf-8") as file:
            chinese = file.read().splitlines()
        with open(longman, 'r', encoding="utf-8") as file:
            english = file.read().splitlines()
        with open(ru, 'r', encoding="utf-8") as file:
            russian = file.read().splitlines()
        
        # choose the most frequent 3000 words
        chinese = chinese[:3000]
        english = english[:3000]
        russian = russian[:3000]

        text = []
        for i in range(self.num_lines):
            # tuple's second element is text length factor
            corpus = random.choice([(chinese, 1.5), (english,0.8), (russian,0.7)])
            text.append(" ".join(random.choices(corpus[0], k=ceil(duration*corpus[1]))))

        text_filters = []
        for i in range(self.num_lines):
            speed = random.uniform(0.4, 1.0)
            color = f"{random.randrange(16**6):06x}"
            text_filter = f"drawtext=fontfile={self.font}:"\
                + f"text='{text[i]}':"\
                + f"fontcolor={color}@{self.opacity}:"\
                + f"fontsize={fontsize}:"\
                + f"box=1:"\
                + f"boxcolor=black@{self.opacity * 0.2}:"\
                + f"x=w-{speed}*100*t:"\
                + f"y={i*line_width},"
            text_filters.append(text_filter)
        text_filters = "".join(text_filters)

        filters = [
            "-vf", text_filters
            + "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-fps_mode", "cfr", # duplicate and drop frames for constant frame rate
            "-r", str(video_info['r_frame_rate']),
            "-c:a", "copy",
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
