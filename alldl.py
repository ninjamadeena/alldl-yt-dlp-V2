#!/usr/bin/env python3
import os
import subprocess
import traceback
import shutil
import time
import threading
import itertools
import sys

# ── ASCII ART ──
def print_ascii_title():
    print(r"""
 █████╗ ██╗     ██╗     ██████╗ ██╗
██╔══██╗██║     ██║     ██╔══██╗██║
███████║██║     ██║     ██║  ██║██║
██╔══██║██║     ██║     ██║  ██║██║
██║  ██║███████╗███████╗██████╔╝███████╗
╚═╝  ╚═╝╚══════╝╚══════╝╚═════╝ ╚══════╝
    ALLDL  v1.8.5 by ninjamadeena
    """)

# ── ตัวหมุนขณะเช็คโปรแกรม ──
def spinner_animation(stop_event, label):
    spinner = itertools.cycle(['/', '-', '\\', '|'])
    while not stop_event.is_set():
        sys.stdout.write(f"\r⏳ กำลังตรวจสอบ: {label} {next(spinner)} ")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r")

# ── ตรวจสอบโปรแกรมที่จำเป็น ──
def check_requirements():
    print_ascii_title()
    required_programs = ["python", "yt-dlp", "ffmpeg"]
    missing = []

    print("🔍 ตรวจสอบโปรแกรมที่จำเป็น...\n")
    for prog in required_programs:
        stop_event = threading.Event()
        t = threading.Thread(target=spinner_animation, args=(stop_event, prog))
        t.start()
        time.sleep(1.2)
        exists = shutil.which(prog) is not None
        stop_event.set()
        t.join()

        if exists:
            print(f"✅ พบโปรแกรม: {prog}")
        else:
            print(f"❌ ไม่พบโปรแกรม: {prog}")
            missing.append(prog)

    if missing:
        print("\n🚫 ขาดโปรแกรมที่จำเป็น:")
        for m in missing:
            print(f"   - {m}")
        print("\n📌 กรุณาติดตั้งก่อนใช้งานโปรแกรมนี้")
        exit()
    else:
       print("\n✅ โปรแกรมพร้อม\n")

# ── เลือกโฟลเดอร์ ──
def browse_folder(path):
    while True:
        print(f"\n📁 ── โฟลเดอร์ปัจจุบัน: {path}")
        try:
            folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            folders.sort()
        except Exception:
            print(f"\n❌ ไม่สามารถเข้าถึงโฟลเดอร์ได้:\n{traceback.format_exc()}")
            return None

        if not folders:
            print("📭 ไม่มีโฟลเดอร์ย่อยในที่นี้")

        for i, folder in enumerate(folders, 1):
            print(f"   {i}. 📂 {folder}")

        print("\n🔸 ตัวเลือก:")
        print("   [Y] ✅ ใช้โฟลเดอร์นี้")
        print("   [B] 🔙 กลับไปก่อนหน้า")
        print("   [N] ➕ สร้างโฟลเดอร์ใหม่")
        print("   [3] ❌ ยกเลิก")
        choice = input("\n❖ กรุณาเลือก (หมายเลขหรือคำสั่ง): ").strip().lower()

        if choice == 'y':
            return path
        elif choice == 'b':
            new_path = os.path.dirname(path)
            if new_path == path:
                print("🛑 ไม่สามารถย้อนกลับได้อีกแล้ว (Root directory)")
            else:
                path = new_path
        elif choice == 'n':
            name = input("📂 ➕ ตั้งชื่อโฟลเดอร์ใหม่: ").strip()
            if name:
                new_folder_path = os.path.join(path, name)
                try:
                    os.makedirs(new_folder_path, exist_ok=False)
                    print(f"✅ สร้างโฟลเดอร์แล้ว: {new_folder_path}")
                except FileExistsError:
                    print("🚫 โฟลเดอร์นี้มีอยู่แล้ว")
                except Exception as e:
                    print(f"❌ ไม่สามารถสร้างโฟลเดอร์ได้: {e}")
        elif choice == '3':
            return None
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(folders):
                path = os.path.join(path, folders[idx])
            else:
                print("🚫 หมายเลขไม่ถูกต้อง")
        else:
            print("🚫 คำสั่งไม่ถูกต้อง")

# ── รูปแบบ ──
def choose_format():
    print("\n🎛️ ── เลือกรูปแบบการดาวน์โหลด ──")
    options = {"1": ("🎬 วิดีโอ", "video"), "2": ("🎵 เสียง", "audio"), "3": ("❌ ยกเลิก", "cancel")}
    for key, (label, _) in options.items():
        print(f"   {key}. {label}")
    while True:
        choice = input("\n❖ กรุณาเลือกหมายเลข: ").strip()
        if choice in options:
            if options[choice][1] == "cancel":
                return None
            return options[choice][1]
        print("🚫 ตัวเลือกไม่ถูกต้อง กรุณาลองใหม่")

# ── นามสกุล ──
def choose_extension(mode):
    print(f"\n🧩 ── เลือกนามสกุลไฟล์ {'🎬 วิดีโอ' if mode == 'video' else '🎵 เสียง'} ──")
    valid_extensions = {
        "video": {"1": "mp4", "2": "webm", "3": "mkv", "4": "flv", "5": "3gp"},
        "audio": {"1": "mp3", "2": "m4a", "3": "opus", "4": "wav", "5": "aac", "6": "vorbis", "7": "flac"}
    }
    options = valid_extensions[mode]
    for key, ext in options.items():
        print(f"   {key}. .{ext}")
    print("   0. ❌ ยกเลิก")
    while True:
        choice = input("\n❖ เลือกหมายเลข: ").strip()
        if choice == "0":
            return None
        if choice in options:
            return options[choice]
        print("🚫 ตัวเลือกไม่ถูกต้อง")

# ── คุณภาพเสียง ──
def choose_audio_quality():
    print("\n🎚️ ── เลือกคุณภาพเสียง (Bitrate) ──")
    options = {"1": "64", "2": "128", "3": "192", "4": "320", "5": "ยกเลิก"}
    for k, v in options.items():
        print(f"   {k}. {v} kbps")
    while True:
        choice = input("\n❖ เลือกหมายเลข: ").strip()
        if choice in options:
            if options[choice] == "ยกเลิก":
                return None
            return options[choice]
        print("🚫 ตัวเลือกไม่ถูกต้อง")

# ── ความละเอียด ──
def choose_multiple_resolutions():
    print("\n🖼️ ── เลือกความละเอียดวิดีโอ (เลือกได้หลายค่า, คั่นด้วย ,) ──")
    options = {
        "1": ("2160p (4K)", 2160), "2": ("1440p", 1440), "3": ("1080p", 1080),
        "4": ("720p", 720), "5": ("480p", 480), "6": ("360p", 360),
        "7": ("อัตโนมัติ", None), "8": ("❌ ยกเลิก", "cancel")
    }
    for key, (label, _) in options.items():
        print(f"   {key}. {label}")
    while True:
        raw = input("\n❖ เลือกหมายเลข (ตัวอย่าง: 2,3,6): ").strip()
        if "8" in raw:
            return None
        try:
            return [options[x][1] for x in raw.split(",") if x in options]
        except:
            print("🚫 รูปแบบไม่ถูกต้อง")

# ── ป้อนลิงก์ ──
def collect_urls():
    print("\n📥 ── ใส่ลิงก์วิดีโอ (พิมพ์ 'done' เพื่อจบรายการ) ──")
    urls = []
    while True:
        u = input("🔗 ➤ ").strip()
        if u.lower() == "done":
            break
        elif u:
            urls.append(u)
    return urls

# ── ดึงชื่อวิดีโอ ──
def get_title(url):
    try:
        result = subprocess.run(
            ["yt-dlp", "--print", "%(title)s", "--yes-playlist", "--skip-download", url],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception:
        return None

# ── เริ่มต้น ──
check_requirements()
print("🎬 ระบบดาวน์โหลดวิดีโอ/เสียงจากลิงก์เดียวหรือหลายลิงก์")

mode_select = input("\n📂 เลือกโหมด:\n   1. 🔗 ลิงก์เดียว\n   2. 📑 หลายลิงก์\n   3. ❌ ยกเลิก\n❖ เลือก: ").strip()
if mode_select == '1':
    link = input("🔗 ➤ ใส่ลิงก์วิดีโอหรือเพลย์ลิสต์: ").strip()
    urls = [link]
elif mode_select == '2':
    urls = collect_urls()
elif mode_select == '3':
    print("❎ ยกเลิกแล้ว")
    exit()
else:
    print("🚫 คำสั่งไม่ถูกต้อง")
    exit()

if not urls:
    print("🚫 ไม่พบลิงก์ใดๆ")
    exit()

print("\n📋 ── กำลังตรวจสอบลิ้ง กรุณารอสักครู่  ──")
for url in urls:
    title = get_title(url)
    if title:
        print(f"✔️ {title}")
    else:
        print(f"❌ ตรวจสอบลิ้งไม่สำเร็จ: {url}")
        exit()

mode = choose_format()
if not mode:
    print("❎ ยกเลิก")
    exit()

ext = choose_extension(mode)
if not ext:
    print("❎ ยกเลิก")
    exit()

audio_quality = choose_audio_quality() if mode == "audio" else None
if mode == "audio" and not audio_quality:
    print("❎ ยกเลิก")
    exit()

resolutions = choose_multiple_resolutions() if mode == "video" else None
if mode == "video" and resolutions is None:
    print("❎ ยกเลิก")
    exit()

save_path = browse_folder("/storage/emulated/0")
if not save_path:
    print("❎ ยกเลิก")
    exit()

has_error = False
for url in urls:
    print(f"\n🔗 เริ่มดาวน์โหลดจาก: {url}")
    cmds = []

    if mode == "audio":
        cmds.append([
            "yt-dlp", "-f", "bestaudio",
            "--extract-audio", "--audio-format", ext,
            "--audio-quality", audio_quality + "k",
            "--embed-thumbnail", "--add-metadata",
            "--yes-playlist",
            "-o", f"{save_path}/%(title)s.{ext}",
            url
        ])
    else:
        if None in resolutions:
            cmds.append([
                "yt-dlp",
                "-f", f"bestvideo[ext={ext}]+bestaudio[ext=m4a]/best",
                "--merge-output-format", ext,
                "--yes-playlist",
                "-o", f"{save_path}/%(title)s.{ext}",
                url
            ])
        else:
            for r in resolutions:
                cmds.append([
                    "yt-dlp",
                    "-f", f"bestvideo[ext={ext}][height<={r}]+bestaudio[ext=m4a]/best",
                    "--merge-output-format", ext,
                    "--yes-playlist",
                    "-o", f"{save_path}/%(title)s_{r}p.{ext}",
                    url
                ])

    for cmd in cmds:
        print("\n⚙️ คำสั่งที่จะรัน:\n" + " ".join(cmd))
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                print(line, end='')
            process.wait()
            if process.returncode == 0:
                print("\n✅ ดาวน์โหลดสำเร็จ\n")
            else:
                print(f"\n❌ ผิดพลาด ({process.returncode})")
                has_error = True
        except Exception:
            print(f"\n❌ ERROR:\n{traceback.format_exc()}")
            has_error = True

if has_error:
    print("\n🚫 ดาวน์โหลดไม่สำเร็จ")
else:
    print("\n🏁 เสร็จสิ้นทุกงานเรียบร้อย!")
