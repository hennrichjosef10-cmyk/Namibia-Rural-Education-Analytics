# Namibian Rural Education & Digital Resource Analytics Platform

## System Overview
Rural Namibian secondary schools often face slow or unreliable internet access. To solve this problem, each school uses an offline local server to store and share educational content with students without using the internet.

This platform models a **SchoolHub** managing an offline **ServerNode** with stored **LearningAsset** files (`VideoLesson` and `InteractiveQuiz`).

## OOP Implementation Details
* **Composition:** `SchoolHub` manages a `ServerNode` instance.
* **Aggregation:** `ServerNode` stores a list of independent `LearningAsset` objects.
* **Inheritance:** `VideoLesson` and `InteractiveQuiz` extend `LearningAsset`.
* **Polymorphism:** `calculate_bandwidth_mb()` calculates file bandwidth overhead dynamically per subclass.
* **Type Checking:** `optimize_video_assets()` uses `isinstance(asset, VideoLesson)` for compression.
* **Algorithms:** Average bandwidth computation (`get_avg_bandwidth()`) and linear search (`search_asset_by_title()`).

## Project Structure
```text
├── src/
│   └── main.py              # Main Python source code
├── .gitignore               # Ignored files configuration
└── README.md                # Project documentation
