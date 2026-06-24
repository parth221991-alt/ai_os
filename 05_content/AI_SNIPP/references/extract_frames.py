"""Extract frames from local video files for Claude analysis."""
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def duration_s(vid: Path) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1:nokey=1", str(vid)]).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def extract(vid: Path, out: Path, every: float = 1.0):
    out.mkdir(parents=True, exist_ok=True)
    fdir = out / "frames"
    if fdir.exists():
        shutil.rmtree(fdir)
    fdir.mkdir()
    fps = 1.0 / every
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(vid),
         "-vf", f"fps={fps},scale=512:-2", "-q:v", "3", str(fdir / "f%03d.jpg")])
    frames = sorted(fdir.glob("f*.jpg"))
    index = [{"frame": i, "t": round(i * every, 2), "file": f"frames/{p.name}"}
             for i, p in enumerate(frames)]
    (out / "index.json").write_text(json.dumps(index, indent=2))
    print(f"  OK {len(frames)} frames -> {out}")
    return frames


def main():
    refs = Path(r"D:\AI_OS\05_content\AI_SNIPP\references")
    base = refs / "analysis"
    videos = sorted(refs.glob("*.mp4"))
    print(f"Found {len(videos)} videos\n")
    for i, vid in enumerate(videos, 1):
        dur = duration_s(vid)
        every = 1.0 if dur > 15 else 0.5
        print(f"[{i}/{len(videos)}] {vid.name[:40]}... ({dur:.1f}s)")
        out = base / f"v{i:02d}"
        extract(vid, out, every=every)
    print(f"\nDone. Frames in: {base}")



if __name__ == "__main__":
    main()
