---
name: clean-architecture
description: Use when structuring Android or backend code into layers — defining where use cases, repositories, entities, and data sources belong, and how dependencies should flow
---

# Clean Architecture

## Overview

Three layers with a strict dependency rule: **outer layers depend on inner layers, never the reverse.**

```
Presentation  →  Domain  ←  Data
(ViewModel)      (UseCases,   (Repositories impl,
                  Entities,    Remote/Local sources)
                  Repository
                  interfaces)
```

Domain knows nothing about Android, Retrofit, Room, or any framework.

## Layer Responsibilities

### Domain (innermost — pure Kotlin)
- **Entities**: core data models (`AnalysisResult`, `ChordSuggestion`, `Recording`)
- **Repository interfaces**: contracts only, no implementation
- **Use cases**: one public `invoke()` function, one job

```kotlin
// Entity
data class AnalysisResult(val key: String, val bpm: Int, val chords: List<String>)

// Repository interface (in domain)
interface AudioRepository {
    suspend fun uploadAndAnalyze(audioFile: File, durationSec: Int): Result<AnalysisResult>
}

// Use case
class AnalyzeAudioUseCase(private val repository: AudioRepository) {
    suspend operator fun invoke(file: File, duration: Int): Result<AnalysisResult> =
        repository.uploadAndAnalyze(file, duration)
}
```

### Data (implements domain interfaces)
- `AudioRepositoryImpl` — wires remote + local sources
- `AudioRemoteDataSource` — FastAPI calls via Retrofit
- `AudioLocalDataSource` — cached files, Room DB if needed
- DTO classes + mappers to domain entities

```kotlin
class AudioRepositoryImpl(
    private val remote: AudioRemoteDataSource
) : AudioRepository {
    override suspend fun uploadAndAnalyze(file: File, duration: Int): Result<AnalysisResult> {
        return try {
            val dto = remote.upload(file, duration)
            Result.Success(dto.toDomain())
        } catch (e: Exception) {
            Result.Error(e.message ?: "Upload failed")
        }
    }
}
```

### Presentation (Android-dependent)
- `ViewModel` holds use cases, emits `StateFlow<UiState>`
- UI (Fragment/Activity/Composable) observes state, sends events
- No business logic here — delegate to use cases

```kotlin
class RecordingViewModel(
    private val analyzeAudio: AnalyzeAudioUseCase
) : ViewModel() {
    private val _state = MutableStateFlow<UiState<AnalysisResult>>(UiState.Idle)
    val state: StateFlow<UiState<AnalysisResult>> = _state.asStateFlow()

    fun onAnalyzeTapped(file: File, duration: Int) {
        viewModelScope.launch {
            _state.value = UiState.Loading
            _state.value = when (val result = analyzeAudio(file, duration)) {
                is Result.Success -> UiState.Success(result.data)
                is Result.Error -> UiState.Error(result.message)
            }
        }
    }
}
```

## TuneMate Use Cases

| Use Case | Input | Output |
|---|---|---|
| `RecordAudioUseCase` | duration (sec) | `File` (audio file) |
| `AnalyzeAudioUseCase` | `File`, duration | `Result<AnalysisResult>` |
| `GenerateChordsUseCase` | key string | `List<String>` (chord names) |
| `PlaybackWithBeatUseCase` | `File`, beat style | playback handle |

## Dependency Injection

Wire at the `Application` or DI module level — never inside use cases or domain:

```kotlin
// Koin / Hilt module
val appModule = module {
    single<AudioRepository> { AudioRepositoryImpl(get()) }
    factory { AnalyzeAudioUseCase(get()) }
    viewModel { RecordingViewModel(get()) }
}
```

## Quick Reference

| Question | Answer |
|---|---|
| Where does Retrofit/OkHttp live? | Data layer only |
| Where does Android Context live? | Presentation or Data — never Domain |
| Where do mappers live? | Data layer (DTO → Entity) |
| Can a use case call another use case? | Yes, inject and call |
| Can domain import `android.*`? | Never |

## Common Mistakes

- Putting business logic in ViewModel instead of a use case
- Having domain entities reference Android types (`Context`, `Uri`)
- Skipping the repository interface and calling the data source directly from ViewModel
- One giant repository doing too many things — split by feature area
