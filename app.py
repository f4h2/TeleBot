import threading
import time
from flask import Flask, request, Response
from datetime import datetime
from telegram_utils import tel_parse_message, tel_send_message, tel_parse_get_message, tel_upload_file, \
    process_message_content
from db_utils import create_table_user, create_table_message, save_message_to_db_message, save_user_to_db
from queue import Queue

app = Flask(__name__)
workQueue = Queue(maxsize=500)


thread_exit_Flag = False

class SampleThread(threading.Thread):
    def __init__(self, threadID, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q

    def run(self):
        worker(self.q)

def worker(q):
    while not thread_exit_Flag:
        # queueLock.acquire()
        # try:
            if not workQueue.empty():
                message_data = q.get()
                process_message_content(
                    message_data["chat_id"],
                    message_data["message_id"],
                    message_data["from_id"],
                    message_data["last_name"],
                    message_data["txt"],
                    message_data["msg"],
                    message_data["current_time"]
                )
                save_user_to_db(message_data["first_name"], message_data["last_name"])
            else:
                time.sleep(1)
        # finally:
        #     queueLock.release()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        current_time = datetime.now()

        chat_id, message_id, text, from_id, first_name, last_name, username, txt, photo, video, audio, document, caption = tel_parse_message(
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
        workQueue.put(message_data)
        # queueLock.acquire()
        # try:
        #     workQueue.put(message_data)
        # finally:
        #     queueLock.release()

        try:
            file_id = tel_parse_get_message(msg)
            tel_upload_file(file_id)
        except:
            print("No file from index-->")

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"

# queueLock = threading.Lock()
threads = []
threadID = 1
number_thread = 50

if __name__ == '__main__':
    create_table_user()
    create_table_message()

    for _ in range(number_thread):
        thread = SampleThread(threadID, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    from waitress import serve
    serve(app, host="0.0.0.0", port=8080, threads=50)

    while not workQueue.empty():
        pass

    thread_exit_Flag = True

    for t in threads:
        t.join()
    print("Exit Main Thread")

    # for thread in threads:
    #     q.put(None)
    # for thread in threads:
    #     thread.join()
