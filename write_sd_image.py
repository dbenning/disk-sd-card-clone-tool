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

def write_img_to_sd(img_path, disk_id):
    unmount_disk(disk_id)
    print(f"📝 Writing {img_path} to /dev/{disk_id}...")
    subprocess.run(["sudo", "dd", f"if={img_path}", f"of=/dev/r{disk_id}", "bs=1m", "status=progress"], check=True)
    print("✅ Write complete.")

def main():
    print("=== Write SD Card Image to Drive ===")

    img_file = input("Enter the path to the image file (e.g., ~/Desktop/sd_backup.img): ").strip()
    img_file = os.path.expanduser(img_file)

    if not os.path.exists(img_file):
        print(f"❌ File not found: {img_file}")
        sys.exit(1)

    disks = get_all_disks()
    if not disks:
        sys.exit(1)

    dst_disk = choose_disk(disks, "Choose the DESTINATION disk to write the image to")
    confirm = input(f"\n⚠️ WARNING: This will ERASE /dev/{dst_disk}. Type 'yes' to confirm: ").strip().lower()
    if confirm != "yes":
        print("❌ Operation cancelled.")
        sys.exit(0)

    write_img_to_sd(img_file, dst_disk)
    print(f"\n🎉 Image successfully written to: /dev/{dst_disk}")

if __name__ == "__main__":
    main()
