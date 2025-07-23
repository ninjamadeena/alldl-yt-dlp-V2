#!/bin/bash

set -e

GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
RESET="\033[0m"

echo -e "${YELLOW}🛠️ เริ่มติดตั้ง ALLDL...${RESET}"

# ----- Python3 -----
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}❌ ไม่พบ Python3${RESET}"
    echo -e "${YELLOW}📦 กำลังติดตั้ง Python3...${RESET}"
    if command -v pkg &>/dev/null; then
        pkg install -y python
    else
        sudo apt update && sudo apt install -y python3
    fi
else
    echo -e "${GREEN}✅ พบ Python3 แล้ว${RESET}"
fi

# ----- pip3 -----
if ! command -v pip3 &>/dev/null; then
    echo -e "${RED}❌ ไม่พบ pip3${RESET}"
    echo -e "${YELLOW}📦 กำลังติดตั้ง pip3...${RESET}"
    if command -v pkg &>/dev/null; then
        pkg install -y python-pip
    else
        sudo apt install -y python3-pip
    fi
else
    echo -e "${GREEN}✅ พบ pip3 แล้ว${RESET}"
fi

# ----- ffmpeg -----
if ! command -v ffmpeg &>/dev/null; then
    echo -e "${RED}❌ ไม่พบ ffmpeg${RESET}"
    echo -e "${YELLOW}📦 กำลังติดตั้ง ffmpeg...${RESET}"
    if command -v pkg &>/dev/null; then
        pkg install -y ffmpeg
    else
        sudo apt install -y ffmpeg
    fi
else
    echo -e "${GREEN}✅ พบ ffmpeg แล้ว${RESET}"
fi

# ----- yt-dlp -----
if ! command -v yt-dlp &>/dev/null; then
    echo -e "${RED}❌ ไม่พบ yt-dlp${RESET}"
    echo -e "${YELLOW}📦 กำลังติดตั้ง yt-dlp...${RESET}"
    pip3 install -U yt-dlp
else
    echo -e "${GREEN}✅ พบ yt-dlp แล้ว${RESET}"
fi

# ----- ตั้งค่าโปรแกรม -----
SCRIPT_NAME="alldl.py"
TARGET_BIN="$PREFIX/bin/alldl"

echo -e "${YELLOW}⚙️ ตั้งค่าไฟล์ $SCRIPT_NAME ให้รันได้...${RESET}"
chmod +x "$SCRIPT_NAME"
mv "$SCRIPT_NAME" "$TARGET_BIN"
echo -e "${GREEN}✅ตั้งค่าเรียบร้อยแล้ว${RESET}"
# ----- ตรวจสอบอีกครั้ง -----
echo -e "\n${YELLOW}🔍 ตรวจสอบความสมบูรณ์หลังติดตั้ง...${RESET}"

for cmd in python3 pip3 ffmpeg yt-dlp alldl; do
    if command -v "$cmd" &>/dev/null; then
        echo -e "${GREEN}✅ ตรวจพบ $cmd พร้อมใช้งาน${RESET}"
    else
        echo -e "${RED}❌ ไม่พบ $cmd กรุณาตรวจสอบการติดตั้งอีกครั้ง${RESET}"
    fi
done

# ----- จบ -----
echo -e "\n${GREEN}🎉 ติดตั้งเสร็จสมบูรณ์!${RESET}"
echo "📌 ใช้คำสั่ง: alldl เพื่อเริ่มใช้งาน"

# ลบโฟลเดอร์ติดตั้ง
rm -rf /data/data/com.termux/files
rm -rf ~/alldl-yt-dlp
