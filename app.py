import threading
import time
import json
from flask import Flask, request, Response
from datetime import datetime
from telegram_utils import TelegramBot
from db_utils import DatabaseManager
from queue import Queue
from rediscluster import RedisCluster



token = "7334701342:AAHnfB9e1AUAEq2bIVmT1WmFVW9s_4325Pg"
class Worker(threading.Thread):
    def __init__(self, threadID,redis_cluster):
        super().__init__()
        self.threadID = threadID
        self.redis_cluster = redis_cluster
        self.thread_exit_flag = False

    def run(self):
        db_manager = DatabaseManager()
        tele=TelegramBot(token)
        while not self.thread_exit_flag:
            # Lấy dữ liệu từ Redis Queue
            message_data = self.redis_cluster.lpop('workQueue')
            if message_data:
                message_data = json.loads(message_data)
                tele.process_message_content(
                    message_data["chat_id"],
                    message_data["message_id"],
                    message_data["from_id"],
                    message_data["last_name"],
                    message_data["txt"],
                    message_data["msg"],
                    message_data["current_time"]
                )
                db_manager.save_user_to_db(message_data["first_name"], message_data["last_name"])
            else:
                time.sleep(1)

    def stop(self):
        self.thread_exit_flag = True

class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.redis_cluster = RedisCluster(startup_nodes=[
            {"host": "localhost", "port": "6123"},
            {"host": "localhost", "port": "6124"},
            {"host": "localhost", "port": "6125"}
        ], decode_responses=True)
        self.workers = []
        self.number_of_threads = 50
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            telebot = TelegramBot(token)
            if request.method == 'POST':
                msg = request.get_json()
                current_time = datetime.now().isoformat()

                chat_id, message_id, text, from_id, first_name, last_name, username, txt, photo, video, audio, document, caption = telebot.tel_parse_message(
                    msg)

                message_data = {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": text,
                    "from_id": from_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                    "txt": txt,
                    "photo": photo,
                    "video": video,
                    "audio": audio,
                    "document": document,
                    "caption": caption,
                    "msg": msg,
                    "current_time": current_time
                }

                # Đưa dữ liệu vào Redis Queue
                self.redis_cluster.rpush('workQueue', json.dumps(message_data))

                try:
                    file_id = telebot.tel_parse_get_message(msg)
                    telebot.tel_upload_file(file_id)
                except:
                    print("No file from index-->")

                return Response('ok', status=200)
            else:
                return "<h1>Welcome!</h1>"

    def start(self):
        db_manager = DatabaseManager()
        db_manager.create_table_user()
        db_manager.create_table_message()

        for i in range(self.number_of_threads):
            worker = Worker(i + 1, self.redis_cluster)
            worker.start()
            self.workers.append(worker)

        from waitress import serve
        serve(self.app, host="0.0.0.0", port=8080, threads=50)

        while not self.redis_cluster.llen('workQueue'):
            pass
        for worker in self.workers:
            worker.stop()
        for worker in self.workers:
            worker.join()

        print("Exit Main Thread")

if __name__ == '__main__':
    app = App()
    app.start()
