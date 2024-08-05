import requests
import json
from bs4 import BeautifulSoup
from utils import JSONHandler
from db_utils import DatabaseManager



class TelegramBot:
    def __init__(self, token):
        self.token = token

    def _send_request(self, method, payload):
        url = f'https://api.telegram.org/bot{self.token}/{method}'
        response = requests.post(url, json=payload)
        return response

    def tel_parse_get_message(self, message):
        print("message-->", message)
        try:
            g_chat_id = message['message']['chat']['id']
            file_id = message['message'].get('photo', [{}])[0].get('file_id') or \
                      message['message'].get('video', {}).get('file_id') or \
                      message['message'].get('audio', {}).get('file_id') or \
                      message['message'].get('document', {}).get('file_id')
            if file_id:
                print("g_chat_id-->", g_chat_id)
                print("g_file_id-->", file_id)
                return file_id
        except:
            print("NO file found-->>")
        return None

    def tel_parse_message(self, message):
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

            return chat_id, message_id, text, from_id, first_name, last_name, username, text, photo, video, audio, document, caption

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

            return callback_from_id, callback_data

        except KeyError as e:
            print(f"KeyError: {e} - Missing key in callback_query")
        except Exception as e:
            print(f"Error: {e}")

        return None, None

    def tel_send_message(self, chat_id, text):
        payload = {'chat_id': chat_id, 'text': text}
        return self._send_request('sendMessage', payload)

    def tel_send_image(self, chat_id):
        payload = {'chat_id': chat_id, 'photo': "https://admin.vov.gov.vn/UploadFolder/KhoTin/Images/UploadFolder/VOVVN/Images/sites/default/files/styles/large/public/2024-02/vu%20tru.jpg"}
        response = self._send_request('sendPhoto', payload)
        return response, payload['photo']

    def tel_send_poll(self, chat_id):
        payload = {
            'chat_id': chat_id,
            "question": "In which direction does the sun rise?",
            "options": json.dumps(["North", "South", "East", "West"]),
            "is_anonymous": False,
            "type": "quiz",
            "correct_option_id": 2
        }
        return self._send_request('sendPoll', payload)

    def tel_send_button(self, chat_id):
        payload = {
            'chat_id': chat_id,
            'text': "What is this?",
            'reply_markup': {
                'keyboard': [[{'text': 'supa'}, {'text': 'mario'}]]
            }
        }
        return self._send_request('sendMessage', payload)

    def tel_send_inlinebutton(self, chat_id):
        payload = {
            'chat_id': chat_id,
            'text': "What is this?",
            'reply_markup': {
                "inline_keyboard": [[
                    {"text": "A", "callback_data": "ic_A"},
                    {"text": "B", "callback_data": "ic_B"}
                ]]
            }
        }
        return self._send_request('sendMessage', payload)

    def tel_send_inlineurl(self, chat_id):
        payload = {
            'chat_id': chat_id,
            'text': "Which link would you like to visit?",
            'reply_markup': {
                "inline_keyboard": [
                    [{"text": "google", "url": "http://www.google.com/"},
                     {"text": "youtube", "url": "http://www.youtube.com/"}]
                ]
            }
        }
        return self._send_request('sendMessage', payload)

    def tel_send_audio(self, chat_id):
        payload = {
            'chat_id': chat_id,
            "audio": "http://www.largesound.com/ashborytour/sound/brobob.mp3",
        }
        response = self._send_request('sendAudio', payload)
        return response, payload["audio"]

    def tel_send_document(self, chat_id):
        payload = {
            'chat_id': chat_id,
            "document": "http://www.africau.edu/images/default/sample.pdf"
        }
        response = self._send_request('sendDocument', payload)
        return response, payload["document"]

    def tel_send_video(self, chat_id):
        payload = {
            'chat_id': chat_id,
            "video": "https://www.appsloveworld.com/wp-content/uploads/2018/10/640.mp4"
        }
        response = self._send_request('sendVideo', payload)
        return response, payload["video"]

    def tel_upload_file(self, file_id):
        url = f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}'
        response = requests.post(url)
        json_resp = response.json()
        file_path = json_resp['result']['file_path']
        file_url = f'https://api.telegram.org/file/bot{self.token}/{file_path}'
        file_content = requests.get(file_url).content
        with open(file_path, "wb") as f:
            f.write(file_content)

    def get_news(self):
        list_news = []
        response = requests.get("https://vnexpress.net/")
        soup = BeautifulSoup(response.text, 'html.parser')
        news_divs = soup.find_all("h3", {"class": "title-news"})

        for news in news_divs:
            news_dict = {}
            news_dict["link"] = news.a.get("href")
            news_dict["title"] = news.a.get("title")
            list_news.append(news_dict)
        return list_news

    def tele_read_news(self, chat_id):
        data = self.get_news()
        news_str = "\n".join(item["title"] for item in data)
        payload = {'chat_id': chat_id, 'text': news_str}
        response = self._send_request('sendMessage', payload)
        return response, news_str

    def searchGoogle(self, textSearch):
        API_KEY = "AIzaSyAxQ78Jk6iqUD2bCKsleEPWBjy8VXKBaQA"
        SEARCH_ENGINE_ID = "80854a8a4f95a4634"
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

    def teleSearchGoogle(self, chat_id, textSearch):
        image_urls = self.searchGoogle(textSearch)
        if not image_urls:
            return self.tel_send_message(chat_id, 'No images found for your search.')
        first_image_url = image_urls[0]
        payload = {'chat_id': chat_id, 'photo': first_image_url}
        response = self._send_request('sendPhoto', payload)
        return response, first_image_url

    ###############################
    def process_message_content(self, chat_id, message_id, from_id, last_name, txt, msg, current_time):
        database = DatabaseManager()
        # jsonhandler = JSONHandler()
        processed_message_ids = set()
        if message_id in processed_message_ids:
            return
        processed_message_ids.add(message_id)
        if txt == "hi":
            self.tel_send_message(chat_id, "Hello, world!")
            database.save_message_to_db_message(message_id, from_id, last_name, txt, "Hello, world!", current_time)
        elif txt == "image":
            print("Sending image...")
            r, t = self.tel_send_image(chat_id)
            print(f"Image sent: {t}")
            database.save_message_to_db_message(message_id, from_id, last_name, txt, t, current_time)
        elif txt == "poll":
            self.tel_send_poll(chat_id)
            database.save_message_to_db_message(message_id, from_id, last_name, txt, "poll", current_time)
        elif txt == "button":
            self.tel_send_button(chat_id)
            database.save_message_to_db_message(message_id, from_id, last_name, txt, "button", current_time)
        elif txt == "audio":
            r, t = self.tel_send_audio(chat_id)
            database.save_message_to_db_message(message_id, from_id, last_name, txt, t, current_time)
        elif txt == "file":
            r, t = self.tel_send_document(chat_id)
            database.save_message_to_db_message(message_id, from_id, last_name, txt, t, current_time)
        elif txt == "video":
            r, t = self.tel_send_video(chat_id)
            database.save_message_to_db_message(message_id, from_id, last_name, txt, t, current_time)
        elif txt == "inline":
            self.tel_send_inlinebutton(chat_id)
            database.save_message_to_db_message(message_id, from_id, last_name, txt, "inline", current_time)
        elif txt == "inlineurl":
            self.tel_send_inlineurl(chat_id)
            database.save_message_to_db_message(message_id, from_id, last_name, txt, "inlineurl", current_time)
        elif txt == "ic_A":
            self.tel_send_message(chat_id, "You have clicked A")
            database.save_message_to_db_message(message_id, from_id, last_name, txt, "You have clicked A", current_time)
        elif txt == "ic_B":
            self.tel_send_message(chat_id, "You have clicked B")
            database.save_message_to_db_message(message_id, from_id, last_name, txt, "You have clicked B", current_time)
        elif txt == "read_new":
            r, str1 = self.tele_read_news(chat_id)
            print(f"đây là r: {r}")
            database.save_message_to_db_message(message_id, from_id, last_name, txt, str1, current_time)
        else:
            # jsonhandler.write_json(msg, 'xxx.json')
            response, image_url = self.teleSearchGoogle(chat_id, txt)
            if response.status_code == 200:
                self.tel_send_message(chat_id, 'from webhook')
            else:
                image_url = "Failed to get URL"
            database.save_message_to_db_message(message_id, from_id, last_name, txt, image_url, current_time)
