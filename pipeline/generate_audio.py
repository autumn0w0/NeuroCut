from pathlib import Path
import subprocess
import wave


def generate_audio(script: dict, audio_dir: Path, total_duration: int) -> dict:
    audio_dir.mkdir(parents=True, exist_ok=True)
    voiceover_path = audio_dir / "voiceover.wav"
    tts_result = _write_windows_tts(script["narration"], voiceover_path, total_duration)
    if not tts_result:
        _write_silence_wav(voiceover_path, total_duration)
    actual_duration = _wav_duration(voiceover_path)
    return {
        "status": "created",
        "reason": "Created Windows TTS voiceover." if tts_result else "Windows TTS failed, created a silent timing track.",
        "voiceover_path": str(voiceover_path),
        "duration": round(actual_duration, 2),
        "target_duration": total_duration,
        "music_path": None,
    }


def _write_windows_tts(text: str, output_path: Path, target_duration: int) -> bool:
    text_path = output_path.with_suffix(".txt")
    script_path = output_path.with_suffix(".ps1")
    text_path.write_text(text, encoding="utf-8")
    script_path.write_text(
        """
param(
  [string]$TextPath,
  [string]$OutputPath,
  [int]$Rate
)
Add-Type -AssemblyName System.Speech
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speaker.Rate = $Rate
$speaker.Volume = 100
$speaker.SetOutputToWaveFile($OutputPath)
$speaker.Speak((Get-Content -Raw -Encoding UTF8 $TextPath))
$speaker.Dispose()
""".strip(),
        encoding="utf-8",
    )
    try:
        for rate in (2, 4, 6, 8, 10):
            completed = _run_tts_script(script_path, text_path, output_path, rate)
            if completed.returncode != 0 or not output_path.exists():
                continue
            duration = _wav_duration(output_path)
            if duration <= target_duration + 2 or rate == 10:
                _fit_wav_to_duration(output_path, target_duration)
                return output_path.exists() and output_path.stat().st_size > 44
        return False
    except (OSError, subprocess.SubprocessError):
        return False


def _run_tts_script(script_path: Path, text_path: Path, output_path: Path, rate: int) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script_path),
            "-TextPath",
            str(text_path),
            "-OutputPath",
            str(output_path),
            "-Rate",
            str(rate),
        ],
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )


def _write_silence_wav(path: Path, duration_seconds: int) -> None:
    sample_rate = 44100
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        chunk = b"\x00\x00" * sample_rate
        for _ in range(max(1, duration_seconds)):
            wav.writeframes(chunk)


def _wav_duration(path: Path) -> float:
    if not path.exists():
        return 0.0
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / float(wav.getframerate())


def _fit_wav_to_duration(path: Path, duration_seconds: int) -> None:
    with wave.open(str(path), "rb") as source:
        params = source.getparams()
        frame_rate = source.getframerate()
        target_frames = max(1, duration_seconds) * frame_rate
        frames = source.readframes(source.getnframes())

    sample_width = params.sampwidth
    channels = params.nchannels
    bytes_per_frame = sample_width * channels
    target_bytes = target_frames * bytes_per_frame

    if len(frames) > target_bytes:
        frames = frames[:target_bytes]
    elif len(frames) < target_bytes:
        frames += b"\x00" * (target_bytes - len(frames))

    with wave.open(str(path), "wb") as fitted:
        fitted.setparams(params)
        fitted.writeframes(frames)
