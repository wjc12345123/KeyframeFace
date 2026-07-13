import csv
import json
import os


ARKIT_KEYS = [
    "EyeBlinkLeft", "EyeLookDownLeft", "EyeLookInLeft", "EyeLookOutLeft", "EyeLookUpLeft",
    "EyeSquintLeft", "EyeWideLeft", "EyeBlinkRight", "EyeLookDownRight", "EyeLookInRight",
    "EyeLookOutRight", "EyeLookUpRight", "EyeSquintRight", "EyeWideRight", "JawForward",
    "JawRight", "JawLeft", "JawOpen", "MouthClose", "MouthFunnel", "MouthPucker",
    "MouthRight", "MouthLeft", "MouthSmileLeft", "MouthSmileRight", "MouthFrownLeft",
    "MouthFrownRight", "MouthDimpleLeft", "MouthDimpleRight", "MouthStretchLeft",
    "MouthStretchRight", "MouthRollLower", "MouthRollUpper", "MouthShrugLower",
    "MouthShrugUpper", "MouthPressLeft", "MouthPressRight", "MouthLowerDownLeft",
    "MouthLowerDownRight", "MouthUpperUpLeft", "MouthUpperUpRight", "BrowDownLeft",
    "BrowDownRight", "BrowInnerUp", "BrowOuterUpLeft", "BrowOuterUpRight", "CheekPuff",
    "CheekSquintLeft", "CheekSquintRight", "NoseSneerLeft", "NoseSneerRight", "TongueOut",
    "HeadYaw", "HeadPitch", "HeadRoll", "LeftEyeYaw", "LeftEyePitch", "LeftEyeRoll",
    "RightEyeYaw", "RightEyePitch", "RightEyeRoll",
]


def extract_json(text):
    """Extract the last balanced JSON object from an MS-SWIFT response."""
    end = text.rfind("}")
    if end < 0:
        return None
    depth = 0
    for start in range(end, -1, -1):
        if text[start] == "}":
            depth += 1
        elif text[start] == "{":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start : end + 1])
                except json.JSONDecodeError:
                    return None
    return None


def extract_arkit(record):
    response = record.get("response", "")
    if not response:
        for message in reversed(record.get("messages", [])):
            if message.get("role") == "assistant":
                response = message.get("content", "")
                break
    data = extract_json(response)
    if not isinstance(data, dict):
        return None
    if all(key in data for key in ARKIT_KEYS):
        return data
    for name, value in data.items():
        if name.lower().startswith("keyframe_") and isinstance(value, dict):
            return value
    return None


def convert(input_path, output_path):
    fields = ["Timecode", "BlendshapeCount", *ARKIT_KEYS]
    with open(input_path, "r", encoding="utf-8") as source, open(
        output_path, "w", newline="", encoding="utf-8"
    ) as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        frame = 0
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            params = extract_arkit(json.loads(line))
            if params is None:
                print(f"[Warning] Line {line_number}: cannot parse ARKit parameters")
                continue
            row = {"Timecode": f"00:00:{frame:02d}:00.000", "BlendshapeCount": 61}
            row.update({key: params.get(key, 0.0) for key in ARKIT_KEYS})
            writer.writerow(row)
            frame += 1
    print(f"Done. Output saved to: {output_path}")


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    convert(
        os.path.join(root, "example_result.jsonl"),
        os.path.join(root, "example_result.csv"),
    )

