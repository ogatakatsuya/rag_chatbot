# 履修支援チャットボット

大阪大学の履修登録を支援するためのチャットボットプロジェクト

## 起動方法

1. 以下を実行して環境変数を格納する

```sh
cp .env.sample .env
```

2. コンテナをビルドして立ち上げる

```sh
docker compose up --build
```

3. streamlitのサイトにアクセス

```sh
http://localhost:8501
```
