from pathlib import Path
import subprocess
import wave


def generate_audio(script: dict, audio_dir: Path, total_duration: int) -> dict:
    audio_dir.mkdir(parents=True, exist_ok=True)
    voiceover_path = audio_dir / "voiceover.wav"
    tts_result = _write_windows_tts(script["narration"], voiceover_path)
    if not tts_result:
        _write_silence_wav(voiceover_path, total_duration)
    return {
        "status": "created",
        "reason": "Created Windows TTS voiceover." if tts_result else "Windows TTS failed, created a silent timing track.",
        "voiceover_path": str(voiceover_path),
        "music_path": None,
    }


def _write_windows_tts(text: str, output_path: Path) -> bool:
    text_path = output_path.with_suffix(".txt")
    script_path = output_path.with_suffix(".ps1")
    text_path.write_text(text, encoding="utf-8")
    script_path.write_text(
        """
param(
  [string]$TextPath,
  [string]$OutputPath
)
Add-Type -AssemblyName System.Speech
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speaker.Rate = -2
$speaker.Volume = 100
$speaker.SetOutputToWaveFile($OutputPath)
$speaker.Speak((Get-Content -Raw -Encoding UTF8 $TextPath))
$speaker.Dispose()
""".strip(),
        encoding="utf-8",
    )
    try:
        completed = subprocess.run(
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
            ],
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        return completed.returncode == 0 and output_path.exists() and output_path.stat().st_size > 44
    except (OSError, subprocess.SubprocessError):
        return False


def _write_silence_wav(path: Path, duration_seconds: int) -> None:
    sample_rate = 44100
    frame_count = max(1, duration_seconds) * sample_rate
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        chunk = b"\x00\x00" * sample_rate
        for _ in range(max(1, duration_seconds)):
            wav.writeframes(chunk)
