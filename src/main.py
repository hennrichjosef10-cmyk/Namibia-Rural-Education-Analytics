class LearningAsset:
    def __init__(self, title, file_size_kb):
        self._title = title
        self._file_size_kb = file_size_kb

    def calculate_bandwidth_mb(self):
        return self._file_size_kb / 1024.0


class VideoLesson(LearningAsset):
    def __init__(self, title, file_size_kb, duration_sec):
        super().__init__(title, file_size_kb)
        self._duration_sec = duration_sec

    def calculate_bandwidth_mb(self):
        base_mb = super().calculate_bandwidth_mb()
        streaming_overhead = (self._duration_sec / 60.0) * 0.1
        return base_mb + streaming_overhead


class InteractiveQuiz(LearningAsset):
    def __init__(self, title, file_size_kb, question_count):
        super().__init__(title, file_size_kb)
        self._question_count = question_count

    def calculate_bandwidth_mb(self):
        base_mb = super().calculate_bandwidth_mb()
        quiz_data_mb = (self._question_count * 5) / 1024.0
        return base_mb + quiz_data_mb


class ServerNode:
    def __init__(self, node_id, region, assets=None):
        self._node_id = node_id
        self._region = region
        self._assets = assets if assets is not None else []

    def addAsset(self, asset):
        self._assets.append(asset)

    def optimize_video_assets(self):
        for asset in self._assets:
            if isinstance(asset, VideoLesson):
                asset._file_size_kb *= 0.85

    def get_avg_bandwidth(self):
        if not self._assets:
            return 0.0
        total_bandwidth = sum(asset.calculate_bandwidth_mb() for asset in self._assets)
        return total_bandwidth / len(self._assets)

    def search_asset_by_title(self, title):
        for asset in self._assets:
            if asset._title.lower() == title.lower():
                return asset
        return None


class SchoolHub:
    def __init__(self, school_name, server=None):
        self._school_name = school_name
        self._server = server if server is not None else ServerNode(101, "KHOMAS")

    def generate_analytics_report(self):
        print(f"--- {self._school_name} Digital Resource Analytics ---")
        print(f"Region: {self._server._region}")
        print(f"Average Bandwidth Footprint: {self._server.get_avg_bandwidth():.2f} MB")

    def optimize_hub_storage(self):
        self._server.optimize_video_assets()
        print(f"[{self._school_name}] Video compression applied successfully.")

    def locate_asset_status(self, asset_title):
        result = self._server.search_asset_by_title(asset_title)
        if result:
            print(f"Found '{result._title}' - Size: {result._file_size_kb:.2f} KB | Bandwidth: {result.calculate_bandwidth_mb():.2f} MB")
        else:
            print(f"Asset '{asset_title}' not found on server node.")


if __name__ == "__main__":
    server_node = ServerNode(node_id=101, region="KHOMAS")
    hub = SchoolHub(school_name="Augustineum Secondary School", server=server_node)

    video_1 = VideoLesson("Biology Intro", 50000.0, 600)
    quiz_1 = InteractiveQuiz("Biology Quiz 1", 1200.0, 15)
    video_2 = VideoLesson("Math Basics", 80000.0, 1200)

    hub._server.addAsset(video_1)
    hub._server.addAsset(quiz_1)
    hub._server.addAsset(video_2)

    hub.generate_analytics_report()

    print("\n--- Testing Polymorphism ---")
    print(f" - {video_1._title} Bandwidth: {video_1.calculate_bandwidth_mb():.2f} MB")
    print(f" - {quiz_1._title} Bandwidth: {quiz_1.calculate_bandwidth_mb():.2f} MB")

    print("\n--- Testing Type Checking & Optimization ---")
    hub.optimize_hub_storage()

    print("\n--- Testing Search Algorithm ---")
    hub.locate_asset_status("Biology Quiz 1")

    print("\n--- Final Analytics Report ---")
    hub.generate_analytics_report()
