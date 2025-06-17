#!/usr/bin/env python3
"""
中学生向け天気データ分析関数（標準ライブラリのみ使用版）
統計学習に適したデータ処理機能を提供
"""

import csv
import statistics
from collections import defaultdict
from typing import Dict, List, Tuple

class SimpleWeatherAnalyzer:
    """天気データ分析クラス（標準ライブラリのみ）"""
    
    def __init__(self, csv_file_path: str = "weather_data.csv"):
        """初期化"""
        self.data = []
        self.load_data(csv_file_path)
        
    def load_data(self, csv_file_path: str):
        """CSVデータを読み込み"""
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 数値型に変換
                row['temperature'] = float(row['temperature'])
                row['precipitation'] = float(row['precipitation'])
                row['humidity'] = float(row['humidity'])
                row['month'] = int(row['date'].split('-')[1])
                self.data.append(row)
    
    def get_basic_stats(self, column: str) -> Dict[str, float]:
        """基本統計量を計算"""
        values = [row[column] for row in self.data]
        
        stats = {
            '平均': statistics.mean(values),
            '中央値': statistics.median(values),
            '最大値': max(values),
            '最小値': min(values),
            '標準偏差': statistics.stdev(values) if len(values) > 1 else 0,
            '分散': statistics.variance(values) if len(values) > 1 else 0
        }
        return {k: round(v, 2) for k, v in stats.items()}
    
    def compare_cities(self, column: str) -> Dict[str, Dict[str, float]]:
        """都市間比較"""
        city_data = defaultdict(list)
        
        # 都市別にデータを分類
        for row in self.data:
            city_data[row['city']].append(row[column])
        
        comparison = {}
        for city, values in city_data.items():
            comparison[city] = {
                '平均': round(statistics.mean(values), 2),
                '最高': round(max(values), 2),
                '最低': round(min(values), 2),
                '標準偏差': round(statistics.stdev(values) if len(values) > 1 else 0, 2)
            }
        
        return comparison
    
    def seasonal_analysis(self, city: str, column: str) -> Dict[str, float]:
        """季節分析"""
        seasons = {
            '春': [3, 4, 5],
            '夏': [6, 7, 8], 
            '秋': [9, 10, 11],
            '冬': [12, 1, 2]
        }
        
        seasonal_stats = {}
        for season, months in seasons.items():
            season_values = [
                row[column] for row in self.data 
                if row['city'] == city and row['month'] in months
            ]
            if season_values:
                seasonal_stats[season] = round(statistics.mean(season_values), 2)
            else:
                seasonal_stats[season] = 0.0
                
        return seasonal_stats
    
    def calculate_correlation(self, column1: str, column2: str) -> float:
        """相関係数を計算"""
        values1 = [row[column1] for row in self.data]
        values2 = [row[column2] for row in self.data]
        
        n = len(values1)
        mean1 = statistics.mean(values1)
        mean2 = statistics.mean(values2)
        
        # ピアソン相関係数の計算
        numerator = sum((x - mean1) * (y - mean2) for x, y in zip(values1, values2))
        denominator1 = sum((x - mean1) ** 2 for x in values1)
        denominator2 = sum((y - mean2) ** 2 for y in values2)
        
        if denominator1 == 0 or denominator2 == 0:
            return 0
        
        correlation = numerator / (denominator1 * denominator2) ** 0.5
        return correlation
    
    def find_correlations(self) -> Dict[str, Dict[str, str]]:
        """相関関係の発見"""
        correlations = {}
        
        # 気温と湿度の相関
        temp_humidity_corr = self.calculate_correlation('temperature', 'humidity')
        correlations['気温と湿度'] = {
            '相関係数': str(round(temp_humidity_corr, 3)),
            '解説': self._interpret_correlation(temp_humidity_corr)
        }
        
        # 気温と降水量の相関
        temp_precip_corr = self.calculate_correlation('temperature', 'precipitation')
        correlations['気温と降水量'] = {
            '相関係数': str(round(temp_precip_corr, 3)),
            '解説': self._interpret_correlation(temp_precip_corr)
        }
        
        return correlations
    
    def _interpret_correlation(self, corr_value: float) -> str:
        """相関係数の解釈"""
        if corr_value > 0.7:
            return "強い正の相関（片方が大きいと、もう片方も大きくなる傾向）"
        elif corr_value > 0.3:
            return "中程度の正の相関（ある程度連動している）"
        elif corr_value > -0.3:
            return "弱い相関（あまり関係がない）"
        elif corr_value > -0.7:
            return "中程度の負の相関（片方が大きいと、もう片方は小さくなる傾向）"
        else:
            return "強い負の相関（片方が大きいと、もう片方は確実に小さくなる）"
    
    def weather_probability(self, city: str) -> Dict[str, Dict[str, str]]:
        """天気の確率計算"""
        city_weather = [row['weather_condition'] for row in self.data if row['city'] == city]
        weather_counts = {}
        
        # 天気別カウント
        for weather in city_weather:
            weather_counts[weather] = weather_counts.get(weather, 0) + 1
        
        total = len(city_weather)
        probabilities = {}
        
        for weather, count in weather_counts.items():
            probability = count / total
            probabilities[weather] = {
                '回数': str(count),
                '確率': str(round(probability, 3)),
                'パーセント': f"{round(probability * 100, 1)}%"
            }
            
        return probabilities
    
    def generate_story_data(self, city: str, month: int) -> str:
        """ストーリー生成用データ"""
        month_data = [row for row in self.data if row['city'] == city and row['month'] == month]
        
        if not month_data:
            return f"{city}の{month}月のデータが見つかりません。"
        
        row = month_data[0]
        temp = row['temperature']
        precip = row['precipitation']
        humidity = row['humidity']
        weather = row['weather_condition']
        
        # 都市の年間平均気温を計算
        city_temps = [r['temperature'] for r in self.data if r['city'] == city]
        city_avg = statistics.mean(city_temps)
        
        story = f"""
🌤️ {city}の{month}月の天気物語 🌤️

気温の精霊は「{temp}度」の力を持っています。
{'暖かい' if temp > 20 else '涼しい' if temp > 10 else '寒い'}精霊ですね！

雨の精霊は「{precip}mm」の雨を降らせました。
これは{'たくさん' if precip > 30 else '普通' if precip > 10 else '少し'}の雨を意味します。

湿度の妖精は空気中に「{humidity}%」の水分を混ぜ込みました。
{'ジメジメ' if humidity > 70 else 'さっぱり' if humidity < 60 else '普通'}した感じです。

今日の天気は「{weather}」になりました！

📊 統計ポイント：
- 平均気温との差: {round(temp - city_avg, 1)}度
- この都市の{month}月の特徴: {self._analyze_monthly_feature(city, month, temp, city_avg)}
        """
        
        return story.strip()
    
    def _analyze_monthly_feature(self, city: str, month: int, temp: float, city_avg: float) -> str:
        """月別特徴分析"""
        if temp > city_avg + 5:
            return "年間で特に暖かい月"
        elif temp < city_avg - 5:
            return "年間で特に寒い月"
        else:
            return "年間平均に近い気温の月"


def demo_analysis():
    """デモ実行関数"""
    print("🌤️ 天気データ分析システム - デモ実行中 🌤️\n")
    
    analyzer = SimpleWeatherAnalyzer()
    
    # 1. 基本統計
    print("【1. 気温の基本統計】")
    temp_stats = analyzer.get_basic_stats('temperature')
    for stat, value in temp_stats.items():
        print(f"  {stat}: {value}")
    
    print("\n【2. 都市間気温比較】")
    city_comparison = analyzer.compare_cities('temperature')
    for city, stats in city_comparison.items():
        print(f"  {city}:")
        for stat, value in stats.items():
            print(f"    {stat}: {value}")
    
    print("\n【3. 東京の季節別気温】")
    tokyo_seasons = analyzer.seasonal_analysis('東京', 'temperature')
    for season, temp in tokyo_seasons.items():
        print(f"  {season}: {temp}度")
    
    print("\n【4. 相関関係の発見】")
    correlations = analyzer.find_correlations()
    for relation, data in correlations.items():
        print(f"  {relation}: {data['相関係数']} ({data['解説']})")
    
    print("\n【5. 東京の天気確率】")
    tokyo_weather = analyzer.weather_probability('東京')
    for weather, data in tokyo_weather.items():
        print(f"  {weather}: {data['パーセント']} (年{data['回数']}回)")
    
    print("\n【6. ストーリー形式のデータ】")
    story = analyzer.generate_story_data('東京', 7)
    print(story)


if __name__ == "__main__":
    demo_analysis()