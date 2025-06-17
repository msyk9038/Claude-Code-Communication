import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io

# ページ設定
st.set_page_config(
    page_title="🌤️ お天気データサイエンス",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #87CEEB 0%, #4169E1 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .stats-card {
        background: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4169E1;
        margin: 0.5rem 0;
    }
    .level-badge {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem;
    }
    .weather-emoji {
        font-size: 2rem;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'experience' not in st.session_state:
    st.session_state.experience = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'achievements' not in st.session_state:
    st.session_state.achievements = []

def calculate_level(exp):
    """経験値からレベルを計算"""
    return min(10, 1 + exp // 100)

def get_level_title(level):
    """レベルに応じた称号を取得"""
    titles = {
        1: "🌱 気象見習い",
        2: "🌤️ 天気初心者",
        3: "☁️ 雲観察者",
        4: "🌧️ 雨量マスター",
        5: "❄️ 気温分析師",
        6: "🌪️ 統計探偵",
        7: "🌈 データ魔法使い",
        8: "⛈️ 予報エキスパート",
        9: "🌟 気象マエストロ",
        10: "👑 ウェザーマスター"
    }
    return titles.get(level, "🌱 気象見習い")

def add_experience(points, achievement=""):
    """経験値を追加"""
    st.session_state.experience += points
    new_level = calculate_level(st.session_state.experience)
    
    if new_level > st.session_state.level:
        st.session_state.level = new_level
        st.balloons()
        st.success(f"🎉 レベルアップ！ {get_level_title(new_level)} になりました！")
    
    if achievement and achievement not in st.session_state.achievements:
        st.session_state.achievements.append(achievement)
        st.success(f"🏆 新しい実績を獲得: {achievement}")

# メインヘッダー
st.markdown("""
<div class="main-header">
    <h1>🌤️ お天気データサイエンス</h1>
    <p>統計の魔法で天気の秘密を解き明かそう！</p>
</div>
""", unsafe_allow_html=True)

# サイドバー - プレイヤー情報
with st.sidebar:
    st.markdown("### 👤 あなたの情報")
    
    # レベルとタイトル表示
    current_level = calculate_level(st.session_state.experience)
    st.session_state.level = current_level
    
    st.markdown(f"""
    <div class="level-badge">
        Level {current_level}: {get_level_title(current_level)}
    </div>
    """, unsafe_allow_html=True)
    
    # 経験値バー
    exp_in_level = st.session_state.experience % 100
    progress = exp_in_level / 100
    st.progress(progress)
    st.write(f"経験値: {st.session_state.experience} ({exp_in_level}/100)")
    
    # 実績表示
    if st.session_state.achievements:
        st.markdown("### 🏆 獲得実績")
        for achievement in st.session_state.achievements:
            st.write(f"• {achievement}")

# メインコンテンツ
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📊 データアップロード")
    
    # サンプルデータ生成ボタン
    if st.button("🎲 サンプルデータを生成", type="primary"):
        # サンプル天気データを生成
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        np.random.seed(42)
        
        sample_data = pd.DataFrame({
            '日付': dates,
            '気温(℃)': np.random.normal(15, 8, 30).round(1),
            '湿度(%)': np.random.normal(60, 15, 30).round(0),
            '降水量(mm)': np.random.exponential(2, 30).round(1),
            '風速(m/s)': np.random.gamma(2, 2, 30).round(1)
        })
        
        st.session_state.weather_data = sample_data
        add_experience(20, "🎲 初回データ生成")
        st.success("サンプルデータを生成しました！")
    
    # CSVファイルアップロード
    uploaded_file = st.file_uploader(
        "CSVファイルをアップロード",
        type=['csv'],
        help="気温、湿度、降水量などの天気データをアップロードしてください"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            st.session_state.weather_data = df
            add_experience(30, "📁 ファイルアップロード達成")
            st.success("データをアップロードしました！")
        except Exception as e:
            st.error(f"エラー: {str(e)}")

with col2:
    st.markdown("### 🎯 学習モード選択")
    
    mode = st.selectbox(
        "学習したい統計概念を選んでください",
        ["基本統計（平均・中央値・最頻値）", "データの分布", "相関関係", "時系列分析"],
        help="各モードで異なる統計概念を学べます"
    )

# データが読み込まれている場合の処理
if 'weather_data' in st.session_state:
    df = st.session_state.weather_data
    
    st.markdown("---")
    st.markdown("### 📈 データ分析結果")
    
    # データ概要
    st.markdown("#### 📋 データの概要")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("データ数", len(df))
    with col2:
        st.metric("列数", len(df.columns))
    with col3:
        if len(df.columns) > 1:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            st.metric("数値列数", len(numeric_cols))
    
    # 数値列の選択
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_columns:
        selected_column = st.selectbox(
            "分析したい項目を選択してください",
            numeric_columns,
            help="統計を計算したい数値データを選んでください"
        )
        
        if selected_column:
            data = df[selected_column].dropna()
            
            if mode == "基本統計（平均・中央値・最頻値）":
                st.markdown("#### 📊 基本統計量")
                
                # 統計量計算
                mean_val = data.mean()
                median_val = data.median() 
                std_val = data.std()
                
                # 最頻値の計算（数値データの場合は最も近い値を使用）
                try:
                    mode_val = data.mode().iloc[0] if not data.mode().empty else "なし"
                except:
                    mode_val = "計算不可"
                
                # 統計量表示
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="stats-card">
                        <h4>📊 平均値</h4>
                        <h2>{mean_val:.2f}</h2>
                        <p>データの中心的な値</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="stats-card">
                        <h4>📍 中央値</h4>
                        <h2>{median_val:.2f}</h2>
                        <p>データを順番に並べた真ん中の値</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="stats-card">
                        <h4>🎯 最頻値</h4>
                        <h2>{mode_val}</h2>
                        <p>最も多く現れる値</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="stats-card">
                        <h4>📏 標準偏差</h4>
                        <h2>{std_val:.2f}</h2>
                        <p>データのばらつき具合</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 統計量の説明
                st.markdown("#### 🧠 統計量の意味")
                st.info(f"""
                **平均値**: {mean_val:.2f} - 全てのデータを足して個数で割った値です。\n
                **中央値**: {median_val:.2f} - データを小さい順に並べた時の真ん中の値です。\n
                **標準偏差**: {std_val:.2f} - データが平均からどれくらいばらついているかを表します。
                """)
                
                # ヒストグラム
                fig = px.histogram(
                    df, 
                    x=selected_column,
                    title=f"{selected_column}の分布",
                    nbins=20,
                    color_discrete_sequence=['#4169E1']
                )
                
                # 統計量の線を追加
                fig.add_vline(x=mean_val, line_dash="dash", line_color="red", 
                             annotation_text=f"平均値: {mean_val:.2f}")
                fig.add_vline(x=median_val, line_dash="dash", line_color="green",
                             annotation_text=f"中央値: {median_val:.2f}")
                
                fig.update_layout(
                    xaxis_title=selected_column,
                    yaxis_title="頻度",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 経験値獲得
                add_experience(50, "📊 基本統計計算完了")
            
            elif mode == "データの分布":
                st.markdown("#### 📊 データの分布分析")
                
                # ヒストグラムとボックスプロット
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_hist = px.histogram(
                        df, 
                        x=selected_column,
                        title=f"{selected_column}のヒストグラム",
                        color_discrete_sequence=['#87CEEB']
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col2:
                    fig_box = px.box(
                        df, 
                        y=selected_column,
                        title=f"{selected_column}のボックスプロット",
                        color_discrete_sequence=['#4169E1']
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
                
                add_experience(40, "📈 分布分析完了")
            
            elif mode == "相関関係":
                if len(numeric_columns) >= 2:
                    st.markdown("#### 🔗 相関関係の分析")
                    
                    # 2つ目の変数選択
                    other_columns = [col for col in numeric_columns if col != selected_column]
                    selected_column2 = st.selectbox(
                        "比較する項目を選択してください",
                        other_columns
                    )
                    
                    if selected_column2:
                        # 散布図
                        fig_scatter = px.scatter(
                            df,
                            x=selected_column,
                            y=selected_column2,
                            title=f"{selected_column} vs {selected_column2}",
                            color_discrete_sequence=['#4169E1'],
                            trendline="ols"
                        )
                        st.plotly_chart(fig_scatter, use_container_width=True)
                        
                        # 相関係数
                        correlation = df[selected_column].corr(df[selected_column2])
                        
                        if abs(correlation) > 0.7:
                            strength = "強い"
                            emoji = "💪"
                        elif abs(correlation) > 0.3:
                            strength = "中程度の"
                            emoji = "👍"
                        else:
                            strength = "弱い"
                            emoji = "👌"
                        
                        st.markdown(f"""
                        ### {emoji} 相関の強さ: {strength}相関
                        **相関係数**: {correlation:.3f}
                        
                        {selected_column}と{selected_column2}の間には{strength}相関があります。
                        """)
                        
                        add_experience(60, "🔗 相関分析マスター")
                else:
                    st.warning("相関分析には2つ以上の数値列が必要です。")
            
            elif mode == "時系列分析":
                # 日付列を探す
                date_columns = df.select_dtypes(include=['datetime64', 'object']).columns
                
                if len(date_columns) > 0:
                    date_column = st.selectbox("日付列を選択してください", date_columns)
                    
                    try:
                        df[date_column] = pd.to_datetime(df[date_column])
                        
                        # 時系列プロット
                        fig_time = px.line(
                            df,
                            x=date_column,
                            y=selected_column,
                            title=f"{selected_column}の時系列変化",
                            color_discrete_sequence=['#4169E1']
                        )
                        st.plotly_chart(fig_time, use_container_width=True)
                        
                        # トレンド分析
                        df_sorted = df.sort_values(date_column)
                        first_half = df_sorted[:len(df_sorted)//2][selected_column].mean()
                        second_half = df_sorted[len(df_sorted)//2:][selected_column].mean()
                        
                        trend = "上昇" if second_half > first_half else "下降"
                        trend_emoji = "📈" if trend == "上昇" else "📉"
                        
                        st.markdown(f"""
                        ### {trend_emoji} トレンド分析
                        期間前半の平均: {first_half:.2f}
                        期間後半の平均: {second_half:.2f}
                        
                        **{selected_column}は{trend}傾向**にあります。
                        """)
                        
                        add_experience(70, "📅 時系列分析エキスパート")
                        
                    except Exception as e:
                        st.error(f"日付の解析に失敗しました: {str(e)}")
                else:
                    st.warning("時系列分析には日付列が必要です。")
    
    # データテーブル表示
    with st.expander("📋 データを確認"):
        st.dataframe(df, use_container_width=True)

else:
    # データが未読み込みの場合
    st.markdown("### 🚀 使い方")
    st.info("""
    1. **サンプルデータを生成**ボタンを押すか、CSVファイルをアップロードしてください
    2. 学習したい統計概念を選択してください
    3. 分析したい項目を選んで統計を学びましょう！
    
    統計を学んで経験値を貯め、レベルアップを目指そう！ 🎯
    """)
    
    # 学習のヒント
    st.markdown("### 💡 統計学習のヒント")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📊 基本統計**
        - 平均値：データの中心
        - 中央値：順番の真ん中
        - 最頻値：一番多い値
        """)
    
    with col2:
        st.markdown("""
        **📈 発展的概念**
        - 分布：データの広がり
        - 相関：2つの関係性
        - 時系列：時間の変化
        """)

# フッター
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    🌤️ お天気データサイエンス - 統計の魔法で未来を予測しよう！
</div>
""", unsafe_allow_html=True)