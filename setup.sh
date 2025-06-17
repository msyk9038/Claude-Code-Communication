#!/bin/bash

# 🚀 Multi-Agent Communication Demo 環境構築
# 参考: setup_full_environment.sh

set -e  # エラー時に停止

# 色付きログ関数
log_info() {
    echo -e "\033[1;32m[INFO]\033[0m $1"
}

log_success() {
    echo -e "\033[1;34m[SUCCESS]\033[0m $1"
}

echo "🤖 Multi-Agent Communication Demo 環境構築"
echo "==========================================="
echo ""

# STEP 1: 既存セッションクリーンアップ
log_info "🧹 既存セッションクリーンアップ開始..."

tmux kill-session -t multiagent 2>/dev/null && log_info "multiagentセッション削除完了" || log_info "multiagentセッションは存在しませんでした"
tmux kill-session -t president 2>/dev/null && log_info "presidentセッション削除完了" || log_info "presidentセッションは存在しませんでした"

# 完了ファイルクリア
mkdir -p ./tmp
rm -f ./tmp/worker*_done.txt 2>/dev/null && log_info "既存の完了ファイルをクリア" || log_info "完了ファイルは存在しませんでした"

log_success "✅ クリーンアップ完了"
echo ""

# STEP 2: multiagentセッション作成（4ペイン：boss + worker1,2,3）
log_info "📺 multiagentセッション作成開始 (4ペイン)..."

# 最初のペイン作成（bashを明示指定）
tmux new-session -d -s multiagent -n "agents" bash

# 2x2グリッド作成（合計4ペイン）
tmux split-window -h -t "multiagent:0" bash      # 水平分割（左右）
tmux select-pane -t "multiagent:0.0"
tmux split-window -v bash                        # 左側を垂直分割
tmux select-pane -t "multiagent:0.2"
tmux split-window -v bash                        # 右側を垂直分割

# ペインタイトル設定
log_info "ペインタイトル設定中..."
PANE_TITLES=("boss" "worker1" "worker2" "worker3")

for i in {0..3}; do
    tmux select-pane -t "multiagent:0.$i" -T "${PANE_TITLES[$i]}"
    
    # 作業ディレクトリ設定
    tmux send-keys -t "multiagent:0.$i" "cd $(pwd)" C-m
    
    # カラープロンプト設定
    if [ $i -eq 0 ]; then
        # boss: 赤色
        tmux send-keys -t "multiagent:0.$i" "export PS1='(\[\033[1;31m\]${PANE_TITLES[$i]}\[\033[0m\]) \[\033[1;32m\]\w\[\033[0m\]\$ '" C-m
    else
        # workers: 青色
        tmux send-keys -t "multiagent:0.$i" "export PS1='(\[\033[1;34m\]${PANE_TITLES[$i]}\[\033[0m\]) \[\033[1;32m\]\w\[\033[0m\]\$ '" C-m
    fi

    # 画面をクリア
    tmux send-keys -t "multiagent:0.$i" "clear" C-m
done

log_success "✅ multiagentセッション作成完了"
echo ""

# STEP 3: presidentセッション作成（1ペイン）
log_info "👑 presidentセッション作成開始..."

tmux new-session -d -s president bash
tmux send-keys -t president "cd $(pwd)" C-m
tmux send-keys -t president "export PS1='(\[\033[1;35m\]PRESIDENT\[\033[0m\]) \[\033[1;32m\]\w\[\033[0m\]\$ '" C-m
# 画面をクリア
tmux send-keys -t president "clear" C-m

log_success "✅ presidentセッション作成完了"
echo ""

# STEP 4: 環境確認・表示
log_info "🔍 環境確認中..."

echo ""
echo "📊 セットアップ結果:"
echo "==================="

# tmuxセッション確認
echo "📺 Tmux Sessions:"
tmux list-sessions
echo ""

# ペイン構成表示
echo "📋 ペイン構成:"
echo "  multiagentセッション（4ペイン）:"
echo "    Pane 0: boss     (チームリーダー)"
echo "    Pane 1: worker1   (実行担当者A)"
echo "    Pane 2: worker2   (実行担当者B)"
echo "    Pane 3: worker3   (実行担当者C)"
echo ""
echo "  presidentセッション（1ペイン）:"
echo "    Pane 0: PRESIDENT (プロジェクト統括)"

echo ""
log_success "🎉 Demo環境セットアップ完了！"

# STEP 5: PresidentとMulti-AgentでClaude Code起動
log_info "🤖 Claude Code起動中..."
tmux send-keys -t president "claude" C-m
for i in {0..3}; do
    tmux send-keys -t multiagent:0.$i "claude" C-m
done
log_success "✅ Claude Code起動完了"

# STEP 6: 指示書を読み込ませる
log_info "📜 指示書を読み込ませています..."
tmux send-keys -t president "あなたはpresidentです。CLAUDE.md を読み込んでください。" 
tmux send-keys -t multiagent:0.0 "あなたはbossです。CLAUDE.md を読み込んでください。"
for i in {1..3}; do
    tmux send-keys -t multiagent:0.$i "あなたはworker${i}です。CLAUDE.md を読み込んでください。"
done

sleep 2  # 少し待機してからEnterを送信
tmux send-keys -t president Enter
for i in {0..3}; do
    tmux send-keys -t multiagent:0.$i Enter
done
log_success "✅ 指示書読み込み完了"


echo "  1. 🔗 セッションアタッチ:"
echo "     tmux attach-session -t multiagent   # マルチエージェント確認"
echo "     tmux attach-session -t president    # プレジデント確認"
echo "  2. セッションでタッチ:"
echo "     Ctrl+b, d でセッションからデタッチ"
echo "  3. 🎯 デモ実行: PRESIDENTに「中学生の統計の勉強用にstreamlit アプリを作りたい。テーマは天気。デモ用のデータも作成してほしい。」と入力" 
