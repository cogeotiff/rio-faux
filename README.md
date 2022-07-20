# rio-faux

<p align="center">
  <img src="https://user-images.githubusercontent.com/10407788/180094114-91b8bb55-022b-4a9d-a1bd-7414037f76fa.png" style="max-width: 800px;" alt="rio-tiler"></a>
</p>
<p align="center">
  <em>Now you can share your dataset!</em>
</p>

<p align="center">
  <a href="https://github.com/cogeotiff/rio-faux/actions?query=workflow%3ACI" target="_blank">
      <img src="https://github.com/cogeotiff/rio-faux/workflows/CI/badge.svg" alt="Test">
  </a>
  <a href="https://codecov.io/gh/cogeotiff/rio-faux" target="_blank">
      <img src="https://codecov.io/gh/cogeotiff/rio-faux/branch/master/graph/badge.svg" alt="Coverage">
  </a>
  <a href="https://pypi.org/project/rio-faux" target="_blank">
      <img src="https://img.shields.io/pypi/v/rio-faux?color=%2334D058&label=pypi%20package" alt="Package version">
  </a>
  <a href="https://pypistats.org/packages/rio-faux" target="_blank">
      <img src="https://img.shields.io/pypi/dm/rio-faux.svg" alt="Downloads">
  </a>
  <a href="https://github.com/cogeotiff/rio-faux/blob/master/LICENSE" target="_blank">
      <img src="https://img.shields.io/github/license/cogeotiff/rio-faux.svg" alt="Downloads">
  </a>
</p>

---

**Documentation**: <a href="https://cogeotiff.github.io/rio-faux/" target="_blank">https://cogeotiff.github.io/rio-faux/</a>

**Source Code**: <a href="https://github.com/cogeotiff/rio-faux" target="_blank">https://github.com/cogeotiff/rio-faux</a>

---

Create a copy of your dataset without copying the data.

## Install

```bash
$ pip install -U pip
$ pip install rio-faux
```

Or install from source:

```bash
$ pip install -U pip
$ pip install git+https://github.com/cogeotiff/rio-faux.git
```

## Usage

```
$ rio faux --help
Usage: rio faux [OPTIONS] INPUT OUTPUT

  Create Fake copy.

Options:
  --forward-band-tags         Forward band tags to output bands.
  --co, --profile NAME=VALUE  Driver specific creation options. See the documentation for the selected output driver for more information.
  --config NAME=VALUE         GDAL configuration options.
  --help                      Show this message and exit.
```

```
$ rio faux my_image_i_cant_share.tif public.tif
```

## Contribution & Development

See [CONTRIBUTING.md](https://github.com/cogeotiff/rio-faux/blob/master/CONTRIBUTING.md)

## Changes

See [CHANGES.md](https://github.com/cogeotiff/rio-faux/blob/master/CHANGES.md).

## License

See [LICENSE](https://github.com/cogeotiff/rio-faux/blob/master/LICENSE)

