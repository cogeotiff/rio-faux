"""test rio-faux."""

import math
import os

import pytest
import rasterio
from click.testing import CliRunner

from rio_faux.cli import faux

files = [
    "cog_band_tags.tif",
    "image_171px.tif",
    "image_2000px.tif",
    "image_51px.tif",
    "image_colormap.tif",
    "image_float.tif",
    "image_geos.tif",
    "image_missing_nodata.tif",
    "image_nan.tif",
    "image_nocolormap.tif",
    "image_nodata.tif",
    "image_north.tif",
    "image_rgb.tif",
    "image_rgb_mask.tif",
    "image_rgba.tif",
    "image_tags.tif",
    "image_web.tif",
    "image_web_z5_z11.tif",
    "image_with_offsets.tif",
    "slc.tif",
]


@pytest.mark.parametrize("input", files)
def test_cli(input):
    """Check equivalence of profiles"""
    runner = CliRunner()
    src_path = os.path.join(os.path.dirname(__file__), "fixtures", input)
    with runner.isolated_filesystem():
        result = runner.invoke(faux, [src_path, "output.tif"])
        assert not result.exception
        assert result.exit_code == 0
        with rasterio.open(src_path) as src_dst, rasterio.open(
            "output.tif"
        ) as faux_dst:
            src_p = src_dst.profile
            faux_p = faux_dst.profile

            if src_p["nodata"] is not None and not math.isfinite(src_p["nodata"]):
                assert not math.isfinite(faux_p["nodata"])
                src_p.pop("nodata")
                faux_p.pop("nodata")

            assert src_p == faux_p
