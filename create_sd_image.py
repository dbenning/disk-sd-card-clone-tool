import os
import subprocess
import sys
import re

def get_all_disks():
    print("\n🔍 Scanning all connected drives...")
    result = subprocess.run(["diskutil", "list"], capture_output=True, text=True)
    output = result.stdout
    disk_headers = re.findall(r"(/dev/disk\d+)\s*\(.*?\):", output)

    disks = []

    for disk in set(disk_headers):  # Remove duplicates
        disk_id = disk.replace("/dev/", "")
        info = subprocess.run(["diskutil", "info", disk_id], capture_output=True, text=True).stdout
        size_match = re.search(r"Disk Size:\s+([\d.]+ \w+)", info)
        name_match = re.search(r"Volume Name:\s+(.+)", info)
        size = size_match.group(1) if size_match else "Unknown size"
        name = name_match.group(1).strip() if name_match else "No Name"
        disks.append((disk_id, f"{disk_id} — {name} — {size}"))

    if not disks:
        print("❌ No drives found.")
        return []

    return sorted(disks, key=lambda x: x[0])

def choose_disk(disks, prompt_text):
    print(f"\n{prompt_text}")
    for idx, (_, description) in enumerate(disks):
        print(f"  [{idx + 1}] {description}")
    while True:
        choice = input(f"Enter the number of your choice (1-{len(disks)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(disks):
            return disks[int(choice) - 1][0]
        else:
            print("❌ Invalid choice. Try again.")

def unmount_disk(disk_id):
    print(f"🔌 Unmounting /dev/{disk_id}...")
    subprocess.run(["diskutil", "unmountDisk", f"/dev/{disk_id}"], check=True)

def create_img_from_sd(disk_id, output_img):
    unmount_disk(disk_id)
    print(f"📦 Creating image from /dev/{disk_id} to {output_img}...")
    subprocess.run(["sudo", "dd", f"if=/dev/r{disk_id}", f"of={output_img}", "bs=1m", "status=progress"], check=True)
    print("✅ Image creation complete.")

def main():
    print("=== Create SD Card Image ===")

    disks = get_all_disks()
    if not disks:
        sys.exit(1)

    src_disk = choose_disk(disks, "Choose the SOURCE disk to create an image from")
    img_file = input("Enter path to save the image file (e.g., ~/Desktop/sd_backup.img): ").strip()
    img_file = os.path.expanduser(img_file)

    create_img_from_sd(src_disk, img_file)
    print(f"\n🎉 Image saved to: {img_file}")

if __name__ == "__main__":
    main()
