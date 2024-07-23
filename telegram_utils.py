import requests
import json
from bs4 import BeautifulSoup
from utils import write_json
from db_utils import save_message_to_db_message

TOKEN = "7334701342:AAHnfB9e1AUAEq2bIVmT1WmFVW9s_4325Pg"

def tel_parse_get_message(message):
    print("message-->", message)

    try:
        g_chat_id = message['message']['chat']['id']
        g_file_id = message['message']['photo'][0]['file_id']
        print("g_chat_id-->", g_chat_id)
        print("g_image_id-->", g_file_id)

        return g_file_id
    except:
        try:
            g_chat_id = message['message']['chat']['id']
            g_file_id = message['message']['video']['file_id']
            print("g_chat_id-->", g_chat_id)
            print("g_video_id-->", g_file_id)

            return g_file_id
        except:
            try:
                g_chat_id = message['message']['chat']['id']
                g_file_id = message['message']['audio']['file_id']
                print("g_chat_id-->", g_chat_id)
                print("g_audio_id-->", g_file_id)

                return g_file_id
            except:
                try:  # if the file is a document
                    g_chat_id = message['message']['chat']['id']
                    g_file_id = message['message']['document']['file_id']
                    print("g_chat_id-->", g_chat_id)
                    print("g_file_id-->", g_file_id)

                    return g_file_id
                except:
                    print("NO file found found-->>")


def tel_parse_message(message):
    print("message-->", message)

    try:
        chat_id = message['message']['chat']['id']
        message_id = message['message']['message_id']
        from_id = message['message']['from']['id']
        first_name = message['message']['from'].get('first_name', 'Unknown')
        last_name = message['message']['from'].get('last_name', '')
        username = message['message']['from'].get('username', 'Unknown')
        text = message['message'].get('text', '')
        photo = message['message'].get('photo', [])
        video = message['message'].get('video', {})
        audio = message['message'].get('audio', {})
        document = message['message'].get('document', {})
        caption = message['message'].get('caption', '')

        return chat_id,message_id, text, from_id, first_name, last_name, username, text, photo, video, audio, document, caption

    except KeyError as e:
        print(f"KeyError: {e} - Missing key in message")
    except Exception as e:
        print(f"Error: {e}")

    try:
        callback_id = message['callback_query']['id']
        callback_from_id = message['callback_query']['from']['id']
        callback_first_name = message['callback_query']['from'].get('first_name', 'Unknown')
        callback_last_name = message['callback_query']['from'].get('last_name', '')
        callback_username = message['callback_query']['from'].get('username', 'Unknown')
        callback_data = message['callback_query']['data']

        print(f"callback_id: {callback_id}")
        print(f"callback_from_id: {callback_from_id}")
        print(f"callback_first_name: {callback_first_name}")
        print(f"callback_last_name: {callback_last_name}")
        print(f"callback_username: {callback_username}")
        print(f"callback_data: {callback_data}")

        # Trả về thông tin cần thiết
        return callback_from_id, callback_data

    except KeyError as e:
        print(f"KeyError: {e} - Missing key in callback_query")
    except Exception as e:
        print(f"Error: {e}")

    return None, None


def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(url, json=payload)
    return r


def tel_send_image(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    t = "https://admin.vov.gov.vn/UploadFolder/KhoTin/Images/UploadFolder/VOVVN/Images/sites/default/files/styles/large/public/2024-02/vu%20tru.jpg"
    payload = {
        'chat_id': chat_id,
        'photo': t
    }
    r = requests.post(url, json=payload)
    return r,t


def tel_send_poll(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPoll'
    payload = {
        'chat_id': chat_id,
        "question": "In which direction does the sun rise?",
        "options": json.dumps(["North", "South", "East", "West"]),
        "is_anonymous": False,
        "type": "quiz",
        "correct_option_id": 2
    }
    r = requests.post(url, json=payload)
    return r


def tel_send_button(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': "What is this?",
        'reply_markup': {
            'keyboard': [[
                {
                    'text': 'supa'
                },
                {
                    'text': 'mario'
                }
            ]]
        }
    }
    r = requests.post(url, json=payload)
    return r


def tel_send_inlinebutton(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': "What is this?",
        'reply_markup': {
            "inline_keyboard": [[
                {
                    "text": "A",
                    "callback_data": "ic_A"
                },
                {
                    "text": "B",
                    "callback_data": "ic_B"
                }]
            ]
        }
    }
    r = requests.post(url, json=payload)
    return r


def tel_send_inlineurl(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': "Which link would you like to visit?",
        'reply_markup': {
            "inline_keyboard": [
                [
                    {"text": "google", "url": "http://www.google.com/"},
                    {"text": "youtube", "url": "http://www.youtube.com/"}
                ]
            ]
        }
    }
    r = requests.post(url, json=payload)
    return r


def tel_send_audio(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendAudio'
    t = "http://www.largesound.com/ashborytour/sound/brobob.mp3"
    payload = {
        'chat_id': chat_id,
        "audio": t,
    }
    r = requests.post(url, json=payload)
    return r,t


def tel_send_document(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
    t = "http://www.africau.edu/images/default/sample.pdf"
    payload = {
        'chat_id': chat_id,
        "document": t
    }
    r = requests.post(url, json=payload)
    return r,t


def tel_send_video(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendVideo'
    t = "https://www.appsloveworld.com/wp-content/uploads/2018/10/640.mp4"
    payload = {
        'chat_id': chat_id,
        "video": t
    }
    r = requests.post(url, json=payload)
    return r,t

def tel_upload_file(file_id):
    url = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'
    a = requests.post(url)
    json_resp = json.loads(a.content)
    print("json_resp-->", json_resp)
    file_pathh = json_resp['result']['file_path']
    print("file_pathh-->", file_pathh)
    url_1 = f'https://api.telegram.org/file/bot{TOKEN}/{file_pathh}'
    b = requests.get(url_1)
    file_content = b.content
    with open(file_pathh, "wb") as f:
        f.write(file_content)


################ get new

def get_news():
    list_news = []
    r = requests.get("https://vnexpress.net/")
    soup = BeautifulSoup(r.text, 'html.parser')
    mydivs = soup.find_all("h3", {"class": "title-news"})

    for new in mydivs:
        newdict = {}
        newdict["link"] = new.a.get("href")
        newdict["title"] = new.a.get("title")
        list_news.append(newdict)
    return list_news


def tele_read_news(chat_id):
    data = get_news()
    str1 = ""
    for item in data:
        str1 += item["title"] + "\n"

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': str1
    }
    r = requests.post(url, json=payload)
    return r,str1
############### searchGoogle
def searchGoogle(textSearch):
    API_KEY = "AIzaSyBThrlj9oA0Zjmz-LFL3ZTWEv1xcBsKbuE"          # https://console.cloud.google.com/apis/credentials?project=testsearch-429915
    SEARCH_ENGINE_ID = "705ae1e64eda449fc"                       # https://programmablesearchengine.google.com/controlpanel/overview?cx=705ae1e64eda449fc
    search_query = textSearch
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'searchType': 'image'
    }
    response = requests.get(url, params=params)
    results = response.json().get('items', [])
    image_urls = [item['link'] for item in results if 'link' in item]
    return image_urls


def teleSearchGoogle(chat_id, textSearch):
    image_urls = searchGoogle(textSearch)
    if not image_urls:
        return tel_send_message(chat_id, 'No images found for your search.')

    first_image_url = image_urls[0]
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': first_image_url
    }
    r = requests.post(url, json=payload)
    return r, first_image_url
###############################


def process_message_content(chat_id, message_id, from_id, last_name, txt, msg, current_time):
    if txt == "hi":
        tel_send_message(chat_id, "Hello, world!")
        save_message_to_db_message(message_id, from_id, last_name, txt, "Hello, world!", current_time)
    elif txt == "image":
        print("Sending image...")
        r, t = tel_send_image(chat_id)
        print(f"Image sent: {t}")
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