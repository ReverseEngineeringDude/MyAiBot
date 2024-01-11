from googletrans import Translator

data = "ningalkk sugamano"

trans = Translator()
translated_text = trans.translate(data, src="ml", dest="en")
print(translated_text.text)



