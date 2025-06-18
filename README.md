# GitHub CLI Practice Repository

このリポジトリは GitHub CLI (`gh`) コマンドの練習用です。

## 📋 練習内容

- ✅ リポジトリの作成と管理
- ✅ Issue の作成と管理
- ✅ Pull Request の作成と管理
- ✅ リリースの作成と管理
- ✅ GitHub Actions CI/CD パイプライン
- ✅ テスト駆動開発 (pytest)
- ✅ 設定ファイル管理 (pydantic + YAML)
- ✅ プラグインシステム
- ✅ 対話モード

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

### 基本的なスクリプト実行

```bash
# 基本的な実行（従来版）
uv run python hello.py

# 拡張版の実行
uv run python hello_v2.py

# 名前を指定して実行
uv run python hello_v2.py --name "あなたの名前"

# 詳細ログを有効にして実行
uv run python hello_v2.py --verbose

# ヘルプを表示
uv run python hello_v2.py --help
```

### 設定ファイルを使用した実行

```bash
# 設定ファイルを指定
uv run python hello_v2.py --config config.yaml

# JSON形式で出力
uv run python hello_v2.py --output-format json

# プラグインを使用
uv run python hello_v2.py --plugin weather --plugin quote

# 対話モードで実行
uv run python hello_v2.py --interactive
```

### プラグインヘルプ

```bash
# 利用可能なプラグインを表示
uv run python hello_v2.py --plugins-help

# 特定のプラグインヘルプ（対話モード内で）
# > plugins
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

```
gh-practice/
├── README.md                    # このファイル
├── hello.py                     # 基本的なPythonスクリプト
├── hello_v2.py                  # 拡張版スクリプト（設定・プラグイン対応）
├── config.yaml                  # 設定ファイル例
├── pyproject.toml              # プロジェクト設定（uv対応）
├── Makefile                    # 開発タスク
├── .github/workflows/ci.yml    # GitHub Actions CI設定
├── hello_project/              # メインパッケージ
│   ├── __init__.py
│   ├── config/                 # 設定管理
│   │   ├── __init__.py
│   │   └── settings.py
│   └── plugins/                # プラグインシステム
│       ├── __init__.py
│       ├── base.py            # プラグインベースクラス
│       ├── weather.py         # 天気プラグイン
│       └── quote.py           # 名言プラグイン
└── tests/                      # テストスイート
    ├── __init__.py
    ├── test_hello.py          # 基本スクリプトのテスト
    ├── test_config.py         # 設定管理のテスト
    └── test_plugins.py        # プラグインシステムのテスト
```

## 🔧 新機能の詳細

### 設定ファイル対応
- **pydantic** による型安全な設定管理
- **YAML/JSON** フォーマット対応
- **環境変数** による設定上書き
- 設定の**バリデーション**と**デフォルト値**

### プラグインシステム
- **拡張可能**なアーキテクチャ
- **内蔵プラグイン**（天気、名言）
- **外部プラグイン**の動的読み込み
- エラーハンドリングとフォールバック

### 対話モード
- **リアルタイム**コマンド実行
- プラグインとの**インタラクティブ**な操作
- ヘルプシステムと設定確認

### 出力フォーマット
- **テキスト**形式（デフォルト）
- **JSON**形式（API連携用）
- タイムスタンプ対応

## 📚 ドキュメント

詳細なドキュメントが利用可能です：

- **[完全なドキュメント](https://k-maeda03.github.io/gh-practice/)** - GitHub Pages
- **[APIリファレンス](https://k-maeda03.github.io/gh-practice/api/)** - 詳細なAPI仕様
- **[チュートリアル](https://k-maeda03.github.io/gh-practice/tutorials/)** - ステップバイステップガイド
- **[開発者ガイド](https://k-maeda03.github.io/gh-practice/development/)** - コントリビューション情報

### ローカルでドキュメントを構築

```bash
# ドキュメント依存関係をインストール
uv pip install -e ".[docs]"

# ドキュメントを構築
make docs

# ライブプレビュー（変更を監視）
make docs-live
```

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