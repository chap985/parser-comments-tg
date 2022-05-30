import os
import sys
import json

from telethon.sync import TelegramClient, events

from config import API_ID, API_HASH



class Converted:

	def __init__(self, message, name, post_id):
		self.msg = message
		self.name = name
		self.post_id = post_id

	def convertedJson(self):
		message = json.dumps(
			self.msg.to_dict(), sort_keys=True, indent=2,
			default=str, ensure_ascii=False)
		
		with open(f"jsonData/{self.name}_{self.post_id}.json", "a", encoding="utf-8") as file:
			file.write(f"{message}\n")

	def convertedText(self):
		"""
		В отличии от json содержит в себе только datetime, userId, message.text
		"""
		msg = {
			f"{self.msg.sender.id}": {
				"username": self.msg.sender.username,
				"datetime": self.msg.date,
				"text": self.msg.text
			}
		}
		message = json.dumps(
			msg, sort_keys=True, indent=2,
			default=str, ensure_ascii=False)
		
		with open(f"txtData/{self.name}_{self.post_id}.txt", "a", encoding="utf-8") as file:
			file.write(f"{message}\n")


def worker(info) -> None:
	print("[+] Parsing comments")
	
	for message in client.iter_messages(info[-2], reply_to=int(info[-1]), reverse=True):
		print(f"[*] load {message.sender.id}: {message.text}")
		cJson = Converted(message, info[-2], info[-1]).convertedJson()
		cText = Converted(message, info[-2], info[-1]).convertedText()
	
	print(f"[+] File {info[-2]}_{info[-1]} successfully saved.")

with TelegramClient('sessions/session', API_ID, API_HASH) as client:
	while True:
		channel = input("link to post (format: https://t.me/<name_channel>/<post_id>): ")
		worker = worker(channel.split("/"))
		nexted = input("\n[Y/n] Continue work?: ")
		if nexted == "n":
			sys.exit()
	
	client.run_until_disconnected()