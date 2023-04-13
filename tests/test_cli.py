"""test rio-faux."""

import math
import os

import numpy
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


def test_tags():
    """Check if tags are forwarded."""
    runner = CliRunner()
    src_path = os.path.join(os.path.dirname(__file__), "fixtures", "cog_band_tags.tif")
    with runner.isolated_filesystem():
        result = runner.invoke(faux, [src_path, "output.tif"])
        assert not result.exception
        assert result.exit_code == 0
        with rasterio.open(src_path) as src_dst, rasterio.open(
            "output.tif"
        ) as faux_dst:
            assert src_dst.profile == faux_dst.profile
            assert not src_dst.tags() == faux_dst.tags()
            assert not src_dst.descriptions == faux_dst.descriptions
            assert not src_dst.tags(0) == faux_dst.tags(0)

        result = runner.invoke(
            faux,
            [src_path, "output.tif", "--forward-band-tags", "--forward-dataset-tags"],
        )
        assert not result.exception
        assert result.exit_code == 0
        with rasterio.open(src_path) as src_dst, rasterio.open(
            "output.tif"
        ) as faux_dst:
            assert src_dst.profile == faux_dst.profile
            assert src_dst.tags() == faux_dst.tags()
            assert src_dst.descriptions == faux_dst.descriptions
            assert src_dst.tags(0) == faux_dst.tags(0)


def test_alpha():
    """Check if alpha forwarded."""
    runner = CliRunner()
    src_path = os.path.join(os.path.dirname(__file__), "fixtures", "image_rgba.tif")
    with runner.isolated_filesystem():
        result = runner.invoke(faux, [src_path, "output.tif"])
        assert not result.exception
        assert result.exit_code == 0
        with rasterio.open(src_path) as src_dst, rasterio.open(
            "output.tif"
        ) as faux_dst:
            assert src_dst.colorinterp == faux_dst.colorinterp
            numpy.testing.assert_array_equal(
                src_dst.read(indexes=4), faux_dst.read(indexes=4)
            )


def test_mask():
    """Check if alpha forwarded."""
    runner = CliRunner()
    src_path = os.path.join(os.path.dirname(__file__), "fixtures", "image_rgb_mask.tif")
    with runner.isolated_filesystem():
        result = runner.invoke(faux, [src_path, "output.tif"])
        assert not result.exception
        assert result.exit_code == 0
        with rasterio.open(src_path) as src_dst, rasterio.open(
            "output.tif"
        ) as faux_dst:
            assert src_dst.mask_flag_enums == faux_dst.mask_flag_enums
            numpy.testing.assert_array_equal(
                src_dst.dataset_mask(), faux_dst.dataset_mask()
            )


def test_value():
    """Check value."""
    runner = CliRunner()
    src_path = os.path.join(os.path.dirname(__file__), "fixtures", "image_rgba.tif")
    with runner.isolated_filesystem():
        result = runner.invoke(faux, [src_path, "output.tif", "--value", 100])
        assert not result.exception
        assert result.exit_code == 0
        with rasterio.open(src_path) as src_dst, rasterio.open(
            "output.tif"
        ) as faux_dst:

            assert numpy.unique(faux_dst.read(indexes=1)) == 100

        # Check that we are casting values to the output data type
        result = runner.invoke(faux, [src_path, "output.tif", "--value", 100.3])
        assert not result.exception
        assert result.exit_code == 0
        with rasterio.open(src_path) as src_dst, rasterio.open(
            "output.tif"
        ) as faux_dst:

            assert numpy.unique(faux_dst.read(indexes=1)) == 100
