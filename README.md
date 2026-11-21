# ORBIT SIEGE

リアルタイムで銀河を奪い合う宇宙戦略ゲーム（HTML1ファイル・外部ライブラリなし）。

## 構成
- `src/game.html` … ゲーム本体（Claudeのアーティファクトとして公開している形そのまま）
- `tools/build.py` … `src/game.html` を完全なHTML＋PWAに包んで `public/` に出力し、itch.io用の `dist/orbit-siege-web.zip` を作る
- `tools/sw.template.js` … オフライン用のService Worker（ビルドで版番号が入る）
- `public/` … 公開するもの一式（GitHub Pages はこのフォルダを公開）
- `store/` … itch.io の説明文・カバー画像・バナー

## ビルド
```sh
python3 tools/build.py
```

## 公開
- itch.io：`dist/orbit-siege-web.zip` を「HTML」プロジェクトとしてアップロード（`store/itch-page.md` 参照）
- GitHub Pages：`public/` を公開（Actions のワークフロー `.github/workflows/pages.yml`）

## 保存データ
ブラウザの localStorage（`orbitSiegeMeta`・`orbitSiegeBest3`）。公開先のドメインごとに別になる。
