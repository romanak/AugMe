from copy import deepcopy
from typing import Any, Dict, List, Optional
from augme.video import helpers


def get_func_kwargs(
    metadata: Optional[List[Dict[str, Any]]],
    local_kwargs: Dict[str, Any],
    video_path: str,
    **kwargs,
) -> Dict[str, Any]:
    if metadata is None:
        return {}
    func_kwargs = deepcopy(local_kwargs)
    func_kwargs.pop("metadata")
    video_info = helpers.get_video_info(video_path)
    func_kwargs.update(
        {
            "src_video_info": video_info,
            **kwargs,
        }
    )
    return func_kwargs

def get_metadata(
    metadata: Optional[List[Dict[str, Any]]],
    function_name: str,
    video_path: str,
    output_path: Optional[str],
    src_video_info: Dict[str, Any],
    **kwargs,
) -> None:
    if metadata is None:
        return

    assert isinstance(
        metadata, list
    ), "Expected 'metadata' to be set to None or of type list"

    # Output video may not be provided
    output_path = output_path or video_path
    dst_video_info = helpers.get_video_info(output_path)

    # Json can't represent tuples, so they're represented as lists, which should
    # be equivalent to tuples. So let's avoid tuples in the metadata by
    # converting any tuples to lists here.
    kwargs_types_fixed = dict(
        (k, list(v)) if isinstance(v, tuple) else (k, v) for k, v in kwargs.items()
    )

    metadata.append(
        {
            "name": function_name,
            "src_duration": src_video_info["duration"],
            "dst_duration": dst_video_info["duration"],
            "src_fps": src_video_info["r_frame_rate"],
            "dst_fps": dst_video_info["r_frame_rate"],
            "src_width": src_video_info["width"],
            "src_height": src_video_info["height"],
            "dst_width": dst_video_info["width"],
            "dst_height": dst_video_info["height"],
            **kwargs_types_fixed,
        }
    )

