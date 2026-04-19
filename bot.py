import requests
import time

TOKEN = "8676719325:AAHy7EvOB1MVyQhQr5pbqr-wQe_Vx6kfOMk"
URL = f"https://api.telegram.org/bot{TOKEN}"

savollar = [
    ("O'zbekiston poytaxti?", "A", ["A) Toshkent", "B) Moskva", "C) London", "D) Parij"]),
    ("2 + 2 = ?", "B", ["A) 3", "B) 4", "C) 5", "D) 6"]),
    ("Python nima?", "C", ["A) O'yin", "B) Telefon", "C) Dasturlash tili", "D) Film"]),
    ("Yer nechanchi sayyora?", "A", ["A) 3", "B) 2", "C) 5", "D) 1"]),
    ("Eng katta okean?", "B", ["A) Atlantika", "B) Tinch", "C) Hind", "D) Shimoliy"]),
    ("5 * 5 = ?", "D", ["A) 10", "B) 15", "C) 20", "D) 25"]),
    ("Suv formulasi?", "A", ["A) H2O", "B) CO2", "C) O2", "D) N2"]),
    ("1 yil nechta oy?", "B", ["A) 10", "B) 12", "C) 11", "D) 13"])
]

user_data = {}
last_update = 0


def send(chat_id, text):
    requests.get(URL + f"/sendMessage?chat_id={chat_id}&text={text}")


def send_question(chat_id):
    data = user_data[chat_id]
    i = data["index"]

    if i >= len(savollar):
        send(chat_id, f"🏁 Tugadi!\nBall: {data['ball']}/8")
        return

    savol, _, variantlar = savollar[i]

    text = f"⏱ Savol {i+1}:\n{savol}\n\n" + "\n".join(variantlar)
    send(chat_id, text)

    data["time"] = time.time()


print("Bot ishlayapti...")

while True:
    try:
        res = requests.get(URL + f"/getUpdates?offset={last_update}").json()

        for upd in res["result"]:
            last_update = upd["update_id"] + 1

            if "message" in upd:
                chat_id = upd["message"]["chat"]["id"]
                text = upd["message"].get("text", "").upper()

                if text == "/START":
                    user_data[chat_id] = {
                        "index": 0,
                        "ball": 0,
                        "time": time.time()
                    }
                    send(chat_id, "🤖 Quiz boshlandi! Har savolga 10 soniya!")
                    send_question(chat_id)

                elif chat_id in user_data:
                    i = user_data[chat_id]["index"]
                    correct = savollar[i][1]

                    # 10 SONIYA TIMER
                    if time.time() - user_data[chat_id]["time"] > 10:
                        send(chat_id, "⏰ Vaqt tugadi!")
                    else:
                        if text == correct:
                            user_data[chat_id]["ball"] += 1
                            send(chat_id, "✅ To'g'ri!")
                        else:
                            send(chat_id, f"❌ Noto'g'ri! Javob: {correct}")

                    user_data[chat_id]["index"] += 1
                    send_question(chat_id)

        time.sleep(1)

    except:
        time.sleep(2)
