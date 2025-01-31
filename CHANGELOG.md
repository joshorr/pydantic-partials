# Changelog

## [2.0.1](https://github.com/joshorr/pydantic-partials/compare/v2.0.0...v2.0.1) (2025-01-31)


### Bug Fixes

* update/generate new docs after fixing/tweaking them. ([b307401](https://github.com/joshorr/pydantic-partials/commit/b30740103ed29aeb0abed0952a1917baefc32ad1))

## [2.0.0](https://github.com/joshorr/pydantic-partials/compare/v1.1.0...v2.0.0) (2025-01-30)


### ⚠ BREAKING CHANGES

* Support mypy + make `PartialModel` not auto-define partial fields, use `AutoPartialModel` instead if you want the old behavior.

### Features

* Support mypy + make `PartialModel` not auto-define partial fields, use `AutoPartialModel` instead if you want the old behavior. ([b6b669e](https://github.com/joshorr/pydantic-partials/commit/b6b669ee7159a28198d21ad7a3f54ee5ff521f52))


### Documentation

* adjust docs supported python version and make upgrade title more clear. ([2c39761](https://github.com/joshorr/pydantic-partials/commit/2c39761c449c67a8144c5e516302b316c6ef0ea6))

## [1.1.0](https://github.com/joshorr/pydantic-partials/compare/v1.0.8...v1.1.0) (2024-10-26)


### Features

* add way to exclude specific fields from auto partials. ([ceeb995](https://github.com/joshorr/pydantic-partials/commit/ceeb995d21ceb03447353272025f045f722dfbdf))

## [1.0.8](https://github.com/joshorr/pydantic-partials/compare/v1.0.7...v1.0.8) (2024-07-17)


### Bug Fixes

* ensure our validator only runs when the value type is `Missing`. ([07508c1](https://github.com/joshorr/pydantic-partials/commit/07508c1c134abda3fc82b4c177ca656197f5682d))

## [1.0.7](https://github.com/joshorr/pydantic-partials/compare/v1.0.6...v1.0.7) (2024-07-08)


### Bug Fixes

* we want to not change validated object to missing. ([9f754f7](https://github.com/joshorr/pydantic-partials/commit/9f754f753da1eae492fb289f5bce829a0186bb76))
* when setting values, Pydantic would ask this to serialize them if the type was not exactly what it expected. ([90555bd](https://github.com/joshorr/pydantic-partials/commit/90555bd1c8e1fe44abef896ee91686e87edf8aeb))

## [1.0.6](https://github.com/joshorr/pydantic-partials/compare/v1.0.5...v1.0.6) (2024-06-14)


### Bug Fixes

* require python &gt;=3.10, &lt;4 (from >=3.10,<3.11) ([2fb0959](https://github.com/joshorr/pydantic-partials/commit/2fb0959b0847da8aab67424dd674ddf41052e3a9))

## [1.0.5](https://github.com/joshorr/pydantic-partials/compare/v1.0.4...v1.0.5) (2024-06-11)


### Documentation

* clarifying readme/docs. ([d4d85ed](https://github.com/joshorr/pydantic-partials/commit/d4d85ed3af712319bfb782adabaf50b2e6f608e7))
* fix extra indent in code example in README.md. ([1745485](https://github.com/joshorr/pydantic-partials/commit/1745485fa7e6bfb9b3c070ebccff1289285b05cf))

## [1.0.4](https://github.com/joshorr/pydantic-partials/compare/v1.0.3...v1.0.4) (2024-06-10)


### Documentation

* added clarification around inheritance and default values. ([d09b8a0](https://github.com/joshorr/pydantic-partials/commit/d09b8a01f8a29d099687f9414f0640bf1d99d2c9))

## [1.0.3](https://github.com/joshorr/pydantic-partials/compare/v1.0.2...v1.0.3) (2024-06-10)


### Documentation

* clarified a point in readme/docs. ([6b9fbd0](https://github.com/joshorr/pydantic-partials/commit/6b9fbd0dc24257671fec3eb7124e53f551c6eb3b))
* fix incorrect mkdocs metadata. ([fe6779b](https://github.com/joshorr/pydantic-partials/commit/fe6779b08b8a65e811201e7c0712745e705745f8))

## [1.0.2](https://github.com/joshorr/pydantic-partials/compare/v1.0.1...v1.0.2) (2024-06-10)

### Documentation

* readme. ([ed0766c](https://github.com/joshorr/pydantic-partials/commit/ed0766c1b03074e51a6772ce5ee078a288083309))
* unneeded reference in docs. ([6d78d07](https://github.com/joshorr/pydantic-partials/commit/6d78d07846b16635cd1817df871e6df98a286d03))

## [1.0.1](https://github.com/joshorr/pydantic-partials/compare/v1.0.0...v1.0.1) (2024-06-10)


### Documentation

* generate docs issue. ([770cb7c](https://github.com/joshorr/pydantic-partials/commit/770cb7c0e5e8f3b2c6d82c479161b857296d9683))

## 1.0.0 (2024-06-10)


### Features

* 1.0.0 release ([0186934](https://github.com/joshorr/pydantic-partials/commit/01869347c27838e793f1aa481863fe3ea6aa85ed))
* final code adjustments for the initial release of pydantic-partials. ([7a680c3](https://github.com/joshorr/pydantic-partials/commit/7a680c354510e016ce2bfc70694454ba8ecb52c6))
* initial commit, want to refactor so committing stuff now. ([d0e9aa8](https://github.com/joshorr/pydantic-partials/commit/d0e9aa8ad05ff25fa5252cc4f41b0e4c767fb999))


### Bug Fixes

* version number. ([c13313b](https://github.com/joshorr/pydantic-partials/commit/c13313b21f702d43faf4c606e7e7b3186f4c820c))


### Documentation

* added basic docs to readme. ([a0eb544](https://github.com/joshorr/pydantic-partials/commit/a0eb544554d8351df07586ee7bc8ad393c761164))
* added/changed doc-comments. ([eb1eb7c](https://github.com/joshorr/pydantic-partials/commit/eb1eb7c507c1236a922d59a7dc7972f765615391))
