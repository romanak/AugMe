import os 
from pathlib import Path
import numpy as np
import augme.video as amv
import json


def select_random_audio(audio_path, rng=np.random.default_rng()):
    audio_path_list = list(Path(audio_path).glob("*.mp3"))
    audio = rng.choice(audio_path_list)
    
    return str(audio)


def get_font_path():
    # ffmpeg only accepts posix-style relative directory of fontfile
    working_directory = os.path.dirname(__file__)
    font_path = amv.helpers.select_random_font(rng=rng)
    font_path = os.path.relpath(font_path, working_directory)
    font_path = Path(font_path).as_posix()

    return str(font_path)


# video1 is the video we want to augment
video1 = "video/Q100001.mp4"
# video2-video4 are videos for overlay, blend and stack augmentations
video2 = "video/Q100002.mp4"
video3 = "video/Q100003.mp4"
video4 = "video/Q100004.mp4"
audio_dir = "audio"

seed = 123456
rng = np.random.default_rng(seed)

# Random parameters for video augmentation
font_path = get_font_path()
noise_level = rng.integers(20000, 1000000)
audio_path = select_random_audio(audio_dir, rng=rng)
blend_opacity = rng.uniform(0.2, 0.8)
blur_sigma = rng.uniform(1, 10)
brightness_level = rng.uniform(-0.6, 0.6)
aspect_ratio = rng.uniform(9/16, 16/9)
speed_factor = rng.uniform(0.5, 2)
saturation_factor = rng.uniform(0.0, 3.0)
pad_color = (rng.integers(0, 255), rng.integers(0, 255), rng.integers(0, 255))
contrast_level = rng.uniform(-2.0, 2.0)
crop_left = rng.uniform(0, 0.3)
crop_top = rng.uniform(0, 0.3)
crop_right = rng.uniform(0.7, 1.0)
crop_bottom = rng.uniform(0.7, 1.0)
encoding_quality = rng.integers(17, 51)
fps = rng.integers(1, 30)
num_loops = rng.integers(1, 5)
overlay_size = rng.uniform(0.3, 0.8)
overlay_x = rng.uniform(0, 1 - overlay_size)
overlay_y = rng.uniform(0, 1 - overlay_size)
emoji_path = amv.helpers.select_random_emoji(rng=rng)
emoji_x = rng.uniform(0.1, 0.6)
emoji_y = rng.uniform(0.1, 0.6)
emoji_opacity = rng.uniform(0.5, 1.0)
emoji_size = rng.uniform(0.2, 0.6)
text_lines = rng.integers(4, 10)
text_fontsize = rng.uniform(0.05, 1/text_lines)
text_opacity = rng.uniform(0.5, 1.0)
pad_width = rng.uniform(0, 0.25)
pad_height = rng.uniform(0, 0.25)
pixelization_factor = rng.uniform(0.1, 0.5)
frames_cache = rng.integers(5, 30)
resize_width = rng.integers(320, 1920)
resize_height = rng.integers(320, 1920)
rotate_degrees = rng.choice([i for i in range(-30, 30, 5)])
scale_factor = rng.uniform(0.2, 0.8)
stack_2grid = rng.choice([0, 1])
stack_pad = rng.choice([True, False])
stack_preserve_aspect_ratio = rng.choice([True, False])
stack_4grid = rng.choice([0, 1, 2, 3])
transpose_direction = rng.choice([0, 1, 2, 3])

# Transforms API
augment_methods = [
    amv.AddNoise(level=noise_level, add_audio_noise=True),
    amv.AudioSwap(audio_path=audio_path, audio_offset=0),
    amv.BlendVideos(overlay_path=video2, opacity=blend_opacity,
        merge_audio=True),
    amv.Blur(sigma=blur_sigma),
    amv.Brightness(level=brightness_level),
    amv.ChangeAspectRatio(ratio=aspect_ratio),
    amv.ChangeVideoSpeed(factor=speed_factor),
    amv.ColorJitter(saturation_factor=saturation_factor),
    amv.Concat(other_video_paths=[video2, video3, video4],
        src_video_path_index=3, pad_color=pad_color),
    amv.Contrast(level=contrast_level),
    amv.Crop(left=crop_left, top=crop_top, right=crop_right,
        bottom=crop_bottom),
    amv.Emboss(),
    amv.EncodingQuality(quality=encoding_quality),
    amv.FPS(fps=fps),
    amv.Gradient(),
    amv.Grayscale(),
    amv.HFlip(),
    amv.InsertInBackground(background_path=video2, start=5, end=15,
        background_offset=10, pad_color=pad_color),
    amv.Loop(num_loops=num_loops),
    amv.Overlay(overlay_path=video2, overlay_size=overlay_size,
        x_factor=overlay_x, y_factor=overlay_y, merge_audio=False),
    amv.OverlayEmoji(emoji_path=emoji_path, x_factor=emoji_x,
        y_factor=emoji_y, opacity=emoji_opacity, emoji_size=emoji_size),
    amv.OverlayText(font=font_path, fontsize=text_fontsize,
        num_lines=text_lines, opacity=text_opacity),
    amv.Pad(w_factor=pad_width, h_factor=pad_height, color=pad_color),
    amv.Pixelization(ratio=pixelization_factor),
    amv.RandomFrames(num_frames=frames_cache),
    amv.RemoveAudio(),
    amv.Resize(width=resize_width, height=resize_height),
    amv.Rotate(degrees=rotate_degrees),
    amv.Scale(factor=scale_factor),
    amv.Transpose(direction=transpose_direction),
    amv.Trim(start=5, end=17),
    amv.VFlip(),
    amv.VStack(
        second_video_path=video2,
        merge_audio=True,
        target_grid=stack_2grid,
        preserve_aspect_ratio=stack_preserve_aspect_ratio,
        pad_second_video=stack_pad,
        pad_color=pad_color
    ),
    amv.HStack(
        second_video_path=video2,
        merge_audio=True,
        target_grid=stack_2grid,
        preserve_aspect_ratio=stack_preserve_aspect_ratio,
        pad_second_video=stack_pad,
        pad_color=pad_color
    ),
    amv.FStack(
        second_video_path=video2,
        third_video_path=video3,
        fourth_video_path=video4,
        merge_audio=True,
        target_grid=stack_4grid,
        preserve_aspect_ratio=stack_preserve_aspect_ratio,
        pad_video=stack_pad, pad_color=pad_color
    ),
]

for i in range(len(augment_methods)):
    meta_list = []
    output_path = f"output_transform/video_{str(i+1).zfill(2)}.mp4"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    augment_methods[i](video1, output_path, metadata=meta_list)

    with open(f"output_transform/video_{str(i+1).zfill(2)}.json", "w") as f:
        json.dump(meta_list, f)
        

# Functional API
meta_list = []
Path("output_functional").mkdir(parents=True, exist_ok=True)

amv.add_noise(video1, output_path="output_functional/video_01.mp4",
    level=noise_level, add_audio_noise=True, metadata=meta_list)
amv.audio_swap(video1, audio_path, output_path="output_functional/video_02.mp4",
    audio_offset=0, metadata=meta_list)
amv.blend_videos(video1, video2, output_path="output_functional/video_03.mp4",
    opacity=blend_opacity, merge_audio=True, metadata=meta_list)
amv.blur(video1, output_path="output_functional/video_04.mp4", sigma=blur_sigma,
    metadata=meta_list)
amv.brightness(video1, output_path="output_functional/video_05.mp4",
    level=brightness_level, metadata=meta_list)
amv.change_aspect_ratio(video1, output_path="output_functional/video_06.mp4",
    ratio=aspect_ratio, metadata=meta_list)
amv.change_video_speed(video1, output_path="output_functional/video_07.mp4",
    factor=speed_factor, metadata=meta_list)
amv.color_jitter(video1, output_path="output_functional/video_08.mp4",
    saturation_factor=saturation_factor, metadata=meta_list)
amv.concat([video1, video2, video3, video4],
    output_path="output_functional/video_09.mp4",
    src_video_path_index=1, pad_color=pad_color, metadata=meta_list)
amv.contrast(video1, output_path="output_functional/video_10.mp4",
    level=contrast_level, metadata=meta_list)
amv.crop(video1, output_path="output_functional/video_11.mp4", left=crop_left,
    top=crop_top, right=crop_right, bottom=crop_bottom, metadata=meta_list)
amv.emboss(video1, output_path="output_functional/video_12.mp4",
    metadata=meta_list)
amv.encoding_quality(video1, output_path="output_functional/video_13.mp4",
    quality=encoding_quality, metadata=meta_list)
amv.fps(video1, output_path="output_functional/video_14.mp4", fps=fps,
    metadata=meta_list)
amv.gradient(video1, output_path="output_functional/video_15.mp4",
    metadata=meta_list)
amv.grayscale(video1, output_path="output_functional/video_16.mp4",
    metadata=meta_list)
amv.hflip(video1, output_path="output_functional/video_17.mp4",
    metadata=meta_list)
amv.insert_in_background(video1, video2,
    output_path="output_functional/video_18.mp4", start=5, end=15,
    background_offset=10, pad_color=pad_color, metadata=meta_list)
amv.loop(video1, output_path="output_functional/video_19.mp4",
    num_loops=num_loops, metadata=meta_list)
amv.overlay(video1, video2, output_path="output_functional/video_20.mp4",
    overlay_size=overlay_size, x_factor=overlay_x, y_factor=overlay_y,
    merge_audio=True, metadata=meta_list)
amv.overlay_emoji(video1, output_path="output_functional/video_21.mp4",
    emoji_path=emoji_path, x_factor=emoji_x, y_factor=emoji_y, opacity=emoji_opacity,
    emoji_size=emoji_size, metadata=meta_list)
amv.overlay_text(video1, output_path="output_functional/video_22.mp4",
    font=font_path, fontsize=text_fontsize, num_lines=text_lines,
    opacity=text_opacity, metadata=meta_list)
amv.pad(video1, output_path="output_functional/video_23.mp4",
    w_factor=pad_width, h_factor=pad_height, color=pad_color, metadata=meta_list)
amv.pixelization(video1, output_path="output_functional/video_24.mp4",
    ratio=pixelization_factor, metadata=meta_list)
amv.random_frames(video1, output_path="output_functional/video_25.mp4",
    num_frames=frames_cache, metadata=meta_list)
amv.remove_audio(video1, output_path="output_functional/video_26.mp4",
    metadata=meta_list)
amv.resize(video1, output_path="output_functional/video_27.mp4",
    width=resize_width, height=resize_height, metadata=meta_list)
amv.rotate(video1, output_path="output_functional/video_28.mp4",
    degrees=rotate_degrees, metadata=meta_list)
amv.scale(video1, output_path="output_functional/video_29.mp4",
    factor=scale_factor, metadata=meta_list)
amv.transpose(video1, output_path="output_functional/video_30.mp4",
    direction=transpose_direction, metadata=meta_list)
amv.trim(video1, output_path="output_functional/video_31.mp4", start=5, end=17,
    metadata=meta_list)
amv.vflip(video1, output_path="output_functional/video_32.mp4",
    metadata=meta_list)
amv.vstack(video1, video2,
    output_path="output_functional/video_33.mp4",
    merge_audio=True,
    target_grid=stack_2grid,
    preserve_aspect_ratio=stack_preserve_aspect_ratio,
    pad_second_video=stack_pad,
    pad_color=pad_color,
    metadata=meta_list
)
amv.hstack(video1, video2,
    output_path="output_functional/video_34.mp4",
    merge_audio=True,
    target_grid=stack_2grid,
    preserve_aspect_ratio=stack_preserve_aspect_ratio,
    pad_second_video=stack_pad,
    pad_color=pad_color,
    metadata=meta_list
)
amv.fstack(video1, video2, video3, video4,
    output_path="output_functional/video_35.mp4",
    merge_audio=True,
    target_grid=stack_4grid,
    preserve_aspect_ratio=stack_preserve_aspect_ratio,
    pad_video=stack_pad,
    pad_color=pad_color,
    metadata=meta_list
)

with open(f"output_functional/metadata.json", "w") as f:
        json.dump(meta_list, f)
