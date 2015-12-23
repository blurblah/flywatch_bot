# -*- coding: utf-8 -*-
import telepot
import logging
import time

CMD_START = "/start"
CMD_REG = "/reg"
CMD_UNREG = "/unreg"
CMD_LIST = "/list"
CMD_HELP = "/help"

bot = telepot.Bot('168334744:AAGES7dIVbO9II40cn2t-48k-q5EVYzOhEM')

def main():
	bot.notifyOnMessage(handle)
	print "Listening..."
	while 1:
		time.sleep(10)
		# check crawling data and send message

def showHelp(chatId):
	USAGE = u"""[사용법] 아래 명령어대로 입력하세요.
	/reg keyword - (keyword 등록)
	/unreg keyword - (keyword 제거)
	/list - (등록된 keyword)
	/help - (도움말 보여주기)
	"""
	bot.sendMessage(chatId, USAGE)

def registerKeyword(chatId, keyword):
	print "키워드", keyword, "등록 완료."

def unregisterKeyword(chatId, keyword):
	print "키워드", keyword, "제거 완료."

def showKeywordList(chatId):
	pass

def handle(msg):
	print msg
	content_type, chat_type, chat_id = telepot.glance2(msg)
	if content_type == 'text':
		tokens = msg['text'].split(' ')
		command = tokens[0].lower()
		keyword = msg['text'][len(command):].lstrip().rstrip()
		if command == CMD_START:
			showHelp(chat_id)
		if command == CMD_REG:
			# register keyword
			registerKeyword(chat_id, keyword)
		elif command == CMD_LIST:
			# show registered keyword
			showKeywordList(chat_id)
		elif command == CMD_UNREG:
			# unregister keyword
			unregisterKeyword(chat_id, keyword)
		elif command == CMD_HELP:
			# send help message
			showHelp(chat_id)
		else:
			bot.sendMessage(chat_id, "올바른 명령이 아닙니다.")
			showHelp(chat_id)

if __name__ == '__main__':
	main()