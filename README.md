# 🌍 World Map

An interactive desktop application for exploring the world with detailed country information, pronunciation guides, and dark/light mode support.

![License](https://img.shields.io/badge/license-ISC-blue)
![Node Version](https://img.shields.io/badge/node-%3E%3D16.0.0-brightgreen)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey)

## ✨ Features

- **Interactive World Map** – Explore 197 countries on a zoomable, pannable map using D3.js and Natural Earth data
- **Country Tooltips** – Hover over any country to see the flag emoji, country name, and capital
- **Collapsible Country List** – Browse countries organized by continent with a clean tabular interface
- **Pronunciation Guide** – Click the microphone button next to any country or capital to hear the correct English pronunciation (Web Speech API)
- **Dual View Tabs** – Toggle between Map and List views seamlessly
- **Search & Filter** – Quickly find countries by name or capital
- **Collapse/Expand Controls** – Batch expand or collapse all continent sections with a single click
- **Dark/Light Mode** – Switch between dark and light themes with a theme toggle button below the title
- **Desktop Distribution** – Built with Electron for easy distribution on macOS and Windows
- **Custom App Icon** – Professional globe icon generated with Python

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | Electron | 41.3.0 |
| **Visualization** | D3.js | 7.9.0 |
| **Geospatial** | TopoJSON Client, World Atlas | 3.1.0, 2.0.2 |
| **Packaging** | Electron Builder | 26.8.1 |
| **Build Tools** | Python/Pillow, Bash | 3.7+, sh |
| **Speech** | Web Speech API | Native |

## 📦 Quick Start

### Prerequisites
- Node.js v16 or higher
- Python 3.7+ (optional, only for icon regeneration)
- Pillow library: `pip install Pillow` (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/abhinavp403/world-map-list.git
cd world-map-list

# Install dependencies
npm install

# Start the app
npm start
```

## 🚀 Building for Distribution

### Macros & Windows Installers

```bash
# Build for both macOS and Windows
npm run dist

# Build for specific platform
npm run dist:mac   # macOS DMG for arm64 & x64
npm run dist:win   # Windows NSIS installer
```

Installers will be created in `dist/` directory.

### Icon Generation (Optional)

```bash
# Regenerate app icon from scratch
npm run icon
```

This creates:
- `build/icon-1024.png` – Base icon (1024×1024)
- `build/icon.icns` – macOS icon bundle
- `build/icon.ico` – Windows icon with multiple sizes

## 📁 Project Structure

```
world-map-list/
├── 📄 index.html               # Complete app UI (HTML + CSS + JS)
├── 🔧 main.js                  # Electron main process
├── 📋 package.json             # Dependencies & scripts
├── 🎨 README.md                # This file
├── 🚫 .gitignore
├── 🎯 build/                   # Generated app icons
│   ├── icon-1024.png          # Source icon
│   ├── icon-512.png           # Preview size
│   ├── icon.icns              # macOS icon
│   ├── icon.ico               # Windows icon
│   └── icon.iconset/          # macOS icon components
├── 📦 vendor/                  # Runtime dependencies (bundled)
│   ├── d3.min.js              # 273 KB
│   ├── topojson-client.min.js # 7 KB
│   └── countries-110m.json    # 105 KB
├── 🛠️ scripts/                # Build tools
│   ├── create_icon.py         # Python Pillow icon generator
│   ├── create_ico.py          # Windows ICO binary encoder
│   └── build_icons.sh         # macOS icon pipeline
└── 📦 node_modules/           # Dev dependencies (not bundled)
```

## 🎯 Supported Regions

**197 Countries & Territories across 6 Continents:**

- 🌍 **Africa** – 54 countries
- 🌏 **Asia** – 49 countries  
- 🌎 **Europe** – 45 countries
- 🌎 **North America** – 23 countries (includes Greenland)
- 🌎 **South America** – 13 countries (includes Falkland Islands, French Guiana)
- 🌏 **Oceania** – 13 countries

## 🎮 How to Use

### Map View
1. Use **mouse wheel** or **trackpad** to zoom in/out
2. **Click and drag** to pan around the map
3. **Hover over countries** to see tooltips with flag, name, and capital
4. **Click** on the "List" tab to switch to list view

### List View
1. **Click continent headers** to expand/collapse country lists
2. **Use "Collapse All" / "Expand All"** buttons for batch control
3. **Type in search box** to filter by country or capital name
4. **Click microphone icons** to hear pronunciation
5. **Click** on the "Map" tab to return to the map

### Theme
- Click the **sun/moon icon** below the "World Map" title to toggle between dark and light modes
- Theme preference is automatically saved

## 🔧 Development

### File Organization
- **Single-file app**: All HTML, CSS, and JavaScript in `index.html` for simplicity
- **Vendor bundling**: Only minified runtime files + data in `vendor/` (~385 KB total)
- **Dev dependencies**: d3, topojson-client, world-atlas kept in `node_modules` but not bundled

### Key Implementation Details

**Context Isolation & Security**
```javascript
// Electron configured with:
contextIsolation: true      // Protect main process
webSecurity: false          // Allow file:// fetch for vendor files
```

**CSS Theme System**
- All colors as CSS custom properties (`--var-name`)
- Single `[data-theme]` attribute controls dark/light mode
- No JavaScript DOM manipulation needed for theme switching

**Responsive Map**
- D3 Natural Earth 1 projection
- Debounced resize handler (150ms) for smooth reflow
- SVG `viewBox` for scaling across devices

**Data Structures**
- 197-country array with `{id, iso2, name, capital, continent}`
- Country ID matches Natural Earth 110m topojson geometry IDs
- Continent-organized grouping for list view

## 📊 Data Sources

- **Boundaries**: Natural Earth 1:110m via [world-atlas](https://github.com/topojson/world-atlas)
- **Countries**: Curated dataset with ISO 3166 codes, capitals, and continental grouping
- **Flags**: Unicode emoji via [country-code-emoji](https://en.wikipedia.org/wiki/Regional_indicator_symbol)

## 🎨 Customization

### Change App Icon
Edit `scripts/create_icon.py` to customize colors, add text, or change the design:
```python
# Example: Change ocean color from (7, 20, 58) to RGB(your_color)
```
Then run `npm run icon`.

### Change Theme Colors
Edit CSS variables in `index.html`:
```css
:root {
  --ocean-fill: #070a12;
  --text-1: #e0e0e0;
  /* ... more colors ... */
}

[data-theme="light"] {
  --ocean-fill: #e3f2fd;
  /* ... light mode overrides ... */
}
```

### Add More Countries
Edit the `COUNTRIES` array in `index.html`. Format:
```javascript
{id: 999, iso2: 'XX', name: 'Country Name', capital: 'Capital', continent: 'Continent'}
```

## ⚙️ Available Scripts

```bash
npm start              # Launch app in development
npm run dist           # Build for macOS and Windows
npm run dist:mac       # Build macOS DMG only
npm run dist:win       # Build Windows NSIS only
npm run icon           # Regenerate app icons
```

## 🐛 Troubleshooting

**Map doesn't appear after theme toggle from list view**
- This was a bug where `initMap()` was called with `display: none` on the map container, resulting in zero dimensions
- Fix: Theme toggle no longer calls `initMap()` since CSS variables propagate automatically

**Multiple maps stacked on top of each other**
- Caused by `initMap()` being called multiple times without clearing the SVG first
- Fix: `initMap()` now clears the SVG at the start and is debounced on resize

**Gridlines don't move when zooming**
- Graticule was appended to root SVG instead of the zoom-transformed group
- Fix: Graticule now appended to the `g` element that receives zoom transforms

## 📝 License

ISC License – See [LICENSE](./package.json) section for details

## 👨‍💻 Author

**Abhinav P**  
📧 abhinavp403@gmail.com  
🔗 [GitHub](https://github.com/abhinavp403)

---

## 🙏 Acknowledgments

- [D3.js](https://d3js.org/) – Data visualization
- [Natural Earth](https://www.naturalearthdata.com/) – Geospatial data
- [Electron](https://www.electronjs.org/) – Desktop apps with web technologies
- [Electron Builder](https://www.electron.build/) – Simple packaging

---

**Made with ❤️ for geography enthusiasts and data visualization lovers.**