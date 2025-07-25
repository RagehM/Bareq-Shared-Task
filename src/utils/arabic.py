import re

def remove_diacritics(text):
	arabic_diacritics = re.compile(r'[\u0617-\u061A\u064B-\u0652\u0670]')
	return re.sub(arabic_diacritics, '', text)