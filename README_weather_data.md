# 🌤️ 中学生向け天気データ分析システム

## 📂 ファイル構成

### データファイル
- `weather_data.csv` - 2023年の日本4都市（東京、大阪、札幌、福岡）の月別気象データ

### 分析プログラム
- `weather_analysis_simple.py` - 標準ライブラリのみを使用した分析システム
- `weather_analysis.py` - pandas/numpy対応版（モジュールインストール必要）

## 📊 データ構造

### CSVデータ形式
```csv
date,city,temperature,precipitation,humidity,weather_condition
2023-01-01,東京,8.2,2.1,65,曇り
```

#### 項目説明
- **date**: 日付（月初日で代表）
- **city**: 都市名（東京、大阪、札幌、福岡）
- **temperature**: 気温（摂氏）
- **precipitation**: 降水量（mm）
- **humidity**: 湿度（%）
- **weather_condition**: 天気（晴れ、曇り、雨、雪）

## 🚀 使用方法

### 基本実行
```bash
python weather_analysis_simple.py
```

### プログラム内での利用
```python
from weather_analysis_simple import SimpleWeatherAnalyzer

# 初期化
analyzer = SimpleWeatherAnalyzer("weather_data.csv")

# 基本統計
stats = analyzer.get_basic_stats('temperature')
print(stats)

# 都市間比較
comparison = analyzer.compare_cities('temperature')
print(comparison)

# 季節分析
seasons = analyzer.seasonal_analysis('東京', 'temperature')
print(seasons)

# 物語生成
story = analyzer.generate_story_data('東京', 7)
print(story)
```

## 📚 学習できる統計概念

### 1. 基本統計量
- 平均値（mean）
- 中央値（median）
- 最大値・最小値
- 標準偏差・分散

### 2. 比較分析
- 都市間比較
- 季節変動分析
- 時系列変化

### 3. 相関分析
- 気温と湿度の関係
- 気温と降水量の関係
- 相関係数の解釈

### 4. 確率計算
- 天気の出現確率
- パーセンテージ表示
- 頻度分析

## 🎯 教育効果

### 中学生にとってのメリット
1. **身近なテーマ**: 天気という日常的な現象で統計を学習
2. **視覚的理解**: 数値データを物語形式で表現
3. **段階的学習**: 基礎から応用まで体系的に構成
4. **実用性実感**: 実際のデータでの分析体験

### 統計概念の具体化
- 「平均」→ 年間を通じた典型的な気温
- 「相関」→ 気温が高いときは降水量も多い傾向
- 「確率」→ 東京で晴れる確率は50%
- 「分散」→ 札幌は気温変化が大きい都市

## 🔧 カスタマイズ方法

### データ追加
1. `weather_data.csv`に新しい行を追加
2. 日付形式: `YYYY-MM-DD`
3. 数値データは小数点対応

### 新機能追加
```python
class SimpleWeatherAnalyzer:
    def custom_analysis(self):
        # 独自の分析機能を追加
        pass
```

### 物語のカスタマイズ
`generate_story_data()`メソッドを編集して、より創造的な物語を生成可能

## 📈 出力例

```
🌤️ 東京の7月の天気物語 🌤️

気温の精霊は「28.7度」の力を持っています。
暖かい精霊ですね！

雨の精霊は「35.2mm」の雨を降らせました。
これはたくさんの雨を意味します。

📊 統計ポイント：
- 平均気温との差: 9.1度
- この都市の7月の特徴: 年間で特に暖かい月
```

## 🎓 発展的活用

### 追加可能な分析
- 予測モデルの構築
- 異常値検出
- クラスタリング分析
- 回帰分析

### 他教科との連携
- 地理：地域特性の理解
- 理科：気象現象の科学的理解
- 社会：気候変動の社会的影響

---

このシステムは中学生が統計学の基礎を楽しく学び、データサイエンスの実用性を体感できるよう設計されています。