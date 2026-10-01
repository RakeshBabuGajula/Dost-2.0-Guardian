# Design System Specification: DOST Guardian 2.0

**Document ID**: DOC-DES-01  
**Design Philosophy**: *Railway Command Centre + Modern Field Safety Technology*  
**Status**: Approved Design System Specification  

---

## 1. Visual Identity & Color Tokens

The visual palette is engineered for high outdoor contrast, dark-mode efficiency, and instant cognitive state recognition.

### 1.1 Core Palette Tokens
- **Background Base (`--color-bg-base`)**: `#090D16` (Deep Railway Navy / Slate Dark)
- **Background Panel (`--color-bg-panel`)**: `#121826` (Elevated Command Card)
- **Background Surface (`--color-bg-surface`)**: `#1A2336` (Interactive Container)
- **Border Default (`--color-border-default`)**: `#2A364F` (Subtle Grid Line)
- **Text Primary (`--color-text-primary`)**: `#F8FAFC` (Pure High-Contrast White)
- **Text Secondary (`--color-text-secondary`)**: `#94A3B8` (Muted Label Slate)
- **Accent Primary (`--color-accent-primary`)**: `#0284C7` (Electric Railway Blue)
- **Accent Secondary (`--color-accent-secondary`)**: `#06B6D4` (Telemetry Cyan)

### 1.2 System Safety State Tokens

| Safety State | Token Variable | Hex Code | Purpose & Context |
| :--- | :--- | :--- | :--- |
| **SAFE** | `--color-safety-safe` | `#10B981` (Emerald Green) | Normal operations, track clear, active protection. |
| **CAUTION** | `--color-safety-caution` | `#F59E0B` (Amber Gold) | Train in adjacent section, elevated monitoring. |
| **WARNING** | `--color-safety-warning` | `#F97316` (Vibrant Orange) | Train approaching work zone boundary, preparation time. |
| **CRITICAL** | `--color-safety-critical` | `#EF4444` (Signal Red) | Imminent threat, immediate evacuation required. |
| **EMERGENCY** | `--color-safety-emergency` | `#DC2626` (Flashing Crimson) | Unacknowledged breach, active emergency escalation. |
| **AI / ANALYTICS** | `--color-accent-ai` | `#A855F7` (Deep Purple) | Non-safety AI trend insights, analytical overlays only. |

---

## 2. Typography Hierarchy

Using modern, highly legible sans-serif typefaces (e.g., Inter, Roboto, or Outfit) with tabular figures for numbers to prevent layout jitter during live countdowns.

- **Primary Font**: `Inter, system-ui, sans-serif`
- **Monospace Font**: `JetBrains Mono, tabular-nums, monospace` (used for coordinates, TTD countdowns, telemetry timestamps)

| Level | Size | Weight | Line Height | Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Display (Emergency Countdown)** | `64px` / `4.0rem` | Bold (700) | `1.0` | Critical Time-to-Danger timer (`01:15`) |
| **Heading 1 (Screen Title)** | `32px` / `2.0rem` | SemiBold (600) | `1.2` | Mobile Alert State Header (`CRITICAL`) |
| **Heading 2 (Panel Header)** | `24px` / `1.5rem` | SemiBold (600) | `1.3` | Command Center Panel Titles |
| **Subheading** | `18px` / `1.125rem` | Medium (500) | `1.4` | Card titles, field label groups |
| **Body Primary** | `16px` / `1.0rem` | Regular (400) | `1.5` | Standard UI text, list items |
| **Body Small / Captions** | `13px` / `0.8125rem` | Regular (400) | `1.4` | Telemetry metadata, device status labels |

---

## 3. UI Component Specifications

### 3.1 Mobile Emergency Alert Screen Component
- **Layout**: Single-card layout, zero scrollbar, full viewlock.
- **Top Badge**: Pulsing state banner (`CRITICAL`).
- **Center Hero**: `01:15` Tabular Mono Countdown Timer with dynamic outline glow.
- **Action Button**: `[ I'M SAFE ]` button spanning full screen width ($h = 72\text{px}$), min font size $22\text{px}$ bold, background `#10B981` (Green), $12\text{px}$ border-radius.

### 3.2 Command Center Panel Cards
- **Container**: Slate Dark background (`#121826`), subtle $1\text{px}$ border (`#2A364F`), $8\text{px}$ corner radius, gentle inset drop shadow (`0 4px 20px rgba(0,0,0,0.4)`).
- **Glassmorphism Rule**: Subtle background blur (`backdrop-filter: blur(12px)`) allowed ONLY on floating map controls and overlay headers. Never use glassmorphism behind critical text.

### 3.3 Status Badges
- Pill-shaped badges ($24\text{px}$ height, $12\text{px}$ border-radius) with $8\text{px}$ status indicator dot.
- Green dot = Connected / Safe; Amber dot = Caution; Red dot = Unacknowledged / Critical; Gray dot = Offline.

---

## 4. Accessibility & Outdoor Usability Standards

1. **High Sunlight Contrast**: Minimum 7:1 contrast ratio across all text elements against backgrounds (WCAG AAA).
2. **Gloved Touch Targets**: All interactive buttons on mobile app must measure at least $64 \times 64\text{ dp}$.
3. **Multi-Sensory Alerts**: Every alert state change combines visual color changes, haptic vibration pulses (patterns: short pulse for caution, triple pulse for warning, continuous vibration for critical), and localized audio tones.
4. **No Color-Only Information**: Color indicators are always paired with explicit text labels (e.g., `CRITICAL` text + Red color + Warning icon).
