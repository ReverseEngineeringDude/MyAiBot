import telebot
import markdown
import re
import gemini
import os

TOKEN = 'Add you token here'

bot = telebot.TeleBot(TOKEN)

def escape_reserved_characters(text):
    reserved_characters = r'.^$*+?{}[]\|()-<>=!&$#'
    escaped_text = re.sub(f'([{re.escape(reserved_characters)}])', r'\\\1', text)
    return escaped_text

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am an Ai bot developed by @darker_m_t. ask me any question")

@bot.message_handler(func=lambda message: True)
def Ai_text_replay(message):
    wait_msg = bot.reply_to(message, "Please wait.. ")
    replay_ans = gemini.text_ai(message.text)
    escaped_response = escape_reserved_characters(replay_ans)
    bot.reply_to(message, escaped_response, parse_mode="MarkdownV2")
    bot.delete_message(wait_msg.chat.id, wait_msg.message_id)


@bot.message_handler(content_types=['photo'])
def reply_to_image(message):
    # Get the photo ID
    wait_msg = bot.reply_to(message, "Please wait.. ")
    photo_id = message.photo[-1].file_id
    
    # Get the image file
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Save the image file locally
    image_filename = f"image_{photo_id}.jpg"  # You might want to change this naming convention
    with open(image_filename, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    # Get the caption
    caption = message.caption
    
    if caption:
        # Process the image using gemini.image_ai() with the image file path and the caption
        img_res = gemini.image_ai(image_filename, caption)
        
        escaped_response = escape_reserved_characters(img_res)
        # print(escaped_response)
        bot.reply_to(message, escaped_response, parse_mode="MarkdownV2")
        
        # Delete the "Please wait..." message
        bot.delete_message(wait_msg.chat.id, wait_msg.message_id)
        
        # Clean up: Remove the image file after processing
        os.remove(image_filename)
    else:
        bot.reply_to(message, "Please add a caption and send again.")

print("Bot is Running....")
bot.polling()
