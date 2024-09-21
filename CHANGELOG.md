# Changelog

## 0.1.0
### Added
- Added methods for creating transactions and retrieving user transaction reports

## 0.1.1
### Added
- Added basic project documentation
### Changed
- Changed structure: test structure now matches the application structure. The `main.py` file has been renamed to `service.py`.

## 0.2.0
### Added
- Added API
- Added integration tests
### Changed
- Changed structure: test structure now matches the application structure. The entry point is now `main.py`, and all business logic has been moved to the `service` folder.

## 0.2.1
### Added
- Added Dockerfile
- CI now includes a container build step and upload to Docker Hub

## 0.2.2
### Added
- Added Health check

## 0.3.0
### Added
- Added database

## 0.4.0
### Added
- Added manifests for Kubernetes deployment
- Added Helm charts

## 0.5.0
### Added
- Added tracing

## 0.6.0
### Added
- Added report storage in Redis
