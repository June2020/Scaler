# TuneMate MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the TuneMate MVP — an Android app that records audio, sends it to a Flask backend for key/BPM analysis, displays chord suggestions, and plays back the audio with a beat overlay.

**Architecture:** Two independent components — a Python/Flask backend that receives audio uploads and returns musical analysis (key, BPM, chords), and an Android Kotlin app using Clean Architecture (Domain/Data/Presentation) that handles recording, result display, and local playback.

**Tech Stack:** Python 3.11, Flask, librosa, pytest | Kotlin, Coroutines, StateFlow, Retrofit2, Koin, Navigation Component, AudioRecord, MediaPlayer

---

## File Map

### Backend (`backend/`)
```
backend/
├── app.py                        # Flask app factory + entry point
├── requirements.txt
├── routes/
│   └── audio.py                  # Blueprint: POST /api/audio/analyze
├── services/
│   └── audio_service.py          # librosa key + BPM detection
├── models/
│   └── analysis.py               # AnalysisResult dataclass
├── utils/
│   └── chord_map.py              # Rule-based chord suggestions
└── tests/
    ├── conftest.py               # Flask test client fixture
    ├── test_audio_service.py
    ├── test_chord_map.py
    └── test_routes.py
```

### Android (`android/app/src/main/`)
```
java/com/tunemate/
├── TuneMateApplication.kt        # Application class, Koin init
├── domain/
│   ├── model/
│   │   ├── AnalysisResult.kt     # Core entity
│   │   ├── BeatStyle.kt          # Enum: BASIC, ROCK, JAZZ
│   │   ├── UiState.kt            # sealed class: Idle/Loading/Success/Error
│   │   └── Result.kt             # sealed class: Success/Error
│   ├── repository/
│   │   └── AudioRepository.kt    # interface
│   └── usecase/
│       ├── RecordAudioUseCase.kt  # AudioRecord → WAV file
│       ├── AnalyzeAudioUseCase.kt
│       └── PlaybackUseCase.kt    # MediaPlayer wrapper
├── data/
│   ├── remote/
│   │   ├── TuneMateApi.kt        # Retrofit interface
│   │   ├── dto/
│   │   │   └── AnalysisResponseDto.kt
│   │   └── AudioRemoteDataSource.kt
│   └── repository/
│       └── AudioRepositoryImpl.kt
├── presentation/
│   ├── home/
│   │   ├── HomeFragment.kt
│   │   └── HomeViewModel.kt
│   ├── recording/
│   │   ├── RecordingFragment.kt
│   │   └── RecordingViewModel.kt
│   ├── results/
│   │   ├── ResultsFragment.kt
│   │   └── ResultsViewModel.kt
│   └── playback/
│       ├── PlaybackFragment.kt
│       └── PlaybackViewModel.kt
└── di/
    └── AppModule.kt              # Koin module
res/
├── layout/
│   ├── fragment_home.xml
│   ├── fragment_recording.xml
│   ├── fragment_results.xml
│   └── fragment_playback.xml
└── navigation/
    └── nav_graph.xml
```

---

## PHASE 1 — Flask Backend

---

### Task 1: Backend Scaffold

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/app.py`
- Create: `backend/routes/__init__.py`
- Create: `backend/services/__init__.py`
- Create: `backend/models/__init__.py`
- Create: `backend/utils/__init__.py`
- Create: `backend/tests/__init__.py`

- [ ] **Step 1: Create `backend/requirements.txt`**

```
flask==3.0.3
librosa==0.10.2
numpy==1.26.4
werkzeug==3.0.3
pytest==8.2.0
pytest-flask==1.3.0
soundfile==0.12.1
```

- [ ] **Step 2: Create `backend/app.py`**

```python
from flask import Flask
from routes.audio import audio_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
    app.register_blueprint(audio_bp, url_prefix="/api/audio")

    @app.errorhandler(413)
    def too_large(e):
        return {"error": "File too large (max 50MB)"}, 413

    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Endpoint not found"}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {"error": "Internal server error"}, 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
```

- [ ] **Step 3: Create empty `__init__.py` files in routes/, services/, models/, utils/, tests/**

```bash
touch backend/routes/__init__.py backend/services/__init__.py \
      backend/models/__init__.py backend/utils/__init__.py \
      backend/tests/__init__.py
```

- [ ] **Step 4: Install dependencies**

```bash
cd backend && pip install -r requirements.txt
```

- [ ] **Step 5: Commit**

```bash
git add backend/
git commit -m "feat: backend scaffold — Flask app factory and dependencies"
```

---

### Task 2: AnalysisResult Model

**Files:**
- Create: `backend/models/analysis.py`
- Create: `backend/tests/test_models.py`

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_models.py
from models.analysis import AnalysisResult

def test_analysis_result_fields():
    result = AnalysisResult(key="G Major", bpm=120, chords=["G", "C", "D", "Em"])
    assert result.key == "G Major"
    assert result.bpm == 120
    assert result.chords == ["G", "C", "D", "Em"]

def test_analysis_result_to_dict():
    result = AnalysisResult(key="C Major", bpm=90, chords=["C", "F", "G", "Am"])
    d = result.to_dict()
    assert d == {"key": "C Major", "bpm": 90, "chords": ["C", "F", "G", "Am"]}
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
cd backend && pytest tests/test_models.py -v
```
Expected: `ModuleNotFoundError: No module named 'models.analysis'`

- [ ] **Step 3: Implement `backend/models/analysis.py`**

```python
from dataclasses import dataclass, asdict

@dataclass
class AnalysisResult:
    key: str
    bpm: int
    chords: list[str]

    def to_dict(self) -> dict:
        return asdict(self)
```

- [ ] **Step 4: Run to confirm PASS**

```bash
cd backend && pytest tests/test_models.py -v
```
Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add backend/models/analysis.py backend/tests/test_models.py
git commit -m "feat: AnalysisResult model with to_dict()"
```

---

### Task 3: Chord Map Utility

**Files:**
- Create: `backend/utils/chord_map.py`
- Create: `backend/tests/test_chord_map.py`

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_chord_map.py
from utils.chord_map import get_chord_suggestions

def test_g_major_chords():
    assert get_chord_suggestions("G Major") == ["G", "C", "D", "Em"]

def test_c_major_chords():
    assert get_chord_suggestions("C Major") == ["C", "F", "G", "Am"]

def test_unknown_key_returns_empty():
    assert get_chord_suggestions("X#") == []

def test_minor_key():
    assert get_chord_suggestions("A Minor") == ["Am", "Dm", "Em", "C"]
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
cd backend && pytest tests/test_chord_map.py -v
```
Expected: `ModuleNotFoundError`

- [ ] **Step 3: Implement `backend/utils/chord_map.py`**

```python
CHORD_MAP: dict[str, list[str]] = {
    "C Major":  ["C", "F", "G", "Am"],
    "G Major":  ["G", "C", "D", "Em"],
    "D Major":  ["D", "G", "A", "Bm"],
    "A Major":  ["A", "D", "E", "F#m"],
    "E Major":  ["E", "A", "B", "C#m"],
    "F Major":  ["F", "Bb", "C", "Dm"],
    "Bb Major": ["Bb", "Eb", "F", "Gm"],
    "A Minor":  ["Am", "Dm", "Em", "C"],
    "E Minor":  ["Em", "Am", "Bm", "G"],
    "D Minor":  ["Dm", "Gm", "Am", "F"],
    "B Minor":  ["Bm", "Em", "F#m", "A"],
}

def get_chord_suggestions(key: str) -> list[str]:
    return CHORD_MAP.get(key, [])
```

- [ ] **Step 4: Run to confirm PASS**

```bash
cd backend && pytest tests/test_chord_map.py -v
```
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add backend/utils/chord_map.py backend/tests/test_chord_map.py
git commit -m "feat: rule-based chord suggestions map"
```

---

### Task 4: Audio Service — BPM + Key Detection

**Files:**
- Create: `backend/services/audio_service.py`
- Create: `backend/tests/test_audio_service.py`
- Create: `backend/tests/fixtures/sample.wav` (generate in test setup)

- [ ] **Step 1: Write the failing tests**

```python
# backend/tests/test_audio_service.py
import numpy as np
import soundfile as sf
import tempfile
import os
import pytest
from services.audio_service import detect_bpm, detect_key, analyze_audio
from models.analysis import AnalysisResult

SAMPLE_RATE = 22050

@pytest.fixture
def sine_wav_path():
    """440 Hz sine wave at 120 BPM with click track."""
    duration = 10  # seconds
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # Simple sine tone
    audio = 0.5 * np.sin(2 * np.pi * 440 * t)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, SAMPLE_RATE)
        yield f.name
    os.unlink(f.name)

def test_detect_bpm_returns_int(sine_wav_path):
    bpm = detect_bpm(sine_wav_path)
    assert isinstance(bpm, int)
    assert 40 <= bpm <= 240

def test_detect_key_returns_string(sine_wav_path):
    key = detect_key(sine_wav_path)
    assert isinstance(key, str)
    assert len(key) > 0

def test_analyze_audio_returns_result(sine_wav_path):
    result = analyze_audio(sine_wav_path)
    assert isinstance(result, AnalysisResult)
    assert isinstance(result.key, str)
    assert isinstance(result.bpm, int)
    assert isinstance(result.chords, list)
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
cd backend && pytest tests/test_audio_service.py -v
```
Expected: `ModuleNotFoundError: No module named 'services.audio_service'`

- [ ] **Step 3: Implement `backend/services/audio_service.py`**

```python
import librosa
import numpy as np
from models.analysis import AnalysisResult
from utils.chord_map import get_chord_suggestions

PITCH_CLASSES = ["C", "C#", "D", "D#", "E", "F",
                 "F#", "G", "G#", "A", "A#", "B"]

MINOR_OFFSETS = {9: "A Minor", 4: "E Minor", 11: "B Minor",
                 6: "F# Minor", 1: "C# Minor", 8: "G# Minor",
                 3: "D# Minor", 10: "A# Minor", 5: "F Minor",
                 0: "C Minor", 7: "G Minor", 2: "D Minor"}

def detect_bpm(file_path: str) -> int:
    y, sr = librosa.load(file_path, sr=None)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return int(round(float(tempo)))

def detect_key(file_path: str) -> str:
    y, sr = librosa.load(file_path, sr=None)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    key_index = int(np.argmax(chroma_mean))
    note = PITCH_CLASSES[key_index]
    # Simplified: assume major key based on strongest chroma
    return f"{note} Major"

def analyze_audio(file_path: str) -> AnalysisResult:
    key = detect_key(file_path)
    bpm = detect_bpm(file_path)
    chords = get_chord_suggestions(key)
    return AnalysisResult(key=key, bpm=bpm, chords=chords)
```

- [ ] **Step 4: Run to confirm PASS**

```bash
cd backend && pytest tests/test_audio_service.py -v
```
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add backend/services/audio_service.py backend/tests/test_audio_service.py
git commit -m "feat: audio analysis service — BPM and key detection with librosa"
```

---

### Task 5: Flask Route — POST /api/audio/analyze

**Files:**
- Create: `backend/routes/audio.py`
- Create: `backend/tests/conftest.py`
- Create: `backend/tests/test_routes.py`

- [ ] **Step 1: Create `backend/tests/conftest.py`**

```python
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
```

- [ ] **Step 2: Write the failing route tests**

```python
# backend/tests/test_routes.py
import io
import numpy as np
import soundfile as sf
import pytest

def make_wav_bytes() -> bytes:
    sr = 22050
    audio = 0.5 * np.sin(2 * np.pi * 440 * np.linspace(0, 3, sr * 3))
    buf = io.BytesIO()
    sf.write(buf, audio, sr, format="WAV")
    buf.seek(0)
    return buf.read()

def test_analyze_returns_200(client):
    data = {"file": (io.BytesIO(make_wav_bytes()), "test.wav")}
    response = client.post(
        "/api/audio/analyze",
        content_type="multipart/form-data",
        data=data
    )
    assert response.status_code == 200

def test_analyze_response_has_required_fields(client):
    data = {"file": (io.BytesIO(make_wav_bytes()), "test.wav")}
    response = client.post(
        "/api/audio/analyze",
        content_type="multipart/form-data",
        data=data
    )
    json_data = response.get_json()
    assert "key" in json_data
    assert "bpm" in json_data
    assert "chords" in json_data

def test_analyze_missing_file_returns_400(client):
    response = client.post("/api/audio/analyze", content_type="multipart/form-data", data={})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_analyze_invalid_extension_returns_400(client):
    data = {"file": (io.BytesIO(b"fake"), "test.txt")}
    response = client.post(
        "/api/audio/analyze",
        content_type="multipart/form-data",
        data=data
    )
    assert response.status_code == 400
```

- [ ] **Step 3: Run to confirm FAIL**

```bash
cd backend && pytest tests/test_routes.py -v
```
Expected: connection errors or blueprint not found

- [ ] **Step 4: Implement `backend/routes/audio.py`**

```python
import os
import tempfile
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from services.audio_service import analyze_audio

audio_bp = Blueprint("audio", __name__)

ALLOWED_EXTENSIONS = {"wav", "mp3", "m4a", "ogg", "aac"}

def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@audio_bp.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename or not _allowed(file.filename):
        return jsonify({"error": "Unsupported file type. Use wav, mp3, m4a, ogg, or aac"}), 400

    suffix = "." + secure_filename(file.filename).rsplit(".", 1)[1]
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        result = analyze_audio(tmp_path)
        return jsonify(result.to_dict()), 200
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500
    finally:
        os.unlink(tmp_path)
```

- [ ] **Step 5: Run to confirm PASS**

```bash
cd backend && pytest tests/test_routes.py -v
```
Expected: 4 passed

- [ ] **Step 6: Run all backend tests**

```bash
cd backend && pytest -v
```
Expected: all pass

- [ ] **Step 7: Commit**

```bash
git add backend/routes/audio.py backend/tests/conftest.py backend/tests/test_routes.py
git commit -m "feat: POST /api/audio/analyze endpoint with file upload validation"
```

---

### Task 6: Verify Backend Manually

- [ ] **Step 1: Start the server**

```bash
cd backend && python app.py
```
Expected: `Running on http://127.0.0.1:5000`

- [ ] **Step 2: Test with curl (use any WAV file)**

```bash
curl -X POST http://localhost:5000/api/audio/analyze \
  -F "file=@/path/to/sample.wav"
```
Expected:
```json
{"key": "G Major", "bpm": 120, "chords": ["G", "C", "D", "Em"]}
```

- [ ] **Step 3: Commit backend complete tag**

```bash
git commit --allow-empty -m "chore: backend MVP complete"
```

---

## PHASE 2 — Android App

---

### Task 7: Android Project Setup

**Files:**
- Create: `android/` — new Android Studio project (Empty Activity, Kotlin, min SDK 26)
- Modify: `android/app/build.gradle.kts`
- Modify: `android/app/src/main/AndroidManifest.xml`

- [ ] **Step 1: Create Android project**

In Android Studio: File → New Project → Empty Activity
- Name: TuneMate
- Package: `com.tunemate`
- Language: Kotlin
- Min SDK: API 26 (Android 8.0)
- Save to: `android/`

- [ ] **Step 2: Replace `app/build.gradle.kts` dependencies block**

```kotlin
dependencies {
    // Core
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")

    // Navigation
    implementation("androidx.navigation:navigation-fragment-ktx:2.7.7")
    implementation("androidx.navigation:navigation-ui-ktx:2.7.7")

    // ViewModel + Coroutines
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.8.2")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.2")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1")

    // Retrofit + Gson
    implementation("com.squareup.retrofit2:retrofit:2.11.0")
    implementation("com.squareup.retrofit2:converter-gson:2.11.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

    // Koin DI
    implementation("io.insert-koin:koin-android:3.5.6")
    implementation("io.insert-koin:koin-androidx-viewmodel:3.5.6")

    // Testing
    testImplementation("junit:junit:4.13.2")
    testImplementation("io.mockk:mockk:1.13.11")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.8.1")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.6.1")
}
```

- [ ] **Step 3: Update `AndroidManifest.xml`**

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="28" />

    <application
        android:name=".TuneMateApplication"
        android:allowBackup="true"
        android:label="@string/app_name"
        android:theme="@style/Theme.TuneMate">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

- [ ] **Step 4: Sync Gradle and confirm build succeeds**

```
Build → Make Project (Ctrl+F9)
```
Expected: BUILD SUCCESSFUL

- [ ] **Step 5: Commit**

```bash
git add android/
git commit -m "feat: Android project setup with dependencies and manifest permissions"
```

---

### Task 8: Domain Models

**Files:**
- Create: `android/app/src/main/java/com/tunemate/domain/model/AnalysisResult.kt`
- Create: `android/app/src/main/java/com/tunemate/domain/model/BeatStyle.kt`
- Create: `android/app/src/main/java/com/tunemate/domain/model/UiState.kt`
- Create: `android/app/src/main/java/com/tunemate/domain/model/Result.kt`
- Create: `android/app/src/test/java/com/tunemate/domain/model/AnalysisResultTest.kt`

- [ ] **Step 1: Write the failing test**

```kotlin
// AnalysisResultTest.kt
package com.tunemate.domain.model

import org.junit.Test
import org.junit.Assert.*

class AnalysisResultTest {

    @Test
    fun `analysis result holds key bpm and chords`() {
        val result = AnalysisResult(key = "G Major", bpm = 120, chords = listOf("G", "C", "D", "Em"))
        assertEquals("G Major", result.key)
        assertEquals(120, result.bpm)
        assertEquals(listOf("G", "C", "D", "Em"), result.chords)
    }

    @Test
    fun `bpm label formats correctly`() {
        val result = AnalysisResult(key = "C Major", bpm = 90, chords = emptyList())
        assertEquals("90 BPM", result.bpmLabel)
    }
}
```

- [ ] **Step 2: Run to confirm FAIL**

Run test in Android Studio or: `./gradlew test`
Expected: `Unresolved reference: AnalysisResult`

- [ ] **Step 3: Implement domain models**

```kotlin
// AnalysisResult.kt
package com.tunemate.domain.model

data class AnalysisResult(
    val key: String,
    val bpm: Int,
    val chords: List<String>
) {
    val bpmLabel: String get() = "$bpm BPM"
    val keyLabel: String get() = "Key: $key"
}
```

```kotlin
// BeatStyle.kt
package com.tunemate.domain.model

enum class BeatStyle(val displayName: String) {
    BASIC("Basic"),
    ROCK("Rock"),
    JAZZ("Jazz")
}
```

```kotlin
// Result.kt
package com.tunemate.domain.model

sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val message: String, val cause: Throwable? = null) : Result<Nothing>()
}
```

```kotlin
// UiState.kt
package com.tunemate.domain.model

sealed class UiState<out T> {
    object Idle : UiState<Nothing>()
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}
```

- [ ] **Step 4: Run to confirm PASS**

```bash
./gradlew test --tests "com.tunemate.domain.model.AnalysisResultTest"
```
Expected: 2 tests passed

- [ ] **Step 5: Commit**

```bash
git add android/app/src/main/java/com/tunemate/domain/model/
git add android/app/src/test/java/com/tunemate/domain/model/
git commit -m "feat: domain models — AnalysisResult, BeatStyle, UiState, Result"
```

---

### Task 9: Repository Interface + Use Cases

**Files:**
- Create: `android/app/src/main/java/com/tunemate/domain/repository/AudioRepository.kt`
- Create: `android/app/src/main/java/com/tunemate/domain/usecase/AnalyzeAudioUseCase.kt`
- Create: `android/app/src/test/java/com/tunemate/domain/usecase/AnalyzeAudioUseCaseTest.kt`

- [ ] **Step 1: Write the failing test**

```kotlin
// AnalyzeAudioUseCaseTest.kt
package com.tunemate.domain.usecase

import com.tunemate.domain.model.AnalysisResult
import com.tunemate.domain.model.Result
import com.tunemate.domain.repository.AudioRepository
import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.test.runTest
import org.junit.Assert.*
import org.junit.Test
import java.io.File

class AnalyzeAudioUseCaseTest {

    private val repository: AudioRepository = mockk()
    private val useCase = AnalyzeAudioUseCase(repository)

    @Test
    fun `returns success result from repository`() = runTest {
        val file = mockk<File>()
        val expected = AnalysisResult("G Major", 120, listOf("G", "C", "D", "Em"))
        coEvery { repository.analyzeAudio(file, 60) } returns Result.Success(expected)

        val result = useCase(file, 60)

        assertTrue(result is Result.Success)
        assertEquals(expected, (result as Result.Success).data)
    }

    @Test
    fun `returns error result when repository fails`() = runTest {
        val file = mockk<File>()
        coEvery { repository.analyzeAudio(file, 60) } returns Result.Error("Network error")

        val result = useCase(file, 60)

        assertTrue(result is Result.Error)
        assertEquals("Network error", (result as Result.Error).message)
    }
}
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
./gradlew test --tests "com.tunemate.domain.usecase.AnalyzeAudioUseCaseTest"
```
Expected: `Unresolved reference: AudioRepository`

- [ ] **Step 3: Create `AudioRepository.kt`**

```kotlin
package com.tunemate.domain.repository

import com.tunemate.domain.model.AnalysisResult
import com.tunemate.domain.model.Result
import java.io.File

interface AudioRepository {
    suspend fun analyzeAudio(file: File, durationSec: Int): Result<AnalysisResult>
}
```

- [ ] **Step 4: Create `AnalyzeAudioUseCase.kt`**

```kotlin
package com.tunemate.domain.usecase

import com.tunemate.domain.model.AnalysisResult
import com.tunemate.domain.model.Result
import com.tunemate.domain.repository.AudioRepository
import java.io.File

class AnalyzeAudioUseCase(private val repository: AudioRepository) {
    suspend operator fun invoke(file: File, durationSec: Int): Result<AnalysisResult> =
        repository.analyzeAudio(file, durationSec)
}
```

- [ ] **Step 5: Run to confirm PASS**

```bash
./gradlew test --tests "com.tunemate.domain.usecase.AnalyzeAudioUseCaseTest"
```
Expected: 2 tests passed

- [ ] **Step 6: Commit**

```bash
git add android/app/src/main/java/com/tunemate/domain/
git add android/app/src/test/java/com/tunemate/domain/
git commit -m "feat: AudioRepository interface and AnalyzeAudioUseCase"
```

---

### Task 10: Retrofit API Client + DTO + Remote Data Source

**Files:**
- Create: `android/app/src/main/java/com/tunemate/data/remote/TuneMateApi.kt`
- Create: `android/app/src/main/java/com/tunemate/data/remote/dto/AnalysisResponseDto.kt`
- Create: `android/app/src/main/java/com/tunemate/data/remote/AudioRemoteDataSource.kt`
- Create: `android/app/src/test/java/com/tunemate/data/remote/AudioRemoteDataSourceTest.kt`

- [ ] **Step 1: Write the failing test**

```kotlin
// AudioRemoteDataSourceTest.kt
package com.tunemate.data.remote

import com.tunemate.data.remote.dto.AnalysisResponseDto
import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.test.runTest
import okhttp3.MultipartBody
import org.junit.Assert.*
import org.junit.Test
import java.io.File

class AudioRemoteDataSourceTest {

    private val api: TuneMateApi = mockk()
    private val dataSource = AudioRemoteDataSource(api)

    @Test
    fun `upload returns dto on success`() = runTest {
        val mockFile = mockk<File>(relaxed = true)
        val dto = AnalysisResponseDto(key = "G Major", bpm = 120, chords = listOf("G", "C", "D", "Em"))
        coEvery { api.analyzeAudio(any()) } returns dto

        val result = dataSource.upload(mockFile)

        assertEquals("G Major", result.key)
        assertEquals(120, result.bpm)
    }
}
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
./gradlew test --tests "com.tunemate.data.remote.AudioRemoteDataSourceTest"
```
Expected: `Unresolved reference: TuneMateApi`

- [ ] **Step 3: Create `AnalysisResponseDto.kt`**

```kotlin
package com.tunemate.data.remote.dto

import com.tunemate.domain.model.AnalysisResult

data class AnalysisResponseDto(
    val key: String,
    val bpm: Int,
    val chords: List<String>
) {
    fun toDomain() = AnalysisResult(key = key, bpm = bpm, chords = chords)
}
```

- [ ] **Step 4: Create `TuneMateApi.kt`**

```kotlin
package com.tunemate.data.remote

import com.tunemate.data.remote.dto.AnalysisResponseDto
import okhttp3.MultipartBody
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

interface TuneMateApi {
    @Multipart
    @POST("audio/analyze")
    suspend fun analyzeAudio(
        @Part file: MultipartBody.Part
    ): AnalysisResponseDto
}
```

- [ ] **Step 5: Create `AudioRemoteDataSource.kt`**

```kotlin
package com.tunemate.data.remote

import com.tunemate.data.remote.dto.AnalysisResponseDto
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File

class AudioRemoteDataSource(private val api: TuneMateApi) {
    suspend fun upload(file: File): AnalysisResponseDto {
        val requestBody = file.asRequestBody("audio/*".toMediaTypeOrNull())
        val part = MultipartBody.Part.createFormData("file", file.name, requestBody)
        return api.analyzeAudio(part)
    }
}
```

- [ ] **Step 6: Run to confirm PASS**

```bash
./gradlew test --tests "com.tunemate.data.remote.AudioRemoteDataSourceTest"
```
Expected: 1 test passed

- [ ] **Step 7: Commit**

```bash
git add android/app/src/main/java/com/tunemate/data/remote/
git add android/app/src/test/java/com/tunemate/data/remote/
git commit -m "feat: Retrofit API client, AnalysisResponseDto, AudioRemoteDataSource"
```

---

### Task 11: Repository Implementation

**Files:**
- Create: `android/app/src/main/java/com/tunemate/data/repository/AudioRepositoryImpl.kt`
- Create: `android/app/src/test/java/com/tunemate/data/repository/AudioRepositoryImplTest.kt`

- [ ] **Step 1: Write the failing test**

```kotlin
// AudioRepositoryImplTest.kt
package com.tunemate.data.repository

import com.tunemate.data.remote.AudioRemoteDataSource
import com.tunemate.data.remote.dto.AnalysisResponseDto
import com.tunemate.domain.model.Result
import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.test.runTest
import org.junit.Assert.*
import org.junit.Test
import java.io.File

class AudioRepositoryImplTest {

    private val remote: AudioRemoteDataSource = mockk()
    private val repository = AudioRepositoryImpl(remote)

    @Test
    fun `analyzeAudio returns Success when remote call succeeds`() = runTest {
        val file = mockk<File>(relaxed = true)
        val dto = AnalysisResponseDto("G Major", 120, listOf("G", "C", "D", "Em"))
        coEvery { remote.upload(file) } returns dto

        val result = repository.analyzeAudio(file, 60)

        assertTrue(result is Result.Success)
        assertEquals("G Major", (result as Result.Success).data.key)
    }

    @Test
    fun `analyzeAudio returns Error when remote call throws`() = runTest {
        val file = mockk<File>(relaxed = true)
        coEvery { remote.upload(file) } throws Exception("timeout")

        val result = repository.analyzeAudio(file, 60)

        assertTrue(result is Result.Error)
        assertTrue((result as Result.Error).message.contains("timeout"))
    }
}
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
./gradlew test --tests "com.tunemate.data.repository.AudioRepositoryImplTest"
```
Expected: `Unresolved reference: AudioRepositoryImpl`

- [ ] **Step 3: Implement `AudioRepositoryImpl.kt`**

```kotlin
package com.tunemate.data.repository

import com.tunemate.data.remote.AudioRemoteDataSource
import com.tunemate.domain.model.AnalysisResult
import com.tunemate.domain.model.Result
import com.tunemate.domain.repository.AudioRepository
import java.io.File

class AudioRepositoryImpl(
    private val remote: AudioRemoteDataSource
) : AudioRepository {
    override suspend fun analyzeAudio(file: File, durationSec: Int): Result<AnalysisResult> {
        return try {
            val dto = remote.upload(file)
            Result.Success(dto.toDomain())
        } catch (e: Exception) {
            Result.Error(e.message ?: "Analysis failed", e)
        }
    }
}
```

- [ ] **Step 4: Run to confirm PASS**

```bash
./gradlew test --tests "com.tunemate.data.repository.AudioRepositoryImplTest"
```
Expected: 2 tests passed

- [ ] **Step 5: Commit**

```bash
git add android/app/src/main/java/com/tunemate/data/repository/
git add android/app/src/test/java/com/tunemate/data/repository/
git commit -m "feat: AudioRepositoryImpl with error wrapping"
```

---

### Task 12: Koin DI Module + Application Class

**Files:**
- Create: `android/app/src/main/java/com/tunemate/di/AppModule.kt`
- Create: `android/app/src/main/java/com/tunemate/TuneMateApplication.kt`

- [ ] **Step 1: Create `AppModule.kt`**

```kotlin
package com.tunemate.di

import com.tunemate.data.remote.AudioRemoteDataSource
import com.tunemate.data.remote.TuneMateApi
import com.tunemate.data.repository.AudioRepositoryImpl
import com.tunemate.domain.repository.AudioRepository
import com.tunemate.domain.usecase.AnalyzeAudioUseCase
import com.tunemate.presentation.recording.RecordingViewModel
import com.tunemate.presentation.results.ResultsViewModel
import com.tunemate.presentation.playback.PlaybackViewModel
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import org.koin.androidx.viewmodel.dsl.viewModel
import org.koin.dsl.module
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

private const val BASE_URL = "http://10.0.2.2:5000/api/"  // 10.0.2.2 = localhost from emulator

val appModule = module {
    single {
        OkHttpClient.Builder()
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            })
            .build()
    }
    single {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(get())
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(TuneMateApi::class.java)
    }
    single { AudioRemoteDataSource(get()) }
    single<AudioRepository> { AudioRepositoryImpl(get()) }
    factory { AnalyzeAudioUseCase(get()) }
    viewModel { RecordingViewModel(get()) }
    viewModel { ResultsViewModel() }
    viewModel { PlaybackViewModel() }
}
```

- [ ] **Step 2: Create `TuneMateApplication.kt`**

```kotlin
package com.tunemate

import android.app.Application
import com.tunemate.di.appModule
import org.koin.android.ext.koin.androidContext
import org.koin.core.context.startKoin

class TuneMateApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@TuneMateApplication)
            modules(appModule)
        }
    }
}
```

- [ ] **Step 3: Build to confirm no errors**

```
Build → Make Project
```
Expected: BUILD SUCCESSFUL

- [ ] **Step 4: Commit**

```bash
git add android/app/src/main/java/com/tunemate/di/
git add android/app/src/main/java/com/tunemate/TuneMateApplication.kt
git commit -m "feat: Koin DI module and Application class"
```

---

### Task 13: RecordAudioUseCase (AudioRecord → WAV)

**Files:**
- Create: `android/app/src/main/java/com/tunemate/domain/usecase/RecordAudioUseCase.kt`
- Create: `android/app/src/test/java/com/tunemate/domain/usecase/RecordAudioUseCaseTest.kt`

- [ ] **Step 1: Write the failing test**

```kotlin
// RecordAudioUseCaseTest.kt
package com.tunemate.domain.usecase

import android.content.Context
import io.mockk.every
import io.mockk.mockk
import org.junit.Assert.*
import org.junit.Test
import java.io.File

class RecordAudioUseCaseTest {

    private val context: Context = mockk()

    @Test
    fun `output file has wav extension`() {
        val cacheDir = createTempDir()
        every { context.cacheDir } returns cacheDir
        val useCase = RecordAudioUseCase(context)
        assertTrue(useCase.outputFile().name.endsWith(".wav"))
    }
}
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
./gradlew test --tests "com.tunemate.domain.usecase.RecordAudioUseCaseTest"
```
Expected: `Unresolved reference: RecordAudioUseCase`

- [ ] **Step 3: Implement `RecordAudioUseCase.kt`**

```kotlin
package com.tunemate.domain.usecase

import android.content.Context
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileOutputStream
import java.nio.ByteBuffer
import java.nio.ByteOrder

class RecordAudioUseCase(private val context: Context) {

    private val sampleRate = 44100
    private val channelConfig = AudioFormat.CHANNEL_IN_MONO
    private val encoding = AudioFormat.ENCODING_PCM_16BIT
    private var recorder: AudioRecord? = null
    private var isRecording = false

    fun outputFile(): File = File(context.cacheDir, "tunemate_recording.wav")

    suspend fun start() = withContext(Dispatchers.IO) {
        val bufferSize = AudioRecord.getMinBufferSize(sampleRate, channelConfig, encoding)
        recorder = AudioRecord(MediaRecorder.AudioSource.MIC, sampleRate, channelConfig, encoding, bufferSize)
        val output = outputFile()
        val rawData = mutableListOf<Byte>()

        recorder?.startRecording()
        isRecording = true

        val buffer = ShortArray(bufferSize)
        while (isRecording) {
            val read = recorder?.read(buffer, 0, buffer.size) ?: 0
            for (i in 0 until read) {
                val bytes = ByteBuffer.allocate(2).order(ByteOrder.LITTLE_ENDIAN).putShort(buffer[i]).array()
                rawData.addAll(bytes.toList())
            }
        }
        writeWav(output, rawData.toByteArray(), sampleRate)
    }

    fun stop() {
        isRecording = false
        recorder?.stop()
        recorder?.release()
        recorder = null
    }

    private fun writeWav(file: File, pcm: ByteArray, sampleRate: Int) {
        val totalDataLen = pcm.size + 36
        FileOutputStream(file).use { out ->
            // WAV header
            out.write("RIFF".toByteArray())
            out.write(intToBytes(totalDataLen))
            out.write("WAVE".toByteArray())
            out.write("fmt ".toByteArray())
            out.write(intToBytes(16))           // chunk size
            out.write(shortToBytes(1))          // PCM format
            out.write(shortToBytes(1))          // mono
            out.write(intToBytes(sampleRate))
            out.write(intToBytes(sampleRate * 2))
            out.write(shortToBytes(2))          // block align
            out.write(shortToBytes(16))         // bits per sample
            out.write("data".toByteArray())
            out.write(intToBytes(pcm.size))
            out.write(pcm)
        }
    }

    private fun intToBytes(v: Int) = ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(v).array()
    private fun shortToBytes(v: Int) = ByteBuffer.allocate(2).order(ByteOrder.LITTLE_ENDIAN).putShort(v.toShort()).array()
}
```

- [ ] **Step 4: Run to confirm PASS**

```bash
./gradlew test --tests "com.tunemate.domain.usecase.RecordAudioUseCaseTest"
```
Expected: 1 test passed

- [ ] **Step 5: Commit**

```bash
git add android/app/src/main/java/com/tunemate/domain/usecase/RecordAudioUseCase.kt
git add android/app/src/test/java/com/tunemate/domain/usecase/RecordAudioUseCaseTest.kt
git commit -m "feat: RecordAudioUseCase — AudioRecord to WAV file"
```

---

### Task 14: Navigation Graph + MainActivity

**Files:**
- Create: `android/app/src/main/res/navigation/nav_graph.xml`
- Modify: `android/app/src/main/res/layout/activity_main.xml`
- Modify: `android/app/src/main/java/com/tunemate/MainActivity.kt`

- [ ] **Step 1: Create `res/navigation/nav_graph.xml`**

```xml
<?xml version="1.0" encoding="utf-8"?>
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/nav_graph"
    app:startDestination="@id/homeFragment">

    <fragment android:id="@+id/homeFragment"
        android:name="com.tunemate.presentation.home.HomeFragment"
        android:label="Home">
        <action android:id="@+id/action_home_to_recording"
            app:destination="@id/recordingFragment" />
    </fragment>

    <fragment android:id="@+id/recordingFragment"
        android:name="com.tunemate.presentation.recording.RecordingFragment"
        android:label="Recording">
        <action android:id="@+id/action_recording_to_results"
            app:destination="@id/resultsFragment" />
    </fragment>

    <fragment android:id="@+id/resultsFragment"
        android:name="com.tunemate.presentation.results.ResultsFragment"
        android:label="Results">
        <argument android:name="analysisResult"
            app:argType="com.tunemate.domain.model.AnalysisResult" />
        <action android:id="@+id/action_results_to_playback"
            app:destination="@id/playbackFragment" />
        <action android:id="@+id/action_results_retry"
            app:destination="@id/recordingFragment"
            app:popUpTo="@id/homeFragment" />
    </fragment>

    <fragment android:id="@+id/playbackFragment"
        android:name="com.tunemate.presentation.playback.PlaybackFragment"
        android:label="Playback">
        <action android:id="@+id/action_playback_retry"
            app:destination="@id/recordingFragment"
            app:popUpTo="@id/homeFragment" />
    </fragment>
</navigation>
```

- [ ] **Step 2: Update `activity_main.xml`**

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.fragment.app.FragmentContainerView
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/nav_host_fragment"
    android:name="androidx.navigation.fragment.NavHostFragment"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    app:defaultNavHost="true"
    app:navGraph="@navigation/nav_graph" />
```

- [ ] **Step 3: Update `MainActivity.kt`**

```kotlin
package com.tunemate

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}
```

- [ ] **Step 4: Build to confirm no errors**

```
Build → Make Project
```
Expected: BUILD SUCCESSFUL

- [ ] **Step 5: Commit**

```bash
git add android/app/src/main/res/navigation/ android/app/src/main/res/layout/activity_main.xml
git add android/app/src/main/java/com/tunemate/MainActivity.kt
git commit -m "feat: navigation graph with Home→Recording→Results→Playback flow"
```

---

### Task 15: HomeFragment + HomeViewModel

**Files:**
- Create: `android/app/src/main/java/com/tunemate/presentation/home/HomeViewModel.kt`
- Create: `android/app/src/main/java/com/tunemate/presentation/home/HomeFragment.kt`
- Create: `android/app/src/main/res/layout/fragment_home.xml`
- Create: `android/app/src/test/java/com/tunemate/presentation/home/HomeViewModelTest.kt`

- [ ] **Step 1: Write the failing test**

```kotlin
// HomeViewModelTest.kt
package com.tunemate.presentation.home

import org.junit.Assert.*
import org.junit.Test

class HomeViewModelTest {

    private val viewModel = HomeViewModel()

    @Test
    fun `default duration is 60 seconds`() {
        assertEquals(60, viewModel.selectedDuration.value)
    }

    @Test
    fun `setDuration updates selected duration`() {
        viewModel.setDuration(120)
        assertEquals(120, viewModel.selectedDuration.value)
    }
}
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
./gradlew test --tests "com.tunemate.presentation.home.HomeViewModelTest"
```
Expected: `Unresolved reference: HomeViewModel`

- [ ] **Step 3: Create `HomeViewModel.kt`**

```kotlin
package com.tunemate.presentation.home

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class HomeViewModel : ViewModel() {
    private val _selectedDuration = MutableStateFlow(60)
    val selectedDuration: StateFlow<Int> = _selectedDuration

    fun setDuration(seconds: Int) {
        _selectedDuration.value = seconds
    }
}
```

- [ ] **Step 4: Create `fragment_home.xml`**

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="32dp">

    <TextView
        android:id="@+id/tvTitle"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="TuneMate"
        android:textSize="32sp"
        android:textStyle="bold"
        android:layout_marginBottom="48dp" />

    <RadioGroup
        android:id="@+id/rgDuration"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:layout_marginBottom="48dp">

        <RadioButton android:id="@+id/rb1min" android:layout_width="wrap_content"
            android:layout_height="wrap_content" android:text="1 min" android:checked="true" android:tag="60" />
        <RadioButton android:id="@+id/rb2min" android:layout_width="wrap_content"
            android:layout_height="wrap_content" android:text="2 min" android:tag="120" />
        <RadioButton android:id="@+id/rb5min" android:layout_width="wrap_content"
            android:layout_height="wrap_content" android:text="5 min" android:tag="300" />
    </RadioGroup>

    <Button
        android:id="@+id/btnRecord"
        android:layout_width="160dp"
        android:layout_height="160dp"
        android:text="Record"
        android:textSize="18sp" />
</LinearLayout>
```

- [ ] **Step 5: Create `HomeFragment.kt`**

```kotlin
package com.tunemate.presentation.home

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.RadioGroup
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.tunemate.R
import com.tunemate.databinding.FragmentHomeBinding
import org.koin.androidx.viewmodel.ext.android.viewModel

class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!
    private val viewModel: HomeViewModel by viewModel()

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        binding.rgDuration.setOnCheckedChangeListener { group, checkedId ->
            val radio = group.findViewById<View>(checkedId)
            val seconds = (radio.tag as String).toInt()
            viewModel.setDuration(seconds)
        }

        binding.btnRecord.setOnClickListener {
            val action = HomeFragmentDirections.actionHomeToRecording()
            findNavController().navigate(action)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
```

- [ ] **Step 6: Enable ViewBinding in `build.gradle.kts`**

Inside `android {}` block:
```kotlin
buildFeatures {
    viewBinding = true
}
```

- [ ] **Step 7: Run test to confirm PASS**

```bash
./gradlew test --tests "com.tunemate.presentation.home.HomeViewModelTest"
```
Expected: 2 tests passed

- [ ] **Step 8: Commit**

```bash
git add android/app/src/main/java/com/tunemate/presentation/home/
git add android/app/src/main/res/layout/fragment_home.xml
git commit -m "feat: HomeFragment — duration selection and record button"
```

---

### Task 16: RecordingFragment + RecordingViewModel

**Files:**
- Create: `android/app/src/main/java/com/tunemate/presentation/recording/RecordingViewModel.kt`
- Create: `android/app/src/main/java/com/tunemate/presentation/recording/RecordingFragment.kt`
- Create: `android/app/src/main/res/layout/fragment_recording.xml`
- Create: `android/app/src/test/java/com/tunemate/presentation/recording/RecordingViewModelTest.kt`

- [ ] **Step 1: Write the failing test**

```kotlin
// RecordingViewModelTest.kt
package com.tunemate.presentation.recording

import com.tunemate.domain.model.AnalysisResult
import com.tunemate.domain.model.Result
import com.tunemate.domain.model.UiState
import com.tunemate.domain.usecase.AnalyzeAudioUseCase
import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.*
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import java.io.File

@OptIn(ExperimentalCoroutinesApi::class)
class RecordingViewModelTest {

    private val testDispatcher = UnconfinedTestDispatcher()
    private val analyzeAudio: AnalyzeAudioUseCase = mockk()
    private lateinit var viewModel: RecordingViewModel

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        viewModel = RecordingViewModel(analyzeAudio)
    }

    @After
    fun tearDown() { Dispatchers.resetMain() }

    @Test
    fun `initial state is Idle`() {
        assertTrue(viewModel.uiState.value is UiState.Idle)
    }

    @Test
    fun `onAnalyzeTapped transitions to Success on success`() = runTest {
        val file = mockk<File>(relaxed = true)
        val expected = AnalysisResult("G Major", 120, listOf("G", "C", "D", "Em"))
        coEvery { analyzeAudio(file, 60) } returns Result.Success(expected)

        viewModel.onAnalyzeTapped(file, 60)

        val state = viewModel.uiState.value
        assertTrue(state is UiState.Success)
        assertEquals("G Major", (state as UiState.Success).data.key)
    }

    @Test
    fun `onAnalyzeTapped transitions to Error on failure`() = runTest {
        val file = mockk<File>(relaxed = true)
        coEvery { analyzeAudio(file, 60) } returns Result.Error("timeout")

        viewModel.onAnalyzeTapped(file, 60)

        assertTrue(viewModel.uiState.value is UiState.Error)
    }
}
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
./gradlew test --tests "com.tunemate.presentation.recording.RecordingViewModelTest"
```
Expected: `Unresolved reference: RecordingViewModel`

- [ ] **Step 3: Create `RecordingViewModel.kt`**

```kotlin
package com.tunemate.presentation.recording

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.tunemate.domain.model.AnalysisResult
import com.tunemate.domain.model.Result
import com.tunemate.domain.model.UiState
import com.tunemate.domain.usecase.AnalyzeAudioUseCase
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import java.io.File

class RecordingViewModel(
    private val analyzeAudio: AnalyzeAudioUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState<AnalysisResult>>(UiState.Idle)
    val uiState: StateFlow<UiState<AnalysisResult>> = _uiState

    fun onAnalyzeTapped(file: File, durationSec: Int) {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            _uiState.value = when (val result = analyzeAudio(file, durationSec)) {
                is Result.Success -> UiState.Success(result.data)
                is Result.Error -> UiState.Error(result.message)
            }
        }
    }
}
```

- [ ] **Step 4: Create `fragment_recording.xml`**

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="32dp">

    <TextView
        android:id="@+id/tvStatus"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Recording..."
        android:textSize="20sp"
        android:layout_marginBottom="24dp" />

    <!-- Waveform placeholder — replace with custom WaveformView later -->
    <View
        android:id="@+id/waveformView"
        android:layout_width="match_parent"
        android:layout_height="80dp"
        android:background="#FFDDDDDD"
        android:layout_marginBottom="32dp" />

    <TextView
        android:id="@+id/tvTimer"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="0:00"
        android:textSize="48sp"
        android:layout_marginBottom="48dp" />

    <LinearLayout android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:orientation="horizontal">

        <Button android:id="@+id/btnStop"
            android:layout_width="wrap_content" android:layout_height="wrap_content"
            android:text="Stop" android:layout_marginEnd="16dp" />

        <Button android:id="@+id/btnAnalyze"
            android:layout_width="wrap_content" android:layout_height="wrap_content"
            android:text="Analyze" android:enabled="false" />
    </LinearLayout>

    <ProgressBar android:id="@+id/progressBar"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:visibility="gone" android:layout_marginTop="24dp" />
</LinearLayout>
```

- [ ] **Step 5: Create `RecordingFragment.kt`**

```kotlin
package com.tunemate.presentation.recording

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.findNavController
import com.tunemate.databinding.FragmentRecordingBinding
import com.tunemate.domain.model.UiState
import com.tunemate.domain.usecase.RecordAudioUseCase
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import org.koin.android.ext.android.inject
import org.koin.androidx.viewmodel.ext.android.viewModel

class RecordingFragment : Fragment() {

    private var _binding: FragmentRecordingBinding? = null
    private val binding get() = _binding!!
    private val viewModel: RecordingViewModel by viewModel()
    private val recordUseCase: RecordAudioUseCase by inject()
    private var recordingJob: Job? = null

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentRecordingBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        startRecordingIfPermitted()

        binding.btnStop.setOnClickListener {
            recordingJob?.cancel()
            recordUseCase.stop()
            binding.btnAnalyze.isEnabled = true
        }

        binding.btnAnalyze.setOnClickListener {
            val file = recordUseCase.outputFile()
            viewModel.onAnalyzeTapped(file, durationSec = 60)
        }

        viewLifecycleOwner.lifecycleScope.launch {
            viewModel.uiState.collect { state ->
                when (state) {
                    is UiState.Loading -> {
                        binding.progressBar.visibility = View.VISIBLE
                        binding.btnAnalyze.isEnabled = false
                    }
                    is UiState.Success -> {
                        binding.progressBar.visibility = View.GONE
                        val action = RecordingFragmentDirections
                            .actionRecordingToResults(state.data)
                        findNavController().navigate(action)
                    }
                    is UiState.Error -> {
                        binding.progressBar.visibility = View.GONE
                        binding.tvStatus.text = "Error: ${state.message}"
                        binding.btnAnalyze.isEnabled = true
                    }
                    else -> Unit
                }
            }
        }
    }

    private fun startRecordingIfPermitted() {
        if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.RECORD_AUDIO)
            == PackageManager.PERMISSION_GRANTED) {
            recordingJob = viewLifecycleOwner.lifecycleScope.launch {
                recordUseCase.start()
            }
        } else {
            requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO), 1001)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
```

- [ ] **Step 6: Run test to confirm PASS**

```bash
./gradlew test --tests "com.tunemate.presentation.recording.RecordingViewModelTest"
```
Expected: 3 tests passed

- [ ] **Step 7: Commit**

```bash
git add android/app/src/main/java/com/tunemate/presentation/recording/
git add android/app/src/main/res/layout/fragment_recording.xml
git add android/app/src/test/java/com/tunemate/presentation/recording/
git commit -m "feat: RecordingFragment — record, stop, analyze with loading state"
```

---

### Task 17: ResultsFragment + ResultsViewModel

**Files:**
- Create: `android/app/src/main/java/com/tunemate/presentation/results/ResultsViewModel.kt`
- Create: `android/app/src/main/java/com/tunemate/presentation/results/ResultsFragment.kt`
- Create: `android/app/src/main/res/layout/fragment_results.xml`

- [ ] **Step 1: Create `fragment_results.xml`**

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="32dp">

    <TextView android:id="@+id/tvKey"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:textSize="48sp" android:textStyle="bold"
        android:layout_marginBottom="16dp" />

    <TextView android:id="@+id/tvBpm"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:textSize="24sp" android:layout_marginBottom="24dp" />

    <TextView android:id="@+id/tvChordsLabel"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:text="Suggested Chords"
        android:textSize="16sp" android:layout_marginBottom="8dp" />

    <TextView android:id="@+id/tvChords"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:textSize="28sp" android:layout_marginBottom="48dp" />

    <Button android:id="@+id/btnPlayback"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:text="Play with Beat &amp; Guitar"
        android:layout_marginBottom="16dp" />

    <Button android:id="@+id/btnRetry"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:text="Try Again"
        style="@style/Widget.MaterialComponents.Button.OutlinedButton" />
</LinearLayout>
```

- [ ] **Step 2: Create `ResultsViewModel.kt`**

```kotlin
package com.tunemate.presentation.results

import androidx.lifecycle.ViewModel
import com.tunemate.domain.model.AnalysisResult
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class ResultsViewModel : ViewModel() {
    private val _result = MutableStateFlow<AnalysisResult?>(null)
    val result: StateFlow<AnalysisResult?> = _result

    fun setResult(analysisResult: AnalysisResult) {
        _result.value = analysisResult
    }
}
```

- [ ] **Step 3: Create `ResultsFragment.kt`**

```kotlin
package com.tunemate.presentation.results

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs
import com.tunemate.databinding.FragmentResultsBinding
import org.koin.androidx.viewmodel.ext.android.viewModel

class ResultsFragment : Fragment() {

    private var _binding: FragmentResultsBinding? = null
    private val binding get() = _binding!!
    private val viewModel: ResultsViewModel by viewModel()
    private val args: ResultsFragmentArgs by navArgs()

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentResultsBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val result = args.analysisResult
        viewModel.setResult(result)

        binding.tvKey.text = result.keyLabel
        binding.tvBpm.text = result.bpmLabel
        binding.tvChords.text = result.chords.joinToString(" – ")

        binding.btnPlayback.setOnClickListener {
            findNavController().navigate(
                ResultsFragmentDirections.actionResultsToPlayback()
            )
        }

        binding.btnRetry.setOnClickListener {
            findNavController().navigate(
                ResultsFragmentDirections.actionResultsRetry()
            )
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
```

- [ ] **Step 4: Make `AnalysisResult` Parcelable (required for nav args)**

Add `@Parcelize` to `AnalysisResult.kt`:
```kotlin
import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class AnalysisResult(
    val key: String,
    val bpm: Int,
    val chords: List<String>
) : Parcelable {
    val bpmLabel: String get() = "$bpm BPM"
    val keyLabel: String get() = "Key: $key"
}
```

Enable parcelize plugin in `build.gradle.kts`:
```kotlin
plugins {
    id("kotlin-parcelize")
}
```

- [ ] **Step 5: Build to confirm no errors**

```
Build → Make Project
```

- [ ] **Step 6: Commit**

```bash
git add android/app/src/main/java/com/tunemate/presentation/results/
git add android/app/src/main/res/layout/fragment_results.xml
git add android/app/src/main/java/com/tunemate/domain/model/AnalysisResult.kt
git commit -m "feat: ResultsFragment — display key, BPM, chords with retry and playback actions"
```

---

### Task 18: PlaybackFragment + PlaybackViewModel

**Files:**
- Create: `android/app/src/main/java/com/tunemate/presentation/playback/PlaybackViewModel.kt`
- Create: `android/app/src/main/java/com/tunemate/presentation/playback/PlaybackFragment.kt`
- Create: `android/app/src/main/res/layout/fragment_playback.xml`
- Create: `android/app/src/test/java/com/tunemate/presentation/playback/PlaybackViewModelTest.kt`

- [ ] **Step 1: Write the failing test**

```kotlin
// PlaybackViewModelTest.kt
package com.tunemate.presentation.playback

import com.tunemate.domain.model.BeatStyle
import org.junit.Assert.*
import org.junit.Test

class PlaybackViewModelTest {

    private val viewModel = PlaybackViewModel()

    @Test
    fun `default beat style is BASIC`() {
        assertEquals(BeatStyle.BASIC, viewModel.beatStyle.value)
    }

    @Test
    fun `guitar is enabled by default`() {
        assertTrue(viewModel.guitarEnabled.value)
    }

    @Test
    fun `toggleGuitar flips guitar state`() {
        viewModel.toggleGuitar()
        assertFalse(viewModel.guitarEnabled.value)
    }

    @Test
    fun `setBeatStyle updates beat style`() {
        viewModel.setBeatStyle(BeatStyle.ROCK)
        assertEquals(BeatStyle.ROCK, viewModel.beatStyle.value)
    }
}
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
./gradlew test --tests "com.tunemate.presentation.playback.PlaybackViewModelTest"
```
Expected: `Unresolved reference: PlaybackViewModel`

- [ ] **Step 3: Create `PlaybackViewModel.kt`**

```kotlin
package com.tunemate.presentation.playback

import androidx.lifecycle.ViewModel
import com.tunemate.domain.model.BeatStyle
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class PlaybackViewModel : ViewModel() {
    private val _beatStyle = MutableStateFlow(BeatStyle.BASIC)
    val beatStyle: StateFlow<BeatStyle> = _beatStyle

    private val _guitarEnabled = MutableStateFlow(true)
    val guitarEnabled: StateFlow<Boolean> = _guitarEnabled

    private val _isPlaying = MutableStateFlow(false)
    val isPlaying: StateFlow<Boolean> = _isPlaying

    fun setBeatStyle(style: BeatStyle) { _beatStyle.value = style }
    fun toggleGuitar() { _guitarEnabled.value = !_guitarEnabled.value }
    fun setPlaying(playing: Boolean) { _isPlaying.value = playing }
}
```

- [ ] **Step 4: Create `fragment_playback.xml`**

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="32dp">

    <Button android:id="@+id/btnPlayPause"
        android:layout_width="120dp" android:layout_height="120dp"
        android:text="Play" android:textSize="18sp"
        android:layout_marginBottom="48dp" />

    <CheckBox android:id="@+id/cbGuitar"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:text="Guitar" android:checked="true"
        android:layout_marginBottom="16dp" />

    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:text="Beat Style" android:textSize="16sp" android:layout_marginBottom="8dp" />

    <RadioGroup android:id="@+id/rgBeatStyle"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:orientation="horizontal" android:layout_marginBottom="48dp">
        <RadioButton android:id="@+id/rbBasic" android:layout_width="wrap_content"
            android:layout_height="wrap_content" android:text="Basic" android:checked="true" android:tag="BASIC" />
        <RadioButton android:id="@+id/rbRock" android:layout_width="wrap_content"
            android:layout_height="wrap_content" android:text="Rock" android:tag="ROCK" />
        <RadioButton android:id="@+id/rbJazz" android:layout_width="wrap_content"
            android:layout_height="wrap_content" android:text="Jazz" android:tag="JAZZ" />
    </RadioGroup>

    <Button android:id="@+id/btnRetry"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:text="Try Again"
        style="@style/Widget.MaterialComponents.Button.OutlinedButton" />
</LinearLayout>
```

- [ ] **Step 5: Create `PlaybackFragment.kt`**

```kotlin
package com.tunemate.presentation.playback

import android.media.MediaPlayer
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.findNavController
import com.tunemate.databinding.FragmentPlaybackBinding
import com.tunemate.domain.model.BeatStyle
import com.tunemate.domain.usecase.RecordAudioUseCase
import kotlinx.coroutines.launch
import org.koin.android.ext.android.inject
import org.koin.androidx.viewmodel.ext.android.viewModel

class PlaybackFragment : Fragment() {

    private var _binding: FragmentPlaybackBinding? = null
    private val binding get() = _binding!!
    private val viewModel: PlaybackViewModel by viewModel()
    private val recordUseCase: RecordAudioUseCase by inject()
    private var player: MediaPlayer? = null

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentPlaybackBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        binding.btnPlayPause.setOnClickListener {
            if (viewModel.isPlaying.value) pausePlayback() else startPlayback()
        }

        binding.cbGuitar.setOnCheckedChangeListener { _, _ -> viewModel.toggleGuitar() }

        binding.rgBeatStyle.setOnCheckedChangeListener { group, checkedId ->
            val tag = group.findViewById<View>(checkedId).tag as String
            viewModel.setBeatStyle(BeatStyle.valueOf(tag))
        }

        binding.btnRetry.setOnClickListener {
            findNavController().navigate(PlaybackFragmentDirections.actionPlaybackRetry())
        }

        viewLifecycleOwner.lifecycleScope.launch {
            viewModel.isPlaying.collect { playing ->
                binding.btnPlayPause.text = if (playing) "Pause" else "Play"
            }
        }
    }

    private fun startPlayback() {
        val file = recordUseCase.outputFile()
        if (!file.exists()) return
        player = MediaPlayer().apply {
            setDataSource(file.absolutePath)
            setOnPreparedListener { start(); viewModel.setPlaying(true) }
            setOnCompletionListener { viewModel.setPlaying(false) }
            prepareAsync()
        }
    }

    private fun pausePlayback() {
        player?.pause()
        viewModel.setPlaying(false)
    }

    override fun onDestroyView() {
        player?.release()
        player = null
        _binding = null
        super.onDestroyView()
    }
}
```

- [ ] **Step 6: Run test to confirm PASS**

```bash
./gradlew test --tests "com.tunemate.presentation.playback.PlaybackViewModelTest"
```
Expected: 4 tests passed

- [ ] **Step 7: Commit**

```bash
git add android/app/src/main/java/com/tunemate/presentation/playback/
git add android/app/src/main/res/layout/fragment_playback.xml
git add android/app/src/test/java/com/tunemate/presentation/playback/
git commit -m "feat: PlaybackFragment — play/pause, guitar toggle, beat style selection"
```

---

### Task 19: End-to-End Smoke Test

- [ ] **Step 1: Start the Flask backend**

```bash
cd backend && python app.py
```

- [ ] **Step 2: Update BASE_URL in AppModule.kt for physical device (if needed)**

For a physical device on the same WiFi, replace `10.0.2.2` with your machine's local IP:
```kotlin
private const val BASE_URL = "http://192.168.x.x:5000/api/"
```

- [ ] **Step 3: Run the app on emulator or device**

Android Studio → Run (Shift+F10)

- [ ] **Step 4: Walk through the full flow**

1. Home screen loads with duration radio buttons and Record button
2. Tap "Record" → Recording screen appears, recording starts
3. Tap "Stop" → Analyze button enables
4. Tap "Analyze" → spinner shows, then Results screen appears with Key / BPM / Chords
5. Tap "Play with Beat & Guitar" → Playback screen
6. Tap "Play" → audio plays back
7. Tap "Try Again" → returns to Recording screen

- [ ] **Step 5: Commit final tag**

```bash
git add .
git commit -m "feat: TuneMate MVP complete — end-to-end recording, analysis, and playback"
```

---

## Summary

| Phase | Tasks | Deliverable |
|---|---|---|
| Backend | 1–6 | Flask API accepting audio uploads, returning key/BPM/chords |
| Android Models | 7–9 | Domain layer (entities, repository interface, use cases) |
| Android Data | 10–11 | Retrofit client, DTO mapper, repository implementation |
| Android DI | 12 | Koin wiring, Application class |
| Android Recording | 13 | AudioRecord → WAV file |
| Android UI | 14–18 | All 4 screens wired via Navigation Component |
| Integration | 19 | End-to-end smoke test |
