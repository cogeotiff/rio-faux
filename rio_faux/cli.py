"""rio-faux."""

import os
import warnings

import click
import rasterio
from rasterio.enums import ColorInterp, MaskFlags
from rasterio.enums import Resampling as ResamplingEnums
from rasterio.io import MemoryFile
from rasterio.rio import options
from rasterio.shutil import copy


def has_mask_band(src_dst):
    """Check for mask band in source."""
    if any(
        [
            (MaskFlags.per_dataset in flags and MaskFlags.alpha not in flags)
            for flags in src_dst.mask_flag_enums
        ]
    ):
        return True
    return False


@click.command()
@options.file_in_arg
@options.file_out_arg
@click.option(
    "--forward-band-tags",
    default=False,
    is_flag=True,
    help="Forward band tags to output bands.",
)
@options.creation_options
@click.option(
    "--config",
    "config",
    metavar="NAME=VALUE",
    multiple=True,
    callback=options._cb_key_val,
    help="GDAL configuration options.",
)
def faux(
    input,
    output,
    forward_band_tags,
    creation_options,
    config,
):
    """Create Fake copy."""
    # Check if the dataset has overviews
    with rasterio.open(input) as src_dst:
        ovr = src_dst.overviews(1)

    # Get Overview Blocksize
    overview_blocksize = 512
    if ovr:
        with rasterio.open(input, OVERVIEW_LEVEL=0) as src_dst:
            overview_blocksize = src_dst.profile.get("blockxsize", overview_blocksize)

    config.update(
        dict(
            GDAL_NUM_THREADS="ALL_CPUS",
            GDAL_TIFF_INTERNAL_MASK=os.environ.get("GDAL_TIFF_INTERNAL_MASK", True),
            GDAL_TIFF_OVR_BLOCKSIZE=str(overview_blocksize),
        )
    )
    with rasterio.Env(**config):
        with rasterio.open(input) as src_dst:
            meta = src_dst.meta
            with MemoryFile() as m:
                with m.open(**meta) as tmp_dst:
                    if tmp_dst.colorinterp[0] is ColorInterp.palette:
                        try:
                            tmp_dst.write_colormap(1, src_dst.colormap(1))
                        except ValueError:
                            warnings.warn(
                                "Dataset has `Palette` color interpretation"
                                " but is missing colormap information"
                            )

                    if has_mask_band(src_dst):
                        tmp_dst.write_mask(src_dst.dataset_mask())

                    tags = src_dst.tags()

                    overview_resampling = tags.get(
                        "OVR_RESAMPLING_ALG", "nearest"
                    ).lower()
                    if ovr:
                        tmp_dst.build_overviews(
                            ovr, ResamplingEnums[overview_resampling]
                        )

                    indexes = src_dst.indexes
                    for i, b in enumerate(indexes):
                        tmp_dst.set_band_description(i + 1, src_dst.descriptions[b - 1])

                        if forward_band_tags:
                            tmp_dst.update_tags(i + 1, **src_dst.tags(b))

                    tmp_dst.update_tags(**tags)
                    tmp_dst._set_all_scales([src_dst.scales[b - 1] for b in indexes])
                    tmp_dst._set_all_offsets([src_dst.offsets[b - 1] for b in indexes])

                    output_profile = src_dst.profile
                    output_profile.update(
                        dict(BIGTIFF=os.environ.get("BIGTIFF", "IF_SAFER"))
                    )
                    if creation_options:
                        output_profile.update(creation_options)

                    keys = [
                        "dtype",
                        "nodata",
                        "width",
                        "height",
                        "count",
                        "crs",
                        "transform",
                    ]
                    for key in keys:
                        output_profile.pop(key, None)

                    copy(tmp_dst, output, copy_src_overviews=True, **output_profile)
