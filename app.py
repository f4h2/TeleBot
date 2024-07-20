from flask import Flask, request, Response
from datetime import datetime
from telegram_utils import tel_parse_message, tel_send_message, tel_send_image, tel_send_poll, tel_send_button, tel_send_audio, tel_send_document, tel_send_video, tel_send_inlinebutton, tel_send_inlineurl, tele_read_news, teleSearchGoogle, tel_parse_get_message, tel_upload_file
from db_utils import create_table_user, create_table_message, save_message_to_db_message, save_user_to_db
from utils import write_json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        current_time = datetime.now()
        try:
            chat_id, message_id, text, from_id, first_name, last_name, username, txt, photo, video, audio, document, caption = tel_parse_message(msg)
            save_user_to_db(first_name, last_name)

            if txt == "hi":
                tel_send_message(chat_id, "Hello, world!")
                save_message_to_db_message(message_id, from_id, last_name, txt, "Hello, world!", current_time)
            elif txt == "image":
                r, t = tel_send_image(chat_id)
                save_message_to_db_message(message_id, from_id, last_name, txt, t, current_time)
            elif txt == "poll":
                tel_send_poll(chat_id)
                save_message_to_db_message(message_id, from_id, last_name, txt, "poll", current_time)
            elif txt == "button":
                tel_send_button(chat_id)
                save_message_to_db_message(message_id, from_id, last_name, txt, "button", current_time)
            elif txt == "audio":
                r, t = tel_send_audio(chat_id)
                save_message_to_db_message(message_id, from_id, last_name, txt, t, current_time)
            elif txt == "file":
                r, t = tel_send_document(chat_id)
                save_message_to_db_message(message_id, from_id, last_name, txt, t, current_time)
            elif txt == "video":
                r, t = tel_send_video(chat_id)
                save_message_to_db_message(message_id, from_id, last_name, txt, t, current_time)
            elif txt == "inline":
                tel_send_inlinebutton(chat_id)
                save_message_to_db_message(message_id, from_id, last_name, txt, "inline", current_time)
            elif txt == "inlineurl":
                tel_send_inlineurl(chat_id)
                save_message_to_db_message(message_id, from_id, last_name, txt, "inlineurl", current_time)
            elif txt == "ic_A":
                tel_send_message(chat_id, "You have clicked A")
                save_message_to_db_message(message_id, from_id, last_name, txt, "You have clicked A", current_time)
            elif txt == "ic_B":
                tel_send_message(chat_id, "You have clicked B")
                save_message_to_db_message(message_id, from_id, last_name, txt, "You have clicked B", current_time)
            elif txt == "read_new":
                r, str1 = tele_read_news(chat_id)
                save_message_to_db_message(message_id, from_id, last_name, txt, str1, current_time)
            else:
                write_json(msg, 'xxx.json')
                response, image_url = teleSearchGoogle(chat_id, txt)
                if response.status_code == 200:
                    tel_send_message(chat_id, 'from webhook')
                else:
                    image_url = "Failed to get URL"
                save_message_to_db_message(message_id, from_id, last_name, txt, image_url, current_time)
        except:
            print("fromindex-->")

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
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
    app.run(threaded=True)