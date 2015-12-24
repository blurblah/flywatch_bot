
# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors

class DBHandler:

	def __init__(self, dbHost, id, password, db):
		self.connection = MySQLdb.connect(dbHost, id, password, db,
							cursorclass = MySQLdb.cursors.DictCursor)

	def insertKeyword(self, chatId, keyword):
		inserted = False
		cursor = self.connection.cursor()
		try:
			cursor.execute('SET NAMES utf8;')
			cursor.execute('INSERT INTO keywords(uid, keyword, created_at) \
							VALUES(%s, %s, now());', (chatId, keyword))
			self.connection.commit()
			print keyword, "registered. uid:", chatId
			inserted = True
		except Exception, error:
			self.connection.rollback()
			print Exception, error

		return inserted

	def deleteKeyword(self, chatId, keyword):
		deleted = False
		cursor = self.connection.cursor()
		try:
			cursor.execute('SET NAMES utf8;')
			cursor.execute('DELETE FROM keywords WHERE uid = %s AND keyword = %s;',
							(chatId, keyword))
			self.connection.commit()
			print keyword, "deleted. uid:", chatId
			deleted = True
		except Exception, error:
			self.connection.rollback()
			print Exception, error

		return deleted

	def selectKeywordList(self, chatId):
		cursor = self.connection.cursor()
		cursor.execute('SET NAMES utf8;')
		cursor.execute('SELECT * FROM keywords WHERE uid = %d \
						ORDER BY created_at DESC;' % chatId)
		return cursor.fetchall()

	def selectAllKeywords(self):
		cursor = self.connection.cursor()
		cursor.execute('SET NAMES utf8;')
		cursor.execute('SELECT * FROM keywords;')
		return cursor.fetchall()

	def selectArticles(self, searchTime):
		cursor = self.connection.cursor()
		cursor.execute('SET NAMES utf8;')
		cursor.execute("SELECT * FROM articles WHERE created_at >= '%s'" % searchTime)
		return cursor.fetchall()
