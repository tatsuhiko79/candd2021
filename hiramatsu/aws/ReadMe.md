# ServerlessFramework + Flask + DynamoDb

## 概要
DynamoDbを読み書きするAPIを提供します

### 構成
- フロントエンド:Flask
- バックエンド:Python3
- DB:DynamoDB
- プロビジョニング: ServerlessFramework

## 使い方

- 登録内容を全て取得
    ```
    curl <API GW URL>
    ```

- キーを指定して取得
    ```
    curl <API GW URL>/<id>/<name>
    id  : ハッシュキー
    name: ソートキー
    ```

- キーを指定して登録
    ```
    curl <API GW URL>/<id>/<name> -d '{"obj":{"key1":"value1", "key2":"value2"}}' -H 'Content-Type: application/json' -X POST
    ```
    - windowsの場合、ダブルクォートはエスケープが必要
    ```
    curl <API GW URL>/<id>/<name> -d "{\"obj\":{\"key1\":\"value1\", \"key2\":\"value2\"}}" -H "Content-Type: application/json" -X POST
    ```

- データ削除(TTLカラムの追加)
    ```
    curl <API GW URL>/<id>/<name> -X DELETE
    ```

## 開発者向け利用方法

### 各種ツールのインストール
- Serverless Framework
- AWS CLI
- node.js
- python

### 準備
```
git clone <repo>
cd dynamodbsample
npm i
```

### デプロイ

    serverless deploy -v --aws-profile <profile>

### 片付け

    serverless remove -v --aws-profile <profile>


## 参考
### プロジェクトの生成

```
serverless create --template aws-python3 --name dynamodbsample --path dynamodbsample
cd dynamodbsample
npm i --save-dev serverless-python-requirements
npm i --save-dev serverless-wsgi
```

