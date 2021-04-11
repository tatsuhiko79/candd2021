# for WSGI
from flask import Flask, jsonify, request
# for Application
import boto3
import logging
import datetime
import time
import os
# ログの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Flask
app = Flask(__name__)

# DynamoDBオブジェクトの作成
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('TABLENAME'))


@app.route("/", methods=["GET"])
def root():
    result = scan()
    logger.info(f'result: {result}')
    return result


@app.route("/<id>/<name>", methods=['GET', 'POST', 'DELETE'])
def dbaction(id: str, name: str):
    logger.info('=== request')

    if request.method == 'GET':
        logger.info('=== GET')
        result = query(id, name)

    elif request.method == 'POST':
        logger.info('=== POST')
        logger.info(f'headers: {request.headers}')
        event = request.json
        result = put(id, name, event)

    elif request.method == 'DELETE':
        logger.info('=== DELETE')
        delta = datetime.timedelta(seconds=10)
        result = delete(id, name, delta)

    # API GWからの引数
    logger.info(f'event: {request.environ["serverless.event"]}')

    logger.info(f'result: {result}')
    return jsonify(
        {
            'message': 'Success',
            'id': f'{id}',
            'result': f'{result}',
        }), 200


def put(id: str, name: str, data: dict):
    """DyanmoDBにデータを登録する

    Args:
        id (str): ハッシュキー
        name (str): ソートキー
        data (dict): 登録データ
    """
    table.put_item(
        Item={
            "Id": id,
            "Name": name,
            "data": data
        }
    )


def query(id: str, name: str):
    """指定したデータを取得する

    Args:
        id (str): ハッシュキー
        name (str): ソートキー

    Returns:
        dict: 実行結果
    """
    result = table.get_item(
        Key={
            'Id': id,
            'Name': name,
        }
    )
    return result


def scan():
    """DynamoDBから全件検索する関数

    Returns:
        dict: 削除結果
    """
    result = table.scan()
    return result


def delete(id: str, name: str, delta: datetime.timedelta):
    """DynamoDBのTTLキーに現在時刻から引数秒後に削除するカラムを設定する

    Args:
        id (str): ハッシュキー
        name (str): ソートキー
        delta (datetime.timedelta): 何秒後に削除するか

    Returns:
        dict: 削除結果
    """
    deleteAt = datetime.datetime.now() + delta
    epoc = int(time.mktime(deleteAt.timetuple()))
    result = table.update_item(
        Key={
            'Id': id,
            'Name': name
        },
        UpdateExpression="SET #attribute = :val",
        ExpressionAttributeNames={
            # UpadateExpressionで使っている#attributeを置き換える
            '#attribute': "ExpirationTime"
        },
        ExpressionAttributeValues={
            # UpadateExpressionで使っている:valを実際の値で置き換える
            ':val': epoc
        },
        # 戻り値で返す情報
        ReturnValues="UPDATED_NEW"

    )
    return result
