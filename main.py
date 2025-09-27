import telebot
from model import classification
import os
from detect_object import detect_all_objects, analyze_objects

bot = telebot.TeleBot("8358496498:AAFW9Ii5UOinK8PFGBfeslUqWmYGlzMbCrQ")

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, f'Привет! Я бот {bot.get_me().first_name}!')

@bot.message_handler(content_types=['photo'])
def photo(message):
    if message.photo:

        file_info = bot.get_file(message.photo[-1].file_id)
        print(file_info)
        file_name = file_info.file_path.split('/')[-1]
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        res_func = classification('./models/keras_model.h5', './models/labels.txt', file_name)


        detections = detect_all_objects(file_name, "./models/yolov3.pt")
        find_obj = analyze_objects(detections)

        if find_obj == []:
            bot.reply_to(message, "I'm not really sure if the picture shows a bird. Try sending another message.")

            if res_func[0] == "УТОМА":
                name = str.lower(res_func[0].replace('\n', ''))
                score = int(res_func[1] * 100)

                if score >= 51:
                    result_message = f"This bird belongs to the {name} class, with a probability of {score}%"
                    bot.reply_to(message, result_message)
                else:
                    bot.reply_to(message, "I'm not sure what's in the picture. Try sending another one")
                    
        elif len(detections) >= 0:

            name = str.lower(res_func[0].replace('\n', ''))
            score = int(res_func[1] * 100)

            if score >= 51:
                result_message = f"This bird belongs to the {name} class, with a probability of {score}%"
                bot.reply_to(message, result_message)
            else:
                bot.reply_to(message, "I'm not sure what's in the picture. Try sending another one")
            os.remove(file_name)

    else:
        bot.reply_to(message, "You didn't send the image.")

bot.polling()