---
name: simple-code-logic
description: Use when writing or reviewing logic that feels complex, nested, or hard to follow — guard clauses, early returns, flat structure, and single-responsibility functions
---

# Simple Code Logic

## Overview

Complex logic is a bug waiting to happen. Flat is better than nested. Return early. Do one thing per function.

## Core Techniques

### Guard Clauses (Early Return)

Replace nested conditions with upfront exits.

```kotlin
// ❌ Nested
fun analyzeAudio(file: File?) {
    if (file != null) {
        if (file.exists()) {
            if (file.length() > 0) {
                doAnalysis(file)
            }
        }
    }
}

// ✅ Guard clauses
fun analyzeAudio(file: File?) {
    if (file == null) return
    if (!file.exists()) return
    if (file.length() == 0L) return
    doAnalysis(file)
}
```

### Single Responsibility

One function = one job. If you need "and" to describe it, split it.

```kotlin
// ❌ Does too much
fun recordAndUploadAndAnalyze(duration: Int) { ... }

// ✅ Each function does one thing
fun startRecording(duration: Int): File { ... }
fun uploadAudio(file: File): UploadResponse { ... }
fun analyzeUpload(response: UploadResponse): AnalysisResult { ... }
```

### Flatten with When / Sealed Classes

Avoid long if-else chains. Use `when` exhaustively on sealed types.

```kotlin
// ❌ If-else chain
if (state == "loading") showSpinner()
else if (state == "success") showResult(data)
else if (state == "error") showError(msg)
else hideAll()

// ✅ Exhaustive when
when (state) {
    is UiState.Loading -> showSpinner()
    is UiState.Success -> showResult(state.data)
    is UiState.Error -> showError(state.message)
    is UiState.Idle -> hideAll()
}
```

### Intention-Revealing Names Over Comments

```kotlin
// ❌ Comment explains what code does
val t = d / 60  // convert seconds to minutes

// ✅ Name explains intent
val durationMinutes = durationSeconds / 60

// ❌ Boolean flag magic
if (mode == 2) { ... }

// ✅ Named constant
if (mode == BEAT_STYLE_ROCK) { ... }
```

### Small Functions (< 20 lines as a guide)

If a function needs scrolling to read, extract part of it.

```kotlin
// ❌ One big function
fun processAnalysisResponse(response: Response) {
    // 50 lines of parsing, validation, mapping, and state updates
}

// ✅ Extracted steps
fun processAnalysisResponse(response: Response) {
    val dto = parseResponse(response)
    val result = validateAndMap(dto) ?: return showError("Invalid response")
    updateUiState(result)
}
```

### Avoid Boolean Parameters

Boolean args make call sites unreadable.

```kotlin
// ❌ What does `true` mean here?
playback(audioFile, true, false)

// ✅ Named parameters
playback(audioFile, withGuitar = true, withBeat = false)
```

## Quick Reference

| Smell | Fix |
|---|---|
| 3+ levels of nesting | Guard clauses / early return |
| Function does A and B | Split into two functions |
| Long if-else chain on type | `when` on sealed class |
| Unclear boolean arg | Named parameter or enum |
| Comment explains what | Rename to make it obvious |
| Function > 20 lines | Extract a helper |

## Common Mistakes

- Extracting tiny one-liner helpers that add indirection without clarity — only extract when the name adds meaning
- Over-applying early returns in `when` blocks that are already exhaustive
- Splitting functions so small that the call site reads like a table of contents — group related steps that always go together
