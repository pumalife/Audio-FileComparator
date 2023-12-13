import json
import subprocess
import sys
from mutagen import File # for metadata function. test it out

def run_ffprobe(file_path):
    """Run ffprobe on the given file and return the JSON output."""
    command = [
        "ffprobe", "-v", "level+warning", "-show_format", "-show_streams",
        "-of", "json", "-show_data_hash", "SHA256", "-show_optional_fields", "1",
        "-show_packets", "-i", file_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

def compare_audio_files(file1, file2):
    """Compare two audio files and print differences."""
    data1 = run_ffprobe(file1)
    data2 = run_ffprobe(file2)

    # Compare streams
    print("Differences in streams:")
    for stream1, stream2 in zip(data1.get("streams", []), data2.get("streams", [])):
        for key in stream1:
            if stream1[key] != stream2.get(key):
                print(f"Stream {key}: {stream1[key]} != {stream2.get(key)}")

    # Compare format
    print("\nDifferences in format:")
    format1 = data1.get("format", {})
    format2 = data2.get("format", {})
    for key in format1:
        if format1[key] != format2.get(key):
            print(f"Format {key}: {format1[key]} != {format2.get(key)}")

    # Compare packets
    print("\nDifferences in packets:")
    for packet1, packet2 in zip(data1.get("packets", []), data2.get("packets", [])):
        for key in packet1:
            if packet1[key] != packet2.get(key):
                print(f"Packet {key}: {packet1[key]} != {packet2.get(key)}")

    # test it out Compare extended metadata
    compare_metadata(file1, file2)

# test it out
def compare_metadata(file1, file2):
    """Compare the metadata of two audio files."""
    metadata1 = File(file1, easy=True)
    metadata2 = File(file2, easy=True)

    keys = set(metadata1.keys()).union(set(metadata2.keys()))
    print("\nDifferences in Metadata:")
    for key in keys:
        if metadata1.get(key) != metadata2.get(key):
            print(f"Metadata {key}: {metadata1.get(key)} != {metadata2.get(key)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_audio_files.py <file1> <file2>")
        sys.exit(1)

    compare_audio_files(sys.argv[1], sys.argv[2])
