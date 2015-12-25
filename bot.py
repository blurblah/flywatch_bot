# -*- coding: utf-8 -*-
import telepot
import logging
import time
from datetime import datetime
from dbhandler import DBHandler
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

CMD_START = "/start"
CMD_REG = "/reg"
CMD_UNREG = "/unreg"
CMD_LIST = "/list"
CMD_HELP = "/help"

bot = telepot.Bot('access_token')
dbHandler = DBHandler('host', 'id', 'password', 'db')

def searchArticles(keyword, articles):
	searched = list()
	for article in articles:
		title = article['title'].encode('utf-8')
		if title.find(keyword) != -1:
			searched.append("%s\r\nurl : %s" % (title, article['url'].encode('utf-8')))

	return searched

def sendResults(keywords, articles):
	for keywordRow in keywords:
		keyword = keywordRow['keyword'].encode('utf-8')
		results = searchArticles(keyword, articles)
		print "Keyword:", keyword, "Seached articles:", results
		for item in results:
			uid = keywordRow['uid']
			print "Send message to", uid
			print item
			bot.sendMessage(uid, item)

def main():
	bot.notifyOnMessage(handle)
	print "Flywatch bot started..."
	while 1:
		# check crawling data
		checkTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
		print "Select crawling data at", checkTime
		articles = dbHandler.selectArticles()
		print "Selected crawling data:", articles
		now = datetime.now() # update checked time

		keywords = dbHandler.selectAllKeywords()
		sendResults(keywords, articles)
		time.sleep(60)

def showHelp(chatId):
	USAGE = u"""[사용법] 아래 명령어대로 입력하세요.
	/reg keyword - (keyword 등록)
	/unreg keyword - (keyword 제거)
	/list - (등록된 keyword)
	/help - (도움말 보여주기)
	"""
	showKeyboard = {'keyboard': ['/reg', '/unreg', '/list', '/list']}
	bot.sendMessage(chatId, USAGE, reply_markup = showKeyboard)


def registerKeyword(chatId, keyword):
	if dbHandler.insertKeyword(chatId, keyword):
		bot.sendMessage(chatId, "[%s] 등록 성공" % keyword)
	else:
		bot.sendMessage(chatId, "[%s] 등록 실패" % keyword)

def unregisterKeyword(chatId, keyword):
	if dbHandler.deleteKeyword(chatId, keyword):
		bot.sendMessage(chatId, "[%s] 제거 성공" % keyword)
	else:
		bot.sendMessage(chatId, "[%s] 제거 실패" % keyword)

def showKeywordList(chatId):
	rows = dbHandler.selectKeywordList(chatId)
	list = ""
	for row in rows:
		list += "[%s] \r\n" % str(row['keyword'])

	if list == "":
		list = "등록된 키워드 없음"
	bot.sendMessage(chatId, list)

def handle(msg):
	print msg
	content_type, chat_type, chat_id = telepot.glance2(msg)
	if content_type == 'text':
		tokens = msg['text'].split(' ')
		command = tokens[0].lower()
		keyword = msg['text'][len(command):].encode('utf-8').lstrip().rstrip()
		if command == CMD_START:
			showHelp(chat_id)
		elif command == CMD_REG:
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
