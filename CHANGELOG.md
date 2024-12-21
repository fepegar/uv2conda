# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## Unreleased

<small>[Compare with latest](https://github.com/fepegar/uv2conda/compare/v1.0.1...HEAD)</small>

### Added

- Add default recipe to justfile ([aca5cac](https://github.com/fepegar/uv2conda/commit/aca5caca853a76d53ac72fc3ccd1f26d4d27ff5f) by Fernando Pérez-García).
- Add stubs for PyYAML ([89b55e0](https://github.com/fepegar/uv2conda/commit/89b55e03e2a167b65b5688cc6490724e548a86d0) by Fernando Pérez-García).
- Add recipe to push ([ffc36dd](https://github.com/fepegar/uv2conda/commit/ffc36dd4a21ddd7de59251851a408c3921bd5d6c) by Fernando Pérez-García).

### Fixed

- Fix typing errors ([61b58a7](https://github.com/fepegar/uv2conda/commit/61b58a7fbc1bda14e24ad7882eccbdf89b5c4b3b) by Fernando Pérez-García).

### Removed

- Remove uv-args option ([ad74639](https://github.com/fepegar/uv2conda/commit/ad7463979f341e5441dead02d6c04c2ecf87a4b1) by Fernando Pérez-García).
- Remove loguru and add --quiet ([11a8efb](https://github.com/fepegar/uv2conda/commit/11a8efb7c2730897b9250b655aa7aedb7ea7ff1e) by Fernando Pérez-García).

<!-- insertion marker -->
## [v1.0.1](https://github.com/fepegar/uv2conda/releases/tag/v1.0.1) - 2024-12-15

<small>[Compare with v1.0.0](https://github.com/fepegar/uv2conda/compare/v1.0.0...v1.0.1)</small>

### Added

- Add some tests ([212a9e7](https://github.com/fepegar/uv2conda/commit/212a9e70d4df0432a23052b62df1c7d38e2da3d9) by Fernando Pérez-García).

### Fixed

- Fix README ([719882f](https://github.com/fepegar/uv2conda/commit/719882f46eda033ac4ca800a0227c10fba2a76e6) by Fernando Pérez-García).

## [v1.0.0](https://github.com/fepegar/uv2conda/releases/tag/v1.0.0) - 2024-12-15

<small>[Compare with v0.1.7](https://github.com/fepegar/uv2conda/compare/v0.1.7...v1.0.0)</small>

### Removed

- Remove option to return YAML string ([60bc338](https://github.com/fepegar/uv2conda/commit/60bc33830e7718eefbc6ffa08678da20fa722f62) by Fernando Pérez-García).

## [v0.1.7](https://github.com/fepegar/uv2conda/releases/tag/v0.1.7) - 2024-12-12

<small>[Compare with v0.1.6](https://github.com/fepegar/uv2conda/compare/v0.1.6...v0.1.7)</small>

## [v0.1.6](https://github.com/fepegar/uv2conda/releases/tag/v0.1.6) - 2024-12-07

<small>[Compare with v0.1.5](https://github.com/fepegar/uv2conda/compare/v0.1.5...v0.1.6)</small>

### Added

- Add better logging ([990ea81](https://github.com/fepegar/uv2conda/commit/990ea815cbdd73a13decc4ccc5977ca919072504) by Fernando Pérez-García).
- Add some unit tests ([359c5b6](https://github.com/fepegar/uv2conda/commit/359c5b6c5d5329bda268dcd9f4d6844e40ff70ba) by Fernando Pérez-García).
- Add unit testing recipe ([31b3e01](https://github.com/fepegar/uv2conda/commit/31b3e0109a951ef4dc67b5e41aafe17f6d3a3771) by Fernando Pérez-García).
- Add help for version option ([c3c4939](https://github.com/fepegar/uv2conda/commit/c3c49397b794cfac85b48dbcd999c8a5e6856744) by Fernando Pérez-García).
- Add just recipe ([bf0e478](https://github.com/fepegar/uv2conda/commit/bf0e478929408ff0e8a757fe4294aac211ad5b31) by Fernando Pérez-García).
- Add --version parameter ([dc4ac75](https://github.com/fepegar/uv2conda/commit/dc4ac7517270f8dc118458dcd640c1b03629c586) by Fernando Pérez-García).

### Changed

- Change how  version is defined in __init__ ([d6cb4ca](https://github.com/fepegar/uv2conda/commit/d6cb4cadfba06f3c356428acdadc8dce4af4b03d) by Fernando Pérez-García).

### Removed

- Remove *args and **kwargs from function definitions ([83d9a2f](https://github.com/fepegar/uv2conda/commit/83d9a2f53c6899ea19322b56ede0de6bb3e26643) by Fernando Pérez-García).

## [v0.1.5](https://github.com/fepegar/uv2conda/releases/tag/v0.1.5) - 2024-12-06

<small>[Compare with v0.1.4](https://github.com/fepegar/uv2conda/compare/v0.1.4...v0.1.5)</small>

### Added

- Add recipe to update changelog ([ca6ad00](https://github.com/fepegar/uv2conda/commit/ca6ad007a8252f9ab9c1c8fe6912929496dd7a8e) by Fernando Pérez-García).

### Fixed

- Fix logging when conda path is None ([7e2a3a6](https://github.com/fepegar/uv2conda/commit/7e2a3a62ab597ab1f644cfee5866a0a94620e07c) by Fernando Pérez-García).

### Removed

- Remove unused import ([1d1f1dc](https://github.com/fepegar/uv2conda/commit/1d1f1dc129ba095b3453eee6e83dcbc820b2fbcc) by Fernando Pérez-García).

## [v0.1.4](https://github.com/fepegar/uv2conda/releases/tag/v0.1.4) - 2024-12-06

<small>[Compare with v0.1.3](https://github.com/fepegar/uv2conda/compare/v0.1.3...v0.1.4)</small>

## [v0.1.3](https://github.com/fepegar/uv2conda/releases/tag/v0.1.3) - 2024-12-06

<small>[Compare with v0.1.2](https://github.com/fepegar/uv2conda/compare/v0.1.2...v0.1.3)</small>

### Added

- Add support to write a requirements file ([d0903a8](https://github.com/fepegar/uv2conda/commit/d0903a80d37540aeb3caa2cae8821363d5acf3f7) by Fernando Pérez-García).
- Add target to release new version ([1fa13b7](https://github.com/fepegar/uv2conda/commit/1fa13b7ce8ba133a9e4d05e24b676c4c85d14e36) by Fernando Pérez-García).
- Add changelog ([ae06e14](https://github.com/fepegar/uv2conda/commit/ae06e14a55adc8308dc1bedca7a11c0555a2c25a) by Fernando Pérez-García).
- Add justfile ([959ab43](https://github.com/fepegar/uv2conda/commit/959ab439251c653805d0a0ac8b4a94dc668ee592) by Fernando Pérez-García).

### Removed

- Remove recipe ([2ad245c](https://github.com/fepegar/uv2conda/commit/2ad245c2e76d2e1c3ec50593eb43468c3e022fd8) by Fernando Pérez-García).

## [v0.1.2](https://github.com/fepegar/uv2conda/releases/tag/v0.1.2) - 2024-12-02

<small>[Compare with v0.1.1](https://github.com/fepegar/uv2conda/compare/v0.1.1...v0.1.2)</small>

### Added

- Add CHANGELOG ([d78a5d8](https://github.com/fepegar/uv2conda/commit/d78a5d8545c0a04871e8fb159648426417638235) by Fernando Pérez-García).

### Removed

- Remove background when printing the YAML contents ([8b6ca77](https://github.com/fepegar/uv2conda/commit/8b6ca771f38e4e1ddd953b406b8f0d757363f5ca) by Fernando Pérez-García).
- Remove line wrap in output YAML ([6f9a8df](https://github.com/fepegar/uv2conda/commit/6f9a8df0c36776a5d10eb336f3d2f0729b71490c) by Fernando Pérez-García).

## [v0.1.1](https://github.com/fepegar/uv2conda/releases/tag/v0.1.1) - 2024-11-28

<small>[Compare with first commit](https://github.com/fepegar/uv2conda/compare/a3ae5ef5fc577bf80ccc325fb8127d644d140939...v0.1.1)</small>

### Added

- Add bump-my-version config ([006a4fc](https://github.com/fepegar/uv2conda/commit/006a4fc634b7f6da387174531085fb442595c57f) by Fernando Pérez-García).
- Add version to __init__ ([068629e](https://github.com/fepegar/uv2conda/commit/068629effbfa630edcca2dc878f9e2db298226a2) by Fernando Pérez-García).
- Add project URLs ([ddbcc33](https://github.com/fepegar/uv2conda/commit/ddbcc33eed6e48e312cc5c256d44a987ac87daee) by Fernando Pérez-García).
- Add pre-commit (#2) ([d5d2fa6](https://github.com/fepegar/uv2conda/commit/d5d2fa6e2730fb0005fcb31ab70123e774c40192) by Fernando Pérez-García).
- Add some imports in __init__ ([4a1a012](https://github.com/fepegar/uv2conda/commit/4a1a012de08bc0557486b54369c98076b76a4638) by Fernando Pérez-García).
- Add support to pass extra args to uv ([c6e743e](https://github.com/fepegar/uv2conda/commit/c6e743ea3e798de7214149c2c4dc714d25f880e7) by Fernando Pérez-García).

