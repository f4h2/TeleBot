from flask import Flask, request, Response
from datetime import datetime
from telegram_utils import tel_parse_message, tel_send_message, tel_parse_get_message, tel_upload_file, \
    process_message_content
from db_utils import create_table_user, create_table_message, save_message_to_db_message, save_user_to_db
from utils import write_json
from queue import Queue
from threading import Thread

app = Flask(__name__)
q = Queue(maxsize=0)


def worker():
    while True:
        message_data = q.get()
        if message_data is None:
            break
        process_message_content(
            message_data["chat_id"],
            message_data["message_id"],
            message_data["from_id"],
            message_data["last_name"],
            message_data["txt"],
            message_data["msg"],
            message_data["current_time"]
        )
        q.task_done()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        current_time = datetime.now()

        chat_id, message_id, text, from_id, first_name, last_name, username, txt, photo, video, audio, document, caption = tel_parse_message(
            msg)
        save_user_to_db(first_name, last_name)
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
        q.put(message_data)

        try:
            file_id = tel_parse_get_message(msg)
            tel_upload_file(file_id)
        except:
            print("No file from index-->")

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


if __name__ == '__main__':
    create_table_user()
    create_table_message()
    num_threads = 2000
    threads = []
    for i in range(num_threads):
        thread = Thread(target=worker)
        thread.daemon = True
        thread.start()
        threads.append(thread)

    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)

    for thread in threads:
        q.put(None)
    for thread in threads:
        thread.join()
