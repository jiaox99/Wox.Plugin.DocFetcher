#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wox import Wox, WoxAPI
from py4j.java_gateway import JavaGateway, GatewayParameters
from py4j.java_gateway import java_import
import sys
import os

"""
This script sends the given command-line arguments as a query to the running
DocFetcher instance. The results returned by the latter are printed as filename-
filepath pairs on the standard output.

For more advanced processing of the results, call the search function below
directly. In principle, you can also reuse the code in the search function for
arbitrarily scripting the DocFetcher instance.

By default, DocFetcher's scripting support is disabled due to security reasons
and must be enabled by setting the variable "PythonApiEnabled" in the advanced
settings file (program-conf.txt) to "true".

Running this script requires Py4J (https://www.py4j.org/). DocFetcher already
ships with a Py4J distribution, but it only works if the py4j folder is in the
same folder as this script. To script DocFetcher from a different location, move
the py4j folder there, or install Py4J separately.

Note that only the main DocFetcher program instance supports scripting, not the
DocFetcher daemon.
"""
class DocFetcher(Wox):

	def query(self, query):
		results = []
		if query.endswith(">"):
			try:
				result_docs = self.search(query[0:(len(query)-1)], 28834)
				for doc in result_docs:
					# print(doc.getFilename() + "\t" + doc.getPathStr())
					filePath = doc.getPathStr()
					results.append({
						"Title": doc.getFilename(),
						"SubTitle":filePath,
						"IconPath":"Images/app.ico",
						"ContextData":filePath,
						"JsonRPCAction":{
							"method": "openFile",
							#参数必须以数组的形式传过去
							"parameters":[filePath],
							#是否隐藏窗口
							"dontHideAfterAction":True
						}
					})
			except:
				results.append({
					"Title": "Some Error",
					"SubTitle":"ERROR: " + str(sys.exc_info()[1]),
					"IconPath":"Images/app.ico",
				})
		else:
			results.append({
				"Title": "Open parent directory",
				"SubTitle":"Type > at the end to confirm query",
				"IconPath":"Images/app.ico",
			})
		return results

	def context_menu(self, data):
		results = []
		pathInfo = data.split("/")
		pathInfo.pop()
		data = "/".join(pathInfo)
		results.append({
			"Title":"Open parent directory",
			"SubTitle":data,
			"IconPath":"Images/app.ico",
			"JsonRPCAction":{
				"method": "Wox.ShellRun",
				#参数必须以数组的形式传过去
				"parameters":["explorer.exe"],
				#是否隐藏窗口
				"dontHideAfterAction":True
			}
		})
		return results

	def search(self, query, port):
		"""Sends the given query string to the running DocFetcher instance at the
		given port and returns a list of result objects.
		
		The result objects provide the following getter methods for accessing their
		attributes:
		- getAuthors
		- getDateStr - e-mail send date
		- getFilename
		- getLastModifiedStr - last-modified date on files
		- getPathStr - file path
		- getScore - result score as int
		- getSender - e-mail sender
		- getSizeInKB - file size as int
		- getTitle
		- getType
		- isEmail - boolean indicating whether result object is e-mail or file
		
		This method will throw an error if communication with the DocFetcher
		instance fails.
		"""
		gateway = JavaGateway(gateway_parameters=GatewayParameters(port=port))
		java_import(gateway.jvm, "net.sourceforge.docfetcher.gui.Application")
		application = gateway.jvm.net.sourceforge.docfetcher.gui.Application
		
		indexRegistry = application.getIndexRegistry()
		searcher = indexRegistry.getSearcher()
		results = searcher.search(query)
		return results

	def openFile(self, filePath):
		os.startfile(filePath)
			

if __name__ == "__main__":
	DocFetcher()
