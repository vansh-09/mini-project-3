from typing import List, Dict, Any

class EventGrouper:
    """
    Groups consecutive diagram detections into distinct diagram events with start and end timestamps.
    """
    def __init__(self, max_gap_seconds: float = 3.0):
        self.max_gap_seconds = max_gap_seconds

    def group_detections(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Input: List of frame detection items:
          [ { "frame_path": "...", "timestamp": 12.0, "is_diagram": True, "diagram_type": "graph" }, ... ]
        Output: Grouped diagram events:
          [ { "event_id": "evt_001", "start_time": 12.0, "end_time": 25.0, "timestamp": 12.0, "image_path": "...", "diagram_type": "graph" }, ... ]
        """
        diagram_frames = [d for d in detections if d.get("is_diagram", False)]
        if not diagram_frames:
            return []

        # Sort by timestamp
        diagram_frames.sort(key=lambda x: x["timestamp"])

        grouped_events = []
        current_group = [diagram_frames[0]]

        for frame in diagram_frames[1:]:
            prev_frame = current_group[-1]
            gap = frame["timestamp"] - prev_frame["timestamp"]

            if gap <= self.max_gap_seconds:
                current_group.append(frame)
            else:
                grouped_events.append(self._create_event(len(grouped_events) + 1, current_group))
                current_group = [frame]

        if current_group:
            grouped_events.append(self._create_event(len(grouped_events) + 1, current_group))

        return grouped_events

    def _create_event(self, index: int, group: List[Dict[str, Any]]) -> Dict[str, Any]:
        start_time = group[0]["timestamp"]
        end_time = group[-1]["timestamp"]
        # Representative frame selected from middle of group
        mid_frame = group[len(group) // 2]

        return {
            "event_id": f"ad_evt_{index:03d}",
            "start_time": start_time,
            "end_time": end_time,
            "timestamp": start_time,
            "image": mid_frame["frame_path"],
            "diagram_type": mid_frame.get("diagram_type", "diagram")
        }
