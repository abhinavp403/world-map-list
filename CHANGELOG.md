# Changelog

All notable changes to the World Map project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Interactive world map with D3.js visualization
- Country hover tooltips with flag, name, and capital
- Collapsible continent-grouped country list
- Web Speech API pronunciation support for countries and capitals
- Dark/light mode toggle with theme persistence
- Dual-view tabs (Map and List)
- Search and filter functionality for countries and capitals
- Collapse All / Expand All controls for continent sections
- Custom app icon (PNG, ICNS, ICO formats)
- Electron-based desktop application
- Build tools for macOS (DMG) and Windows (NSIS) installers
- Support for 197 countries across 6 continents
- Includes Greenland, French Guiana, and Falkland Islands

## [1.0.0] - 2026-05-01

### Initial Release
- Complete World Map desktop application with all core features
- Electron 41.3.0 framework
- D3.js 7.9.0 for visualization
- Natural Earth 110m geospatial data
- Professional app icon and branding
- Ready for macOS and Windows distribution

---

## Versioning

- **Major**: Breaking changes, significant feature additions
- **Minor**: New features, non-breaking changes
- **Patch**: Bug fixes, performance improvements

## Release Process

1. Create a tag: `git tag v1.0.0`
2. Push tag: `git push origin v1.0.0`
3. GitHub Actions automatically builds and releases installers
4. Edit the release on GitHub with release notes
