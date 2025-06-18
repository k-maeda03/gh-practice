# GitHub CLI Practice Repository

このリポジトリは GitHub CLI (`gh`) コマンドの練習用です。

## 📋 練習内容

- ✅ リポジトリの作成と管理
- ✅ Issue の作成と管理
- ✅ Pull Request の作成と管理
- ✅ リリースの作成と管理
- GitHub Actions の確認

## 🚀 セットアップ手順

### 前提条件
- Python 3.8+
- [uv](https://docs.astral.sh/uv/) (推奨パッケージマネージャー)

### uvのインストール
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### プロジェクトのセットアップ
1. リポジトリをクローン:
   ```bash
   git clone https://github.com/k-maeda03/gh-practice.git
   cd gh-practice
   ```

2. 開発環境をセットアップ:
   ```bash
   make setup-dev
   # または手動で:
   uv venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate   # Windows
   uv pip install -e ".[dev]"
   ```

## 💻 使用例

### Python スクリプトの実行

```bash
# 基本的な実行
uv run python hello.py

# 名前を指定して実行
uv run python hello.py --name "あなたの名前"

# 詳細ログを有効にして実行
uv run python hello.py --verbose

# ヘルプを表示
uv run python hello.py --help

# Makefileを使用
make run
make run-help
```

### 開発作業

```bash
# テストの実行
make test

# カバレッジ付きテスト
make test-cov

# コードフォーマット
make format

# リンティング
make lint

# 型チェック
make type-check

# すべてのCI チェックを実行
make ci
```

### GitHub CLI コマンド例

```bash
# リポジトリ情報の確認
gh repo view

# Issue の一覧表示
gh issue list

# PR の一覧表示
gh pr list

# リリースの一覧表示
gh release list

# 新しいIssueを作成
gh issue create --title "タイトル" --body "説明"

# 新しいPRを作成
gh pr create --title "タイトル" --body "説明"
```

## 📁 ファイル構成

- `README.md` - このファイル
- `hello.py` - 改善されたPythonスクリプト

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. Pull Request を作成

## 📝 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 📞 サポート

質問や問題がある場合は、[Issues](https://github.com/k-maeda03/gh-practice/issues) で報告してください。