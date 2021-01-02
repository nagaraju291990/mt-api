# -*- coding: utf-8 -*-
import requests, json
import sys
from argparse import ArgumentParser
import re

parser = ArgumentParser(description='Program to run ILMT API \n\r'+
						"How to Run?\n" +
						"python3 " + sys.argv[0] + " -i=inputfile.txt" + " -p=portno|8080 -t=allmodules|end2end -m=modulename|morph"
						)

parser.add_argument("-i", "--input", dest="inputfile",
					help="provide .txt file name",required=True)
parser.add_argument("-p", "--portno", dest="portno",
					help="port number",required=False)
#parser.add_argument("-t", "--p=type", dest="type",
#					help="module output or end to end",required=True)
parser.add_argument("-m", "--m=1/3 or 3/5", dest="module_name",
					help="1/3 means starting from 1st module to 3rd module output",required=False)

args = parser.parse_args()

inputfile = args.inputfile
portno = args.portno
modules = args.module_name

fp = open(inputfile, 'r', encoding='utf-8')
lines = fp.read().split("\n")
fp.close()

def reverse(string):
	return string[::-1]
if(modules is not None):
	url = 'http://localhost:' + str(portno) +'/tam/tel/' + modules
else:
	url = 'http://localhost:' + str(portno) + '/tam/tel/1/100'

url2 = 'http://localhost:' + str(portno) + '/tam/tel/modules'

input="""<Sentence id=\"1\">
1 waFcEp unk
2 peVriyakovil unk
3 eVnYavum unk
4 ikkovil unk
5 arYiyappatukirYawu unk
6 . unk
</Sentence>
""";

sentence_count = 1

for line in lines:
	if(line == ''):
		continue

	#print(line)
	dataToSend = {"input":line.encode('utf-8').strip()}
	myheaders = {"Content-type": "application/x-www-form-urlencoded;charset=UTF-8"}
	proxies = {
	"http" :None,
	"https":None,
	}

	module_response = requests.get(url2, proxies=proxies, headers=myheaders)
	#print(module_response.text)
	module_response = json.loads(module_response.text)


	res = requests.post(url, proxies=proxies, data=dataToSend, headers=myheaders)
	myresponse = json.loads(res.text)
	if(modules is None):
		print(myresponse["output"])
	else:
		count = 1
		print("<Beginning of Sentence id=\""+ str(sentence_count) +"\">")

		#print ("iam")
		#myresponse = sorted(myresponse, key=lambda x: x[0])
		#print(myresponse)
		for m in module_response:
			for key in sorted(myresponse):
				if(re.search(m + '-' + r'\d', key)):
					print(key)
					val = re.sub(r'\n\r', '', myresponse[key])
					print(val)

		print("</End of Sentence>")
	sentence_count = sentence_count + 1


