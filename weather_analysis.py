#!/usr/bin/env python3
"""
中学生向け天気データ分析関数
統計学習に適したデータ処理機能を提供
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

class WeatherDataAnalyzer:
    """天気データ分析クラス"""
    
    def __init__(self, csv_file_path: str = "weather_data.csv"):
        """
        初期化
        Args:
            csv_file_path: CSVファイルのパス
        """
        self.data = pd.read_csv(csv_file_path)
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data['month'] = self.data['date'].dt.month
        
    def get_basic_stats(self, column: str) -> Dict[str, float]:
        """
        基本統計量を計算（中学生向け）
        Args:
            column: 分析する列名
        Returns:
            基本統計量の辞書
        """
        stats = {
            '平均': self.data[column].mean(),
            '中央値': self.data[column].median(),
            '最大値': self.data[column].max(),
            '最小値': self.data[column].min(),
            '標準偏差': self.data[column].std(),
            '分散': self.data[column].var()
        }
        return {k: round(v, 2) for k, v in stats.items()}
    
    def compare_cities(self, column: str) -> pd.DataFrame:
        """
        都市間比較（中学生にわかりやすい形式）
        Args:
            column: 比較する項目
        Returns:
            都市別統計表
        """
        comparison = self.data.groupby('city')[column].agg([
            ('平均', 'mean'),
            ('最高', 'max'),
            ('最低', 'min'),
            ('標準偏差', 'std')
        ]).round(2)
        
        return comparison
    
    def seasonal_analysis(self, city: str, column: str) -> Dict[str, float]:
        """
        季節分析（四季での変化）
        Args:
            city: 都市名
            column: 分析項目
        Returns:
            季節別統計
        """
        city_data = self.data[self.data['city'] == city]
        
        seasons = {
            '春': [3, 4, 5],
            '夏': [6, 7, 8], 
            '秋': [9, 10, 11],
            '冬': [12, 1, 2]
        }
        
        seasonal_stats = {}
        for season, months in seasons.items():
            season_data = city_data[city_data['month'].isin(months)]
            seasonal_stats[season] = round(season_data[column].mean(), 2)
            
        return seasonal_stats
    
    def find_correlations(self) -> Dict[str, float]:
        """
        相関関係の発見（中学生向け簡単解説付き）
        Returns:
            相関係数と解説
        """
        correlations = {}
        
        # 気温と湿度の相関
        temp_humidity_corr = self.data['temperature'].corr(self.data['humidity'])
        correlations['気温と湿度'] = {
            '相関係数': round(temp_humidity_corr, 3),
            '解説': self._interpret_correlation(temp_humidity_corr)
        }
        
        # 気温と降水量の相関
        temp_precip_corr = self.data['temperature'].corr(self.data['precipitation'])
        correlations['気温と降水量'] = {
            '相関係数': round(temp_precip_corr, 3),
            '解説': self._interpret_correlation(temp_precip_corr)
        }
        
        return correlations
    
    def _interpret_correlation(self, corr_value: float) -> str:
        """相関係数の解釈（中学生向け）"""
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
    
    def weather_probability(self, city: str) -> Dict[str, float]:
        """
        天気の確率計算（確率の学習）
        Args:
            city: 都市名
        Returns:
            天気別出現確率
        """
        city_data = self.data[self.data['city'] == city]
        weather_counts = city_data['weather_condition'].value_counts()
        total = len(city_data)
        
        probabilities = {}
        for weather, count in weather_counts.items():
            probability = count / total
            probabilities[weather] = {
                '回数': count,
                '確率': round(probability, 3),
                'パーセント': f"{round(probability * 100, 1)}%"
            }
            
        return probabilities
    
    def generate_story_data(self, city: str, month: int) -> str:
        """
        ストーリー生成用データ（物語形式での統計学習）
        Args:
            city: 都市名
            month: 月
        Returns:
            物語形式の統計データ
        """
        month_data = self.data[(self.data['city'] == city) & (self.data['month'] == month)]
        
        if month_data.empty:
            return f"{city}の{month}月のデータが見つかりません。"
        
        row = month_data.iloc[0]
        temp = row['temperature']
        precip = row['precipitation']
        humidity = row['humidity']
        weather = row['weather_condition']
        
        # 統計概念を物語化
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
- 平均気温との差: {round(temp - self.data[self.data['city'] == city]['temperature'].mean(), 1)}度
- この都市の{month}月の特徴: {self._analyze_monthly_feature(city, month)}
        """
        
        return story.strip()
    
    def _analyze_monthly_feature(self, city: str, month: int) -> str:
        """月別特徴分析"""
        city_data = self.data[self.data['city'] == city]
        month_data = city_data[city_data['month'] == month]
        
        if month_data.empty:
            return "データなし"
            
        temp = month_data['temperature'].iloc[0]
        city_avg = city_data['temperature'].mean()
        
        if temp > city_avg + 5:
            return "年間で特に暖かい月"
        elif temp < city_avg - 5:
            return "年間で特に寒い月"
        else:
            return "年間平均に近い気温の月"


def demo_analysis():
    """デモ実行関数"""
    print("🌤️ 天気データ分析システム - デモ実行中 🌤️\n")
    
    analyzer = WeatherDataAnalyzer()
    
    # 1. 基本統計
    print("【1. 気温の基本統計】")
    temp_stats = analyzer.get_basic_stats('temperature')
    for stat, value in temp_stats.items():
        print(f"  {stat}: {value}")
    
    print("\n【2. 都市間気温比較】")
    city_comparison = analyzer.compare_cities('temperature')
    print(city_comparison)
    
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