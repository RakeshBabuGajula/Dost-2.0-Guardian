# UX Principles & Field Usability Architecture: DOST Guardian 2.0

**Document ID**: DOC-DES-02  
**Status**: Approved UX Guidelines  

---

## 1. Core Safety UX Principles

### 1.1 The 1-Second Emergency Comprehension Rule
When a worker's phone triggers an emergency alert while they are tightening a rail joint in noisy outdoor conditions, the visual and haptic feedback must allow the worker to digest 5 critical elements within **1.0 second**:
1. **Severity**: Flashing high-contrast Red background.
2. **Threat Type**: "TRAIN APPROACHING - DOWN LINE".
3. **Time Remaining**: Large monospace countdown ("01:15").
4. **Action Required**: "MOVE TO DESIGNATED SAFE ZONE".
5. **Acknowledgement Action**: Prominent green button `[ I'M SAFE ]`.

```text
+---------------------------------------------------+
|  [!] CRITICAL ALERT                               |
+---------------------------------------------------+
|                                                   |
|             TRAIN APPROACHING                     |
|                (DOWN LINE)                        |
|                                                   |
|                 01:15                             |
|          TIME TO AFFECTED ZONE                    |
|                                                   |
|     MOVE TO DESIGNATED SAFE REFUGE ZONE           |
|                                                   |
+---------------------------------------------------+
|                                                   |
|              [  I'M SAFE  ]                       |
|                                                   |
+---------------------------------------------------+
```

### 1.2 Zero Decorative Distraction During Emergencies
- When in `CRITICAL` or `EMERGENCY` state, all non-essential UI elements (navigation tab bars, settings menus, profile avatars, complex map overlays, historical charts) are **suppressed**.
- Ambient micro-animations are limited to functional pulses (e.g., countdown tick ring).

### 1.3 Progressive Information Density by Role
- **Track Worker**: Radically simple interface (1 screen during session, 1-tap ack).
- **Gang Supervisor**: Medium density (field tablet dashboard showing gang matrix and spatial radar map).
- **Control Room Operator**: High density (multi-monitor command display with live train tracking, block sections, and system health status).

---

## 2. Haptic & Acoustic UX Patterns

| Alert State | Visual State | Acoustic Pattern | Haptic Vibration Pattern |
| :--- | :--- | :--- | :--- |
| **SAFE** | Solid Emerald Green | Silent / Subtle ping on state change | Single 50ms click |
| **CAUTION** | Solid Amber Gold | Single 440Hz tone every 10s | Single 200ms pulse every 10s |
| **WARNING** | Solid Vibrant Orange | Double 880Hz chime every 3s | Double 300ms pulse every 3s |
| **CRITICAL** | Flashing Red | Continuous 1200Hz repeating siren (85 dB max) | Continuous pulse pattern (500ms ON / 100ms OFF) |
| **EMERGENCY** | Pulsing Crimson Overlay | High-urgency multi-tone emergency chime | Continuous intense vibration |

---

## 3. Offline & Low-Power UX Adaptation

- **Degraded Network UX**: When offline, top header displays an orange high-contrast badge `OFFLINE SAFETY MODE`. The map displays cached offline vector tiles.
- **Critical Battery UX**: At < 15% battery, interface automatically forces OLED True Black background (`#000000`) and reduces non-essential map rendering while maintaining 100% telemetry and alerting responsiveness.
