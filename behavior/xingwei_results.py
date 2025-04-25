import json
from collections import defaultdict
import numpy as np
# import os

class BehaviorFeatureExtractor:
    def __init__(self, json_path=None):
        """
        初始化行为特征提取器

        :param json_path: str,JSON文件
        """
        self.data = None
        if json_path:
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            self.extract_from_operation_json(json_data)

    def set_data(self, data):
        """
        手动设置提取后的特征数据
        :param data: dict
        """
        self.data = data

    def extract_from_operation_json(self, json_data, target_id=9):
        record = next((item for item in json_data if item.get("id") == target_id), None)
        if not record:
            raise ValueError(f"未找到ID为 {target_id} 的记录")

        operation_data = json.loads(record["operation"])
        stats = operation_data.get("statisticsData", {})
        events = operation_data.get("eventData", [])

        gametime = stats.get("gameTime", 0)
        hit = stats.get("hitBlockCount", 0)
        total = stats.get("blockCount", 2)
        avoid_proba = (1 - hit / total) * 100

        get_star = stats.get("getStarCount", 0)
        star_count = stats.get("starCount", 1)
        getstarrate = get_star / star_count * 100

        tap = stats.get("tapCount", 0)
        left = stats.get("leftTapCount", 0)
        right = stats.get("rightTapCount", 0)
        hands_imbalance = (left - right) / (left + right) * 100 if (left + right) else 0

        # --- 事件时间段稳定性 ---
        interval = 30
        time_bins = defaultdict(lambda: {"hits": 0, "block": 0, "getstar": 0, "startotal": 0})

        for event in events:
            t = float(event["tm"])
            bin_index = int(t // interval)
            tp = event["ty"]
            if tp == "sb": time_bins[bin_index]["block"] += 1
            elif tp == "hb": time_bins[bin_index]["hits"] += 1
            elif tp == "hs": time_bins[bin_index]["getstar"] += 1
            elif tp == "ss": time_bins[bin_index]["startotal"] += 1

        avoid_probs, star_probs = [], []
        for bin_data in time_bins.values():
            block, hits = bin_data["block"], bin_data["hits"]
            stars, star_total = bin_data["getstar"], bin_data["startotal"]
            if block: avoid_probs.append((1 - hits / block) * 100)
            if star_total: star_probs.append(min(stars, star_total) / star_total * 100)

        def compute_stability(vals):
            if not vals: return 0
            mean = sum(vals) / len(vals)
            std = (sum((x - mean) ** 2 for x in vals) / len(vals)) ** 0.5
            return 1 - (std / mean) if mean != 0 else 0

        avoid_stability = compute_stability(avoid_probs)
        star_stability = compute_stability(star_probs)

        # --- 左右手准确率 ---
        left_lanes = {1, 2, 3}
        right_lanes = {4, 5, 6}
        counts = {
            "left": {"ss": 0, "hb": 0, "sb": 0, "hs": 0},
            "right": {"ss": 0, "hb": 0, "sb": 0, "hs": 0}
        }

        for e in events:
            ty = e["ty"]
            st = e["st"]
            if st in left_lanes:
                side = "left"
            elif st in right_lanes:
                side = "right"
            else:
                continue
            if ty in ["ss", "hb", "sb", "hs"]:
                counts[side][ty] += 1

        def calc_rate(success, total):
            return round(success / total, 3) if total > 0 else 0

        left_accuracy = (counts["left"]["hs"] + (counts["left"]["sb"] - counts["left"]["hb"])) / (counts["left"]["sb"] + counts["left"]["ss"]) * 100 if (counts["left"]["sb"] + counts["left"]["ss"]) else 0
        right_accuracy = (counts["right"]["hs"] + (counts["right"]["sb"] - counts["right"]["hb"])) / (counts["right"]["sb"] + counts["right"]["ss"]) * 100 if (counts["right"]["sb"] + counts["right"]["ss"]) else 0

        accuracy = (get_star + (total - hit)) / (total + star_count) * 100 if (total + star_count) else 0

        self.data = {
            "Game Time": gametime,
            "hitBlock": hit,
            "Avoid Probability": round(avoid_proba, 2),
            "Avoid Stability": round(avoid_stability * 100, 2),
            "GetStar": get_star,
            "Get Star Rate": round(getstarrate, 2),
            "Star Stability": round(star_stability * 100, 2),
            "Hand Imbalance(left-right%)": round(hands_imbalance, 2),
            "Hands Balance": round(100 - abs(hands_imbalance), 2),
            "Left Accuracy": round(left_accuracy, 2),
            "Right Accuracy": round(right_accuracy, 2),
            "Accuracy": round(accuracy, 2),
            "action tendency(get-avoid)": round((get_star - (total - hit)) / (get_star + (total - hit)), 3) if (get_star + (total - hit)) else 0
        }

    def compute_radar_score(self, values, max_score=100):
        num_vars = len(values)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values = values + values[:1]
        angles = angles + angles[:1]
        x = [v * np.cos(a) for v, a in zip(values, angles)]
        y = [v * np.sin(a) for v, a in zip(values, angles)]
        area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

        full_values = [max_score] * num_vars
        full_values = full_values + full_values[:1]
        fx = [v * np.cos(a) for v, a in zip(full_values, angles)]
        fy = [v * np.sin(a) for v, a in zip(full_values, angles)]
        max_area = 0.5 * np.abs(np.dot(fx, np.roll(fy, 1)) - np.dot(fy, np.roll(fx, 1)))

        final_score = area / max_area * 100
        return round(final_score, 2)

    def extract_features_and_score(self):
        if not self.data:
            raise ValueError("请先设置数据或加载JSON文件。")

        # keys = self.data
        selected_keys = [
            "Avoid Probability",
            "Avoid Stability",
            "Get Star Rate",
            "Star Stability",
            "Hands Balance",
            "Accuracy"
        ]
        feature_values = [self.data[k] for k in selected_keys if k in self.data]
        radar_score = self.compute_radar_score(feature_values)

        return {
            'features': self.data,
            'radar_score': radar_score
        }

    # def save_result_to_csv(self, result, csv_path='radar_score_results.csv'):
    #     fieldnames = list(result['features'].keys()) + ['Radar Score']
    #     file_exists = os.path.isfile(csv_path)
    #     with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
    #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #         if not file_exists:
    #             writer.writeheader()
    #         row = result['features']
    #         row['Radar Score'] = result['radar_score']
    #         writer.writerow(row)

if __name__ == "__main__":
    example_json_path = 'operation_tb(5).json'
    extractor = BehaviorFeatureExtractor(example_json_path)
    result = extractor.extract_features_and_score()
    print("行为能力评分结果:")
    print(result)
    # extractor.save_result_to_csv(result)
