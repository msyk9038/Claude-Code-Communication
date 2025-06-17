#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統計概念の分かりやすい説明システム
中学生向け天気データ統計学習支援
"""

import json
from typing import Dict, List, Any

class StatsConceptExplainer:
    """統計概念を中学生にも分かりやすく説明するクラス"""
    
    def __init__(self):
        self.concepts = {
            "mean": {
                "name": "平均値",
                "simple_explanation": "全部の数を足して、個数で割った値だよ！",
                "detailed_explanation": """
                平均値は、データの「真ん中あたり」を表す代表的な値です。
                全てのデータを足し合わせて、データの個数で割ることで計算します。
                
                例：今週の最高気温が [25, 28, 30, 26, 31] 度だった場合
                平均 = (25 + 28 + 30 + 26 + 31) ÷ 5 = 140 ÷ 5 = 28度
                """,
                "why_important": """
                平均値を知ることで「だいたいどのくらい」が分かるよ！
                天気予報で「今週の平均気温」と言われたら、
                極端に暑い日や寒い日があっても、全体的な傾向が分かるんだ。
                """,
                "weather_example": {
                    "scenario": "今週の最高気温",
                    "data": [25, 28, 30, 26, 31],
                    "calculation": "平均 = (25+28+30+26+31) ÷ 5 = 28度",
                    "insight": "今週は平均的に28度の暖かい日が続いたね！"
                }
            },
            
            "median": {
                "name": "中央値",
                "simple_explanation": "数を小さい順に並べて、真ん中にある値だよ！",
                "detailed_explanation": """
                中央値は、データを小さい順（または大きい順）に並べたとき、
                ちょうど真ん中にくる値です。
                
                例：今週の最高気温 [25, 28, 30, 26, 31] を小さい順に並べると
                [25, 26, 28, 30, 31] → 真ん中は28度
                """,
                "why_important": """
                中央値は「極端な値」に影響されにくいんだ！
                もし1日だけ異常に暑い日（例：40度）があっても、
                中央値はあまり変わらないから、「普通の日」がどのくらいか分かるよ。
                """,
                "weather_example": {
                    "scenario": "今週の最高気温",
                    "data": [25, 28, 30, 26, 31],
                    "sorted_data": [25, 26, 28, 30, 31],
                    "calculation": "真ん中（3番目）の値 = 28度",
                    "insight": "半分の日は28度以下、半分の日は28度以上だったね！"
                }
            },
            
            "mode": {
                "name": "最頻値",
                "simple_explanation": "一番多く出てくる値だよ！",
                "detailed_explanation": """
                最頻値は、データの中で最も頻繁に現れる値です。
                「一番人気」の値とも言えるね。
                
                例：今週の天気が [晴れ, 曇り, 晴れ, 雨, 晴れ] だった場合
                最頻値 = 晴れ（3回出現）
                """,
                "why_important": """
                最頻値で「一番よくあるパターン」が分かるよ！
                天気予報で「この季節は晴れが多い」と言われるのは、
                最頻値を使って判断しているんだ。
                """,
                "weather_example": {
                    "scenario": "今週の天気",
                    "data": ["晴れ", "曇り", "晴れ", "雨", "晴れ"],
                    "frequency": {"晴れ": 3, "曇り": 1, "雨": 1},
                    "calculation": "最頻値 = 晴れ（3回）",
                    "insight": "今週は晴れの日が多かったね！"
                }
            }
        }
    
    def explain_concept(self, concept_name: str) -> Dict[str, Any]:
        """指定された統計概念の説明を返す"""
        if concept_name not in self.concepts:
            return {"error": f"概念 '{concept_name}' は見つかりませんでした"}
        
        return self.concepts[concept_name]
    
    def get_all_concepts(self) -> List[str]:
        """利用可能な統計概念の一覧を返す"""
        return list(self.concepts.keys())
    
    def get_concept_comparison(self) -> Dict[str, str]:
        """3つの統計概念の違いを比較して説明"""
        return {
            "comparison_title": "平均値 vs 中央値 vs 最頻値",
            "scenario": "クラスのテストの点数: [60, 70, 80, 80, 90, 95, 100]",
            "mean": "平均値 = 82.1点（全員の合計を人数で割った値）",
            "median": "中央値 = 80点（真ん中の人の点数）", 
            "mode": "最頻値 = 80点（一番多く取られた点数）",
            "key_insight": """
            同じデータでも、見る角度によって違う「代表値」になるんだ！
            - 平均値：全体のバランスを見る
            - 中央値：真ん中の値を見る  
            - 最頻値：一番多いパターンを見る
            
            天気予報でも、目的に応じて使い分けているよ！
            """
        }

class LearningProgressGuide:
    """段階的学習ガイドシステム"""
    
    def __init__(self):
        self.learning_steps = [
            {
                "step": 1,
                "title": "🌤️ 統計って何？",
                "goal": "統計の基本的な考え方を理解する",
                "content": """
                統計は「たくさんのデータから傾向や特徴を見つける方法」だよ！
                
                例えば：
                - 今週は雨が多かった？少なかった？
                - 今年の夏は去年より暑い？
                - 明日の天気はどうなりそう？
                
                こんな疑問に数字で答えるのが統計なんだ！
                """,
                "activity": "今週の天気を思い出して、晴れ・曇り・雨の日数を数えてみよう",
                "hint": "統計は「数で表すことで、物事をより正確に理解する道具」だよ"
            },
            {
                "step": 2,
                "title": "📊 データの代表値を知ろう",
                "goal": "平均値・中央値・最頻値の違いを理解する",
                "content": """
                データの特徴を表す3つの代表値を学ぼう！
                
                🎯 平均値：全部を足して個数で割る
                🎯 中央値：並べて真ん中の値
                🎯 最頻値：一番多く現れる値
                """,
                "activity": "友達5人の身長を測って、3つの代表値を計算してみよう",
                "hint": "同じデータでも、見方によって違う「代表値」になることを発見しよう"
            },
            {
                "step": 3,
                "title": "🌡️ 天気データで実践",
                "goal": "実際の天気データで統計を計算してみる",
                "content": """
                実際の天気データを使って統計を計算してみよう！
                
                今週の最高気温データを使って：
                - 平均気温を計算
                - 中央値を見つける
                - 最も多い気温を探す
                """,
                "activity": "気象庁のデータを使って、あなたの住んでいる地域の気温を分析してみよう",
                "hint": "実際のデータを使うと、統計がより身近に感じられるよ"
            },
            {
                "step": 4,
                "title": "🔍 データの傾向を読み取ろう",
                "goal": "統計から天気の傾向を読み取る",
                "content": """
                統計から「傾向」や「パターン」を見つけよう！
                
                - 今月は先月より暖かい？
                - 雨の日が多い曜日はある？
                - 季節の変わり目はいつ？
                """,
                "activity": "1ヶ月分の天気データから、面白い発見をしてみよう",
                "hint": "統計は「なぜ？」を考えるきっかけをくれるよ"
            },
            {
                "step": 5,
                "title": "🎓 統計マスターになろう",
                "goal": "学んだ統計を使って天気を予測してみる",
                "content": """
                おめでとう！統計の基本をマスターしたね！
                
                今度は学んだことを使って：
                - 明日の天気を予測してみよう
                - 来週の気温を推測してみよう
                - 友達と予測を比べてみよう
                """,
                "activity": "統計的な根拠を持って、天気予測にチャレンジしよう",
                "hint": "統計は未来を予測する強力な道具になるよ"
            }
        ]
    
    def get_step(self, step_number: int) -> Dict[str, Any]:
        """指定されたステップの内容を返す"""
        if step_number < 1 or step_number > len(self.learning_steps):
            return {"error": f"ステップ {step_number} は存在しません"}
        
        return self.learning_steps[step_number - 1]
    
    def get_all_steps(self) -> List[Dict[str, Any]]:
        """全学習ステップを返す"""
        return self.learning_steps
    
    def get_next_step(self, current_step: int) -> Dict[str, Any]:
        """次のステップを返す"""
        if current_step >= len(self.learning_steps):
            return {"message": "おめでとう！全てのステップを完了しました！🎉"}
        
        return self.get_step(current_step + 1)

class FeedbackSystem:
    """達成感を与えるフィードバックシステム"""
    
    def __init__(self):
        self.achievements = {
            "first_calculation": {
                "title": "🎯 初めての計算",
                "description": "統計の計算を初めて行いました！",
                "message": "すごい！統計の世界への第一歩だね！",
                "points": 10
            },
            "concept_master": {
                "title": "📚 概念マスター", 
                "description": "3つの代表値の違いを理解しました！",
                "message": "平均値・中央値・最頻値を使い分けられるようになったね！",
                "points": 25
            },
            "data_analyst": {
                "title": "🔍 データアナリスト",
                "description": "実際のデータを分析しました！",
                "message": "本物のデータサイエンティストみたいだね！",
                "points": 30
            },
            "weather_predictor": {
                "title": "🌤️ 天気予報士",
                "description": "統計を使って天気を予測しました！",
                "message": "君も立派な天気予報士の仲間入りだ！",
                "points": 50
            },
            "stats_wizard": {
                "title": "🧙‍♂️ 統計の魔法使い",
                "description": "全ての学習ステップを完了しました！",
                "message": "おめでとう！統計の魔法を使いこなせるようになったね！",
                "points": 100
            }
        }
    
    def get_achievement(self, achievement_id: str) -> Dict[str, Any]:
        """指定された達成項目を返す"""
        if achievement_id not in self.achievements:
            return {"error": f"達成項目 '{achievement_id}' は見つかりませんでした"}
        
        return self.achievements[achievement_id]
    
    def generate_encouragement(self, progress_percent: float) -> str:
        """進捗率に応じた励ましメッセージを生成"""
        if progress_percent < 20:
            return "🌱 素晴らしいスタートだね！統計の世界へようこそ！"
        elif progress_percent < 40:
            return "🌿 順調に成長しているよ！この調子で頑張ろう！"
        elif progress_percent < 60:
            return "🌳 もう半分以上進んだね！統計が面白くなってきた？"
        elif progress_percent < 80:
            return "🏆 ほぼゴールが見えてきたよ！あと少しで統計マスターだ！"
        else:
            return "🎉 おめでとう！統計の達人になったね！素晴らしい成果だよ！"
    
    def get_hint_for_difficulty(self, concept: str, difficulty_level: str) -> str:
        """難易度に応じたヒントを提供"""
        hints = {
            "mean": {
                "easy": "全部の数を足して、個数で割るだけだよ！",
                "medium": "極端に大きい値や小さい値があると、平均値は影響を受けやすいよ",
                "hard": "加重平均を使うと、重要なデータにより重みを付けられるよ"
            },
            "median": {
                "easy": "まず数を小さい順に並べて、真ん中を見つけよう！",
                "medium": "データが偶数個の場合は、真ん中2つの平均を取るよ",
                "hard": "外れ値に影響されにくいので、ロバストな統計量と呼ばれるよ"
            },
            "mode": {
                "easy": "一番多く出てくる値を探そう！",
                "medium": "最頻値が複数ある場合もあるよ（多峰性）",
                "hard": "カテゴリーデータの場合、最頻値が最も意味のある代表値になるよ"
            }
        }
        
        return hints.get(concept, {}).get(difficulty_level, "頑張って考えてみよう！")

def main():
    """メイン関数：教育システムのデモンストレーション"""
    print("🌤️ 天気データ統計学習システム 🌤️")
    print("=" * 50)
    
    # 統計概念の説明
    explainer = StatsConceptExplainer()
    print("\n📚 統計概念の説明:")
    for concept in explainer.get_all_concepts():
        explanation = explainer.explain_concept(concept)
        print(f"\n{explanation['name']}: {explanation['simple_explanation']}")
    
    # 学習ガイド
    guide = LearningProgressGuide()
    print("\n🎯 学習ステップ:")
    for step in guide.get_all_steps():
        print(f"Step {step['step']}: {step['title']}")
    
    # フィードバックシステム
    feedback = FeedbackSystem()
    print("\n🏆 達成可能な称号:")
    for achievement_id, achievement in feedback.achievements.items():
        print(f"- {achievement['title']}: {achievement['description']}")
    
    print("\n🎉 学習を始める準備ができました！")

if __name__ == "__main__":
    main()