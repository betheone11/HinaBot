from flask import Flask, request
import requests
import afan

app = Flask(__name__)


class API:
    @staticmethod
    def send(message):
        url = "http://127.0.0.1:5700/send_msg"  # 这里要加上http://，不然会报错
        data = request.get_json()  # 获取上报消息
        params = {
            "message_type": data['message_type'],
            "group_id": data['group_id'],
            "message": message
        }
        requests.get(url, params=params)


@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    print(data)
    if data['post_type'] == 'message':

        message = data['message']
        print(message)
        afan.messagex()
    else:
        print("忽略消息")

    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5701)


