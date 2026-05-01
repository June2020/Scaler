---
name: kotlin
description: Use when writing Kotlin code for Android — coroutines, Flow, sealed classes, data classes, null safety, ViewModel, and AudioRecord/MediaPlayer for audio apps
---

# Kotlin

## Overview

Kotlin-first Android development. Prefer idiomatic Kotlin over Java-style patterns. Use coroutines + Flow for async, sealed classes for state, data classes for models.

## Core Patterns

### Async with Coroutines

```kotlin
// ViewModel scope for UI-tied work
viewModelScope.launch {
    _uiState.value = UiState.Loading
    val result = repository.analyzeAudio(file)
    _uiState.value = when (result) {
        is Result.Success -> UiState.Success(result.data)
        is Result.Error -> UiState.Error(result.message)
    }
}

// IO scope for backend calls
withContext(Dispatchers.IO) {
    apiService.uploadAudio(audioFile)
}
```

### Sealed Classes for State

```kotlin
sealed class UiState<out T> {
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}

sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val message: String, val cause: Throwable? = null) : Result<Nothing>()
}
```

### StateFlow for UI State

```kotlin
private val _uiState = MutableStateFlow<UiState<AnalysisResult>>(UiState.Loading)
val uiState: StateFlow<UiState<AnalysisResult>> = _uiState.asStateFlow()

// Collect in Fragment/Activity
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { state ->
            when (state) {
                is UiState.Loading -> showLoading()
                is UiState.Success -> showResults(state.data)
                is UiState.Error -> showError(state.message)
            }
        }
    }
}
```

### Data Classes for API Models

```kotlin
data class AnalysisResult(
    val key: String,       // e.g. "G Major"
    val bpm: Int,
    val chords: List<String>
)

data class AudioUploadRequest(
    val durationSeconds: Int,
    val audioBase64: String
)
```

### Null Safety

```kotlin
// Prefer let/also/run over !!
audioFile?.let { file ->
    analyzeAudio(file)
} ?: showError("No recording found")

// Elvis for defaults
val duration = selectedDuration ?: DEFAULT_DURATION_SECONDS
```

### Extension Functions

```kotlin
fun Int.toBpmLabel(): String = "$this BPM"
fun String.toKeyDisplay(): String = "Key: $this"
fun File.toBase64(): String = Base64.encodeToString(readBytes(), Base64.DEFAULT)
```

## Audio-Specific APIs

### Recording (AudioRecord)

```kotlin
val recorder = AudioRecord(
    MediaRecorder.AudioSource.MIC,
    SAMPLE_RATE,           // 44100
    AudioFormat.CHANNEL_IN_MONO,
    AudioFormat.ENCODING_PCM_16BIT,
    AudioRecord.getMinBufferSize(SAMPLE_RATE, CHANNEL_IN_MONO, ENCODING_PCM_16BIT)
)
```

### Playback (MediaPlayer)

```kotlin
val player = MediaPlayer().apply {
    setDataSource(context, audioUri)
    setOnPreparedListener { start() }
    setOnCompletionListener { onPlaybackComplete() }
    prepareAsync()
}
// Always release: player.release()
```

## Quick Reference

| Pattern | Use For |
|---|---|
| `viewModelScope.launch` | UI-triggered async work |
| `Dispatchers.IO` | Network/file operations |
| `StateFlow` | UI state observable |
| `sealed class` | Result/state types |
| `data class` | API request/response models |
| `?.let` | Null-safe operations |
| `?:` (Elvis) | Default values |

## Common Mistakes

- Using `!!` (null bang) — use `?.let` or `?:` instead
- Launching coroutines in `GlobalScope` — use `viewModelScope` or `lifecycleScope`
- Blocking the main thread — wrap IO in `withContext(Dispatchers.IO)`
- Not releasing `AudioRecord`/`MediaPlayer` — always call `release()` in `onDestroy`
- Mutable state exposed from ViewModel — back with private `MutableStateFlow`, expose as `StateFlow`
