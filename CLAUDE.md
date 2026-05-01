# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Product: TuneMate

An Android app that helps beginner/hobby musicians identify the **musical key**, **BPM**, and **chord suggestions** of a song by recording or humming it, then replaying the input with guitar strumming and beat accompaniment.

---

## Architecture

Two-component system:

### Android App (Kotlin)
- Records audio via microphone
- Uploads audio to backend for analysis
- Displays results (key, BPM, chords)
- Handles local playback with generated guitar + beat overlay

### Backend API (Python / FastAPI)
- Receives audio uploads
- Runs audio analysis: key detection + BPM detection
- Returns structured JSON result
- Audio processing library: **librosa** (MVP) → **Essentia** (later phases)

### Data Flow
```
Record audio → Upload to backend → Analyze key + BPM → Return results → Local playback generation
```

---

## MVP Scope

**Included:**
- Audio recording with waveform animation
- Duration selection (1 min / 2 min / 5 min, default 1 min)
- Key detection (e.g., C Major, A Minor)
- BPM detection
- Chord suggestion based on key (e.g., G Major → G–C–D–Em)
- Playback with guitar strumming + beat/rhythm
- Retry flow (re-record and re-analyze, no history)

**Excluded from MVP:**
- AI/ML-based key detection
- Social features
- Export/save/share

---

## Key Technical Constraints

- Analysis must complete in **< 10 seconds**
- Android minimum: **API 26 (Android 8.0)**
- Must handle moderate background noise
- Target ≥ 80% perceived accuracy on key detection

---

## Screens & Navigation

1. **Home** — Record button + duration selector
2. **Recording** — Waveform animation + timer
3. **Results** — Key, BPM, chord display
4. **Playback** — Play/Pause, beat style toggle, guitar toggle

---

## Core Features Reference

| Feature | Implementation |
|---|---|
| Key detection | Backend (librosa pitch analysis) |
| BPM detection | Backend (librosa beat tracking) |
| Chord suggestions | Computed from detected key (rule-based in MVP) |
| Guitar + beat playback | Generated locally on device |
| Waveform animation | Android AudioRecord + UI rendering |

---

## Release Phases

- **Phase 1 (MVP):** Core detection + playback
- **Phase 2:** Improved accuracy, additional beat styles
- **Phase 3:** AI-based enhancements, advanced chord progressions, multi-instrument support

---

## Skills to Use

Invoke these skills before the corresponding tasks:

| Task | Skill |
|---|---|
| Designing a new feature or screen | `superpowers:brainstorming` |
| Planning a multi-step implementation | `superpowers:writing-plans` |
| Executing an implementation plan | `superpowers:executing-plans` |
| Implementing any feature or bugfix | `superpowers:test-driven-development` |
| Debugging unexpected behavior or test failures | `superpowers:systematic-debugging` |
| Before claiming a task is complete | `superpowers:verification-before-completion` |
| After completing a feature, before merging | `superpowers:requesting-code-review` |
| Phase 3: integrating Claude/AI for key detection | `claude-api` |
| Writing Kotlin / Android code | `kotlin` |
| Structuring layers (use cases, repositories, ViewModels) | `clean-architecture` |
| Simplifying complex or nested logic | `simple-code-logic` |
| Writing Python backend code (librosa, async, models) | `python` |
| Building Flask API endpoints and file uploads | `flask` |
