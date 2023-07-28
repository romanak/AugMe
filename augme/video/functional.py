from typing import Any, Dict, List, Optional, Union, Tuple
from augme.video import ffmpeg as af
from augme.video import helpers
import tempfile
import os
from math import ceil


def add_noise(
    video_path: str,
    output_path: Optional[str] = None,
    level: int = 100000,
    add_audio_noise: bool = False,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Adds noise to a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param level: apply noise to every byte for video and every bit for audio
        but don't drop any packets.

    @param add_audio_noise: add noise to video and audio together, rather than
        add noise only to video.

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    level = int(level)
    add_audio_noise = bool(add_audio_noise)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    noise_aug = af.VideoAugmenterByNoise(level, add_audio_noise)
    noise_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="add_noise", **func_kwargs
        )

    return output_path or video_path


def add_silent_audio(
    video_path: str,
    output_path: Optional[str] = None,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Adds silent audio to a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    silent_audio_aug = af.VideoAugmenterByAddingSilentAudio()
    silent_audio_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="add_noise", **func_kwargs
        )

    return output_path or video_path


def audio_swap(
    video_path: str,
    audio_path: str,
    output_path: Optional[str] = None,
    audio_offset: float = 0.0,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Swaps the video audio for the given audio starting from an offset

    @param video_path: the path to the video to be augmented

    @param audio_path: the path to the audio you'd like to swap with the
        video's audio

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param audio_offset: starting point in seconds such that an audio clip of offset to
        offset + video_duration is used in the audio swap. Default value is zero

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    audio_offset = float(audio_offset)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    audio_swap_aug = af.VideoAugmenterByAudioSwap(audio_path, audio_offset)
    audio_swap_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="audio_swap", **func_kwargs
        )

    return output_path or video_path


def blend_videos(
    video_path: str,
    overlay_path: str,
    output_path: Optional[str] = None,
    opacity: float = 0.5,
    merge_audio: bool = False,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Blends two videos together

    @param video_path: the path to the video to be augmented

    @param overlay_path: the path to the video that will be overlaid onto the
        background video

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param opacity: the lower the opacity, the more transparent the overlaid video

    @param merge_audio: merge the audio of the background and overlaid videos
        together

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    opacity = float(opacity)
    merge_audio = bool(merge_audio)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    blend_videos_aug = af.VideoAugmenterByBlending(
        overlay_path, opacity, merge_audio,
    )
    blend_videos_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="blend_videos", **func_kwargs
        )

    return output_path or video_path


def blur(
    video_path: str,
    output_path: Optional[str] = None,
    sigma: float = 1,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Blurs a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param sigma: horizontal sigma, standard deviation of Gaussian blur

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    sigma = float(sigma)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    blur_aug = af.VideoAugmenterByBlur(sigma)
    blur_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata, function_name="blur", **func_kwargs)

    return output_path or video_path


def brightness(
    video_path: str,
    output_path: Optional[str] = None,
    level: float = 0.15,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Brightens or darkens a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param level: the value must be a float value in range -1.0 to 1.0, where a
        negative value darkens and positive brightens

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    level = float(level)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    brightness_aug = af.VideoAugmenterByBrightness(level)
    brightness_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="brightness", **func_kwargs
        )

    return output_path or video_path


def change_aspect_ratio(
    video_path: str,
    output_path: Optional[str] = None,
    ratio: Optional[Union[float, str]] = 1.0,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Changes the sample aspect ratio attribute of the video, and resizes the
        video to reflect the new aspect ratio

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param ratio: aspect ratio of the new video, either as a float i.e. width/height,
        or as a string representing the ratio in the form "num:denom"

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    if isinstance(ratio, str):
        assert (len(ratio.split(":")) == 2), "Aspect ratio must be a valid string ratio"
        num, denom = [int(x) for x in str(self.ratio).split(":")]
        ratio = num / denom
    else:
        ratio = float(ratio)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    aspect_ratio_aug = af.VideoAugmenterByAspectRatio(ratio)
    aspect_ratio_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="change_aspect_ratio", **func_kwargs
        )

    return output_path or video_path


def change_video_speed(
    video_path: str,
    output_path: Optional[str] = None,
    factor: float = 1.0,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Changes the speed of the video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param factor: the factor by which to alter the speed of the video. A factor
        less than one will slow down the video, a factor equal to one won't alter
        the video, and a factor greater than one will speed up the video

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    factor = float(factor)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    speed_aug = af.VideoAugmenterBySpeed(factor)
    speed_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="change_video_speed", **func_kwargs
        )

    return output_path or video_path


def color_jitter(
    video_path: str,
    output_path: Optional[str] = None,
    brightness_factor: float = 0,
    contrast_factor: float = 1.0,
    saturation_factor: float = 1.0,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Color jitters the video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param brightness_factor: set the brightness expression. The value must be a
        float value in range -1.0 to 1.0. The default value is 0

    @param contrast_factor: set the contrast expression. The value must be a float
        value in range -1000.0 to 1000.0. The default value is 1

    @param saturation_factor: set the saturation expression. The value must be a float
        in range 0.0 to 3.0. The default value is 1

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    brightness_factor = float(brightness_factor)
    contrast_factor = float(contrast_factor)
    saturation_factor = float(saturation_factor)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    color_jitter_aug = af.VideoAugmenterByColorJitter(
        brightness_factor,
        contrast_factor,
        saturation_factor,
    )
    color_jitter_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="color_jitter", **func_kwargs
        )

    return output_path or video_path


def concat(
    video_paths: List[str],
    output_path: Optional[str] = None,
    src_video_path_index: int = 0,
    pad_color: Tuple[int, int, int] = helpers.DEFAULT_COLOR,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Concatenates videos together. Resizes all other videos to the size of the
    `source` video (video_paths[src_video_path_index]), preserving their aspect
    ratios

    @param video_paths: a list of paths to all the videos to be concatenated (in
        order)

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param src_video_path_index: for metadata purposes, this indicates which video in
        the list `video_paths` should be considered the `source` or original video

    @param pad_color: RGB color for padding of other videos after resizing

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    src_video_path_index = int(src_video_path_index)
    pad_color = tuple([int(e) for e in pad_color])

    func_kwargs = helpers.get_func_kwargs(
        metadata, locals(), video_paths[src_video_path_index]
    )

    video_paths_with_audio = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for path in video_paths:
            if helpers.get_audio_info(path):
                video_paths_with_audio.append(path)
            else:
                temp_path = os.path.join(tmpdir, f"{os.urandom(24).hex()}.mp4")
                add_silent_audio(path, temp_path)
                video_paths_with_audio.append(temp_path)

        concat_aug = af.VideoAugmenterByConcat(video_paths_with_audio, src_video_path_index, pad_color)
        concat_aug.add_augmenter(video_paths_with_audio[src_video_path_index], output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata,
            function_name="concat",
            video_path=video_paths[src_video_path_index],
            **func_kwargs,
        )

    return output_path or video_paths[src_video_path_index]


def contrast(
    video_path: str,
    output_path: Optional[str] = None,
    level: float = 1.0,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Alters the contrast of a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param level: the value must be a float value in range -1000.0 to 1000.0,
        where a negative value removes contrast and a positive value adds contrast

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    level = float(level)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    contrast_aug = af.VideoAugmenterByContrast(level)
    contrast_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="contrast", **func_kwargs)

    return output_path or video_path


def crop(
    video_path: str,
    output_path: Optional[str] = None,
    left: float = 0.25,
    top: float = 0.25,
    right: float = 0.75,
    bottom: float = 0.75,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Crops the video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param left: left positioning of the crop; between 0 and 1, relative to
        the video width

    @param top: top positioning of the crop; between 0 and 1, relative to
        the video height

    @param right: right positioning of the crop; between 0 and 1, relative to
        the video width

    @param bottom: bottom positioning of the crop; between 0 and 1, relative to
        the video height

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    left = float(left)
    top = float(top)
    right = float(right)
    bottom = float(bottom)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    crop_aug = af.VideoAugmenterByCrop(left, top, right, bottom)
    crop_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="crop", **func_kwargs)

    return output_path or video_path


def emboss(
    video_path: str,
    output_path: Optional[str] = None,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Emboss a video

    @param video_path: the path to the video to be augmented

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    emboss_aug = af.VideoAugmenterByEmboss()
    emboss_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="emboss", **func_kwargs
        )

    return output_path or video_path


def encoding_quality(
    video_path: str,
    output_path: Optional[str] = None,
    quality: int = 23,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Alters the encoding quality of a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param quality: CRF scale is 0–51, where 0 is lossless, 23 is the default,
        and 51 is worst quality possible. A lower value generally leads to higher
        quality, and a subjectively sane range is 17–28

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    quality = int(quality)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    encoding_aug = af.VideoAugmenterByQuality(quality)
    encoding_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="encoding_quality", **func_kwargs
        )

    return output_path or video_path


def fps(
    video_path: str,
    output_path: Optional[str] = None,
    fps: int = 15,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Alters the FPS of a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param fps: the desired output frame rate. Note that a FPS value greater than
        the original FPS of the video will result in an unaltered video

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    fps = int(fps)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    fps_aug = af.VideoAugmenterByFPSChange(fps)
    fps_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="fps", **func_kwargs)

    return output_path or video_path


def fstack(
    video_path: str,
    second_video_path: str,
    third_video_path: str,
    fourth_video_path: str,
    output_path: Optional[str] = None,
    merge_audio: bool = False,
    target_grid: int = 0,
    preserve_aspect_ratio: bool = False,
    pad_video: bool = False,
    pad_color: Tuple[int, int, int] = helpers.DEFAULT_COLOR,
    max_height: int = 1920,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Stack four videos in a grid

    @param video_path: the path to the video that will be stacked on top left

    @param second_video_path: the path to the video that will be stacked on
        the top right

    @param third_video_path: the path to the video that will be stacked on
        the bottom left

    @param fourth_video_path: the path to the video that will be stacked on
        the bottom right

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param merge_audio: if set to True, the audio all four videos will be merged

    @param target_grid: where to put the target video. 0 for top left (default),
        1 for top right, 2 for bottom left, 3 for bottom right.

    @param preserve_aspect_ratio: keep the original aspect ratio of the second
        video

    @param pad_video: if set to True, all other videos will be padded

    @param pad_color: RGB color for padding of other videos

    @param max_height: resize the output video preserving the aspect ratio if
        the height exceeds the specified value

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    merge_audio = bool(merge_audio)
    target_grid = int(target_grid)
    preserve_aspect_ratio = bool(preserve_aspect_ratio)
    pad_video = bool(pad_video)
    pad_color = tuple([int(e) for e in pad_color])
    max_height = int(max_height)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        video_info = helpers.get_video_info(video_path)
        if (video_info["width"] % 2 == 1) or (video_info["height"] % 2 == 1):
            temp_path = os.path.join(tmpdir, f"{os.urandom(24).hex()}.mp4")
            pad(video_path, temp_path, w_factor=0, h_factor=0)
        else:
            temp_path = None

        fstack_aug = af.VideoAugmenterByFStack(
            second_video_path, third_video_path, fourth_video_path, merge_audio,
            target_grid, preserve_aspect_ratio, pad_video, pad_color, max_height
        )
        fstack_aug.add_augmenter(temp_path or video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="fstack", **func_kwargs)

    return output_path or video_path


def gradient(
    video_path: str,
    output_path: Optional[str] = None,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Overlay a horizontal gradient onto a video

    @param video_path: the path to the video to be augmented

    @param overlay_path: the path to the video that will be overlaid onto the
        background video

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    gradient_aug = af.VideoAugmenterByGradient()
    gradient_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="gradient", **func_kwargs
        )

    return output_path or video_path


def grayscale(
    video_path: str,
    output_path: Optional[str] = None,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Changes a video to be grayscale

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    grayscale_aug = af.VideoAugmenterByGrayscale()
    grayscale_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="grayscale", **func_kwargs
        )

    return output_path or video_path


def hflip(
    video_path: str,
    output_path: Optional[str] = None,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Horizontally flips a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    hflip_aug = af.VideoAugmenterByHFlip()
    hflip_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="hflip", **func_kwargs)

    return output_path or video_path


def hstack(
    video_path: str,
    second_video_path: str,
    output_path: Optional[str] = None,
    merge_audio: bool = False,
    target_grid: int = 0,
    preserve_aspect_ratio: bool = False,
    pad_second_video: bool = False,
    pad_color: Tuple[int, int, int] = helpers.DEFAULT_COLOR,
    max_width: int = 1920,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Horizontally stacks two videos

    @param video_path: the path to the video that will be stacked on the left

    @param second_video_path: the path to the video that will be stacked on
        the right

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param merge_audio: if set to True, the audio from both videos will be merged

    @param target_grid: where to put the target video. 0 for left (default),
        1 for right.

    @param preserve_aspect_ratio: keep the original aspect ratio of the second
        video

    @param pad_second_video: if set to True, the second video will be padded

    @param pad_color: RGB color for padding of second video

    @param max_width: resize the output video preserving the aspect ratio if
        the width exceeds the specified value

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    merge_audio = bool(merge_audio)
    target_grid = int(target_grid)
    preserve_aspect_ratio = bool(preserve_aspect_ratio)
    pad_second_video = bool(pad_second_video)
    pad_color = tuple([int(e) for e in pad_color])
    max_width = int(max_width)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        video_info = helpers.get_video_info(video_path)
        if (video_info["width"] % 2 == 1) or (video_info["height"] % 2 == 1):
            temp_path = os.path.join(tmpdir, f"{os.urandom(24).hex()}.mp4")
            pad(video_path, temp_path, w_factor=0, h_factor=0)
        else:
            temp_path = None

        hstack_aug = af.VideoAugmenterByHStack(
            second_video_path, merge_audio, target_grid, preserve_aspect_ratio,
            pad_second_video, pad_color, max_width
        )
        hstack_aug.add_augmenter(temp_path or video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="hstack", **func_kwargs)

    return output_path or video_path

def insert_in_background(
    video_path: str,
    background_path: str,
    output_path: Optional[str] = None,
    start: Optional[float] = None,
    end: Optional[float] = None,
    background_offset: Optional[float] = None,
    pad_color: Tuple[int, int, int] = helpers.DEFAULT_COLOR,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Insert the video in the middle of the background video

    @param video_path: the path to the video to be augmented

    @param background_path: the path to the video in which to insert the main
        video

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param start: start time in seconds from which the video will be inserted into
        the background video

    @param end: end time in seconds until which the video will be inserted into
        the background video

    @param background_offset: the point measured in seconds in the background
        video from which the main video starts to play

    @param pad_color: the pad color of the video after resizing it to the size
        of the background video, preserving the aspect ratio

    @param metadata: if set to be a list, metadata about the function execution including
        its name, the source & dest duration, fps, etc. will be appended to the inputted
        list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    if start is not None:
        start = float(start)
    if end is not None:
        end = float(end)
    background_offset = float(background_offset)
    pad_color = tuple([int(e) for e in pad_color])

    helpers.validate_path(background_path)
    assert background_offset >= 0, "Background offset cannot be a negative number"
    helpers.validate_rgb_color(pad_color)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    video_info = helpers.get_video_info(video_path)
    background_info = helpers.get_video_info(background_path)

    if background_offset > background_info["duration"]:
        background_offset = background_info["duration"]

    video_paths = []
    with tempfile.TemporaryDirectory() as tmpdir:
        if background_offset > 0:
            before_path = os.path.join(tmpdir, f"{os.urandom(24).hex()}.mp4")
            trim(background_path, before_path, end=background_offset)
            video_paths.append(before_path)
        
        insert_path = os.path.join(tmpdir, f"{os.urandom(24).hex()}.mp4")
        trim(video_path, insert_path, start=start, end=end)
        video_paths.append(insert_path)

        if background_offset < background_info["duration"]:
            after_path = os.path.join(tmpdir, f"{os.urandom(24).hex()}.mp4")
            trim(background_path, after_path, start=background_offset)
            video_paths.append(after_path)

        src_video_path_index = 0
        concat(video_paths, output_path or video_path, src_video_path_index, pad_color)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata,
            function_name="insert_in_background",
            **func_kwargs,
        )

    return output_path or video_path


def loop(
    video_path: str,
    output_path: Optional[str] = None,
    num_loops: int = 0,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Loops a video `num_loops` times

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param num_loops: the number of times to loop the video. 0 means that the video
        will play once (i.e. no loops)

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    num_loops = int(num_loops)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    loop_aug = af.VideoAugmenterByLoops(num_loops)
    loop_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="loop", **func_kwargs)

    return output_path or video_path


def overlay(
    video_path: str,
    overlay_path: str,
    output_path: Optional[str] = None,
    overlay_size: Optional[float] = None,
    x_factor: float = 0.0,
    y_factor: float = 0.0,
    merge_audio: bool = False,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Overlays media onto the video at position (width * x_factor, height * y_factor)

    @param video_path: the path to the video to be augmented

    @param overlay_path: the path to the media (image or video) that will be
        overlaid onto the video

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param overlay_size: size of the overlaid media with respect to the background
        video. If set to None, the original size of the overlaid media is used

    @param x_factor: specifies where the left side of the overlaid media should be
        placed, relative to the video width

    @param y_factor: specifies where the top side of the overlaid media should be
        placed, relative to the video height

    @param merge_audio: if set to True and the media type is a video, the
        audio of the overlaid video will be merged with the main/background
        video's audio

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    if overlay_size is not None:
        overlay_size = float(overlay_size)
    x_factor = float(x_factor)
    y_factor = float(y_factor)
    merge_audio = bool(merge_audio)

    helpers.validate_path(video_path)
    helpers.validate_path(overlay_path)
    
    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        video_info = helpers.get_video_info(video_path)
        overlay_video_info = helpers.get_video_info(overlay_path)
        overlay_resize_path = None

        if overlay_size is not None:
            assert 0 < overlay_size <= 1, "overlay_size must be a value in the range (0, 1]"
            num_loops = ceil(video_info['duration'] / overlay_video_info['duration'])
            overlay_loop_path = os.path.join(tmpdir, f"{os.urandom(24).hex()}.mp4")
            loop(overlay_path, overlay_loop_path, num_loops)

            if overlay_video_info["height"] > overlay_video_info["width"]:
                overlay_h = int(video_info["height"] * overlay_size)
                overlay_w = None
            else:
                overlay_h = None
                overlay_w = int(video_info["width"] * overlay_size)

            overlay_resize_path = os.path.join(tmpdir, f"{os.urandom(24).hex()}.mp4")
            resize(overlay_loop_path, overlay_resize_path, overlay_w, overlay_h)

        overlay_aug = af.VideoAugmenterByOverlay(
            overlay_resize_path or overlay_path, x_factor, y_factor, merge_audio
        )
        overlay_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="overlay", **func_kwargs)

    return output_path or video_path


def overlay_emoji(
    video_path: str,
    output_path: Optional[str] = None,
    emoji_path: str = helpers.EMOJI_PATH,
    x_factor: float = 0.4,
    y_factor: float = 0.4,
    opacity: float = 1.0,
    emoji_size: float = 0.15,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Overlays an emoji onto each frame of a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param emoji_path: path to the emoji image

    @param x_factor: specifies where the left side of the emoji should be placed,
        relative to the video width

    @param y_factor: specifies where the top side of the emoji should be placed,
        relative to the video height

    @param opacity: opacity of the emoji image

    @param emoji_size: emoji size relative to the height of the video frame

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    x_factor = float(x_factor)
    y_factor = float(y_factor)
    opacity = float(opacity)
    emoji_size = float(emoji_size)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    helpers.validate_path(video_path)
    helpers.validate_path(emoji_path)
    video_info = helpers.get_video_info(video_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        emoji_output_path = os.path.join(tmpdir, f"{os.urandom(24).hex()}.png")

        helpers.resize_image(
            emoji_path,
            output_path=emoji_output_path,
            height=int(emoji_size * video_info["height"]),
            width=int(emoji_size * video_info["height"]),
        )
        helpers.opacity_image(emoji_output_path, output_path=emoji_output_path, level=opacity)

        overlay(
            video_path,
            emoji_output_path,
            output_path,
            x_factor=x_factor,
            y_factor=y_factor,
        )

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="overlay_emoji", **func_kwargs
        )

    return output_path or video_path


def overlay_text(
    video_path: str,
    output_path: Optional[str] = None,
    font: Optional[str] = helpers.FONT_PATH,
    fontsize: float = 0.1,
    num_lines: int = 10,
    opacity: float = 0.5,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Overlay random text onto a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param font: a path to the font file. Note that font file is associated with
        different sets of characters (western, cyrillic, chinese, etc.)

    @param fontsize: the font size given as a factor of the video height

    @param num_lines: number of text lines

    @param opacity: the lower the opacity, the more transparent the overlaid video

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    fontsize = float(fontsize)
    num_lines = int(num_lines)
    opacity = float(opacity)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    text_aug = af.VideoAugmenterByText(
        font, fontsize, num_lines, opacity,
    )
    text_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="overlay_text", **func_kwargs
        )

    return output_path or video_path


def pad(
    video_path: str,
    output_path: Optional[str] = None,
    w_factor: float = 0.25,
    h_factor: float = 0.25,
    color: Tuple[int, int, int] = helpers.DEFAULT_COLOR,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Pads the video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param w_factor: pad right and left with w_factor * frame width

    @param h_factor: pad bottom and top with h_factor * frame height

    @param color: RGB color of the padded margin

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    w_factor = float(w_factor)
    h_factor = float(h_factor)
    color = tuple([int(e) for e in color])

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    pad_aug = af.VideoAugmenterByPadding(w_factor, h_factor, color)
    pad_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="pad", **func_kwargs)

    return output_path or video_path


def pixelization(
    video_path: str,
    output_path: Optional[str] = None,
    ratio: float = 1.0,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Pixelizes the video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param ratio: smaller values result in a more pixelated video, 1.0 indicates
        no change, and any value above one doesn't have a noticeable effect

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    ratio = float(ratio)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    assert ratio > 0, "Expected 'ratio' to be a positive number"
    video_info = helpers.get_video_info(video_path)
    width, height = video_info["width"], video_info["height"]

    output_path = output_path or video_path
    resize(video_path, output_path, width * ratio, height * ratio)
    resize(output_path, output_path, width, height)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="pixelization", **func_kwargs
        )

    return output_path or video_path


def random_frames(
    video_path: str,
    output_path: Optional[str] = None,
    num_frames: Optional[int] = 30,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Flush video frames from internal cache of frames into a random order. No
        frame is discarded.

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param num_frames: the number of frames in the cache from which to
        take the next frame randomly without replacement for video output

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    num_frames = int(num_frames)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    random_frames_aug = af.VideoAugmenterByRandomFrames(
        num_frames,
    )
    random_frames_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="random_frames", **func_kwargs
        )

    return output_path or video_path


def remove_audio(
    video_path: str,
    output_path: Optional[str] = None,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Removes the audio stream from a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    remove_audio_aug = af.VideoAugmenterByRemovingAudio()
    remove_audio_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(
            metadata=metadata, function_name="remove_audio", **func_kwargs
        )

    return output_path or video_path


def resize(
    video_path: str,
    output_path: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Resizes a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param width: the width in which the video should be resized to. If None,
        the original video width will be used

    @param height: the height in which the video should be resized to. If None,
        the original video height will be used

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    if width is not None:
        width = int(width)
    if height is not None:
        height = int(height)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    resize_aug = af.VideoAugmenterByResize(width, height)
    resize_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="resize", **func_kwargs)

    return output_path or video_path


def rotate(
    video_path: str,
    output_path: Optional[str] = None,
    degrees: float = 15.0,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Rotates a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param degrees: expression for the angle by which to rotate the input video
        clockwise, expressed in degrees (supports negative values as well)

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    degrees = float(degrees)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    rotate_aug = af.VideoAugmenterByRotation(degrees)
    rotate_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="rotate", **func_kwargs)

    return output_path or video_path


def scale(
    video_path: str,
    output_path: Optional[str] = None,
    factor: float = 0.5,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Alters the resolution of a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param factor: the ratio by which the video should be downscaled or upscaled

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    factor = float(factor)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    scale_aug = af.VideoAugmenterByResolution(factor)
    scale_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="scale", **func_kwargs)

    return output_path or video_path


def transpose(
    video_path: str,
    output_path: Optional[str] = None,
    direction: int = 0,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Transpose rows with columns in the input video and optionally flip it.

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param direction: specify transposition direction and flip:
        0 - Rotate by 90 degrees counter-clockwise and flip vertically (default)
        1 - Rotate by 90 degrees clockwise
        2 - Rotate by 90 degrees counter-clockwise
        3 - Rotate by 90 degrees clockwise and flip vertically

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    direction = int(direction)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    transpose_aug = af.VideoAugmenterByTransposition(direction)
    transpose_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="transpose", **func_kwargs)

    return output_path or video_path


def trim(
    video_path: str,
    output_path: Optional[str] = None,
    start: Optional[float] = None,
    end: Optional[float] = None,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Trims the video using the specified start and end parameters

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param start: starting point in seconds of when the trimmed video should start.
        If None, start will be 0

    @param end: ending point in seconds of when the trimmed video should end.
        If None, the end will be the duration of the video

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    if start is not None:
        start = float(start)
    if end is not None:
        end = float(end)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    trim_aug = af.VideoAugmenterByTrim(start=start, end=end)
    trim_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="trim", **func_kwargs)

    return output_path or video_path


def vflip(
    video_path: str,
    output_path: Optional[str] = None,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Vertically flips a video

    @param video_path: the path to the video to be augmented

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    vflip_aug = af.VideoAugmenterByVFlip()
    vflip_aug.add_augmenter(video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="vflip", **func_kwargs)

    return output_path or video_path


def vstack(
    video_path: str,
    second_video_path: str,
    output_path: Optional[str] = None,
    merge_audio: bool = False,
    target_grid: int = 0,
    preserve_aspect_ratio: bool = False,
    pad_second_video: bool = False,
    pad_color: Tuple[int, int, int] = helpers.DEFAULT_COLOR,
    max_height: int = 1920,
    metadata: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Vertically stacks two videos

    @param video_path: the path to the video that will be stacked on top

    @param second_video_path: the path to the video that will be stacked on
        the bottom

    @param output_path: the path in which the resulting video will be stored.
        If not passed in, the original video file will be overwritten

    @param merge_audio: if set to True, the audio from both videos will be merged

    @param target_grid: where to put the target video. 0 for top (default),
        1 for bottom.

    @param preserve_aspect_ratio: keep the original aspect ratio of the second
        video

    @param pad_second_video: if set to True, the second video will be padded

    @param pad_color: RGB color for padding of second video

    @param max_height: resize the output video preserving the aspect ratio if
        the height exceeds the specified value

    @param metadata: if set to be a list, metadata about the function execution
        including its name, the source & dest duration, fps, etc. will be appended
        to the inputted list. If set to None, no metadata will be appended or returned

    @returns: the path to the augmented video
    """
    merge_audio = bool(merge_audio)
    target_grid = int(target_grid)
    preserve_aspect_ratio = bool(preserve_aspect_ratio)
    pad_second_video = bool(pad_second_video)
    pad_color = tuple([int(e) for e in pad_color])
    max_height = int(max_height)

    func_kwargs = helpers.get_func_kwargs(metadata, locals(), video_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        video_info = helpers.get_video_info(video_path)
        if (video_info["width"] % 2 == 1) or (video_info["height"] % 2 == 1):
            temp_path = os.path.join(tmpdir, f"{os.urandom(24).hex()}.mp4")
            pad(video_path, temp_path, w_factor=0, h_factor=0)
        else:
            temp_path = None

        vstack_aug = af.VideoAugmenterByVStack(
            second_video_path, merge_audio, target_grid, preserve_aspect_ratio,
            pad_second_video, pad_color, max_height
        )
        vstack_aug.add_augmenter(temp_path or video_path, output_path)

    if metadata is not None:
        helpers.get_metadata(metadata=metadata, function_name="vstack", **func_kwargs)

    return output_path or video_path
