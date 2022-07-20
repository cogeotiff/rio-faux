# rio-faux

<p align="center">
  <em>Create empty image from a model.</em>
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

## Contribution & Development

See [CONTRIBUTING.md](https://github.com/cogeotiff/rio-faux/blob/master/CONTRIBUTING.md)

## Changes

See [CHANGES.md](https://github.com/cogeotiff/rio-faux/blob/master/CHANGES.md).

## License

See [LICENSE](https://github.com/cogeotiff/rio-faux/blob/master/LICENSE)

