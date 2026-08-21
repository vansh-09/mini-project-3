import os
from pathlib import Path
from typing import List, Dict, Any

class DiagramAnnotator:
    """
    Draws visual callout boxes and highlight overlays on diagram frame images (Milestone M3.6).
    """
    def annotate_frame(
        self,
        image_path: str,
        bounding_boxes: List[Dict[str, int]],
        label: str = "Diagram Region",
        output_path: str = ""
    ) -> str:
        in_path = Path(image_path)
        if not in_path.is_file():
            return image_path

        out_path = Path(output_path) if output_path else in_path.parent / f"annotated_{in_path.name}"

        try:
            import cv2

            img = cv2.imread(str(in_path))
            if img is None:
                return image_path

            # Draw bounding boxes with primary accent color (Indigo/Cyan)
            color = (241, 102, 99) # BGR for #6366f1
            text_color = (255, 255, 255)

            for box in bounding_boxes:
                x, y, w, h = box["x"], box["y"], box["w"], box["h"]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)

                # Draw label badge background
                badge_w = min(220, w)
                cv2.rectangle(img, (x, max(0, y - 30)), (x + badge_w, y), color, -1)
                cv2.putText(
                    img,
                    label[:25],
                    (x + 5, max(15, y - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    text_color,
                    1,
                    cv2.LINE_AA
                )

            cv2.imwrite(str(out_path), img)
            return str(out_path)
        except ImportError:
            print("OpenCV missing for visual annotation; using original frame.")
            return str(in_path)
        except Exception as e:
            print(f"Annotation error on {image_path}: {e}")
            return str(in_path)
