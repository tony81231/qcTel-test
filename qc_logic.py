import os

def evaluate_image(image_path):
    report = f"""
📊 Dummy HDR QC Report for {os.path.basename(image_path)}:
- Exposure: Good
- Contrast: Fair
- Highlight Clipping: None
- Overall Score: Good
"""
    return report
