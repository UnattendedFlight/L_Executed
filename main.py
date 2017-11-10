import json, os, csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import argparse
parser = argparse.ArgumentParser(description='Look up someone in the US\'s database of executions..')
parser.add_argument('searchterm', metavar='term', type=str, nargs='*', help='search terms to fullfill', default=[])
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-l', '--verbose-lookup', action='store_true')
parser.add_argument('-p', '--pretty-print', action='store_true', help='prints results of --format in a easily readable way.')
oFormats = ['dict', 'json_dump', 'list', 'string']
parser.add_argument('-f', '--format', type=str, nargs=1, help='output format ' + str(oFormats))
args = parser.parse_args()
if args.format:
	if args.format[0].lower() not in oFormats:
		print("Please provide a valid format!")
		exit()

def debug(msg, module='main', errno = 0, exc=""):
	global args
	if args.verbose:
		if errno > 0:
			if module == "lookup":
				if args.verbose_lookup:
					print("[debug]:[{}]:[error][{}] : {} - {}".format(module, errno, msg, exc))
			else:
				print("[debug]:[{}]:[error][{}] : {} - {}".format(module, errno, msg, exc))
		else:
			if module == "lookup":
				if args.verbose_lookup:
					print("[debug]:[{}] : {}".format(module, msg))
			else:
				print("[debug]:[{}] : {}".format(module, msg))

CSV_URL = 'https://deathpenaltyinfo.org/exec-xls-export'
executions = {}
responses = {
    100: ('Continue', 'Request received, please continue'),
    101: ('Switching Protocols',
          'Switching to new protocol; obey Upgrade header'),

    200: ('OK', 'Request fulfilled, document follows'),
    201: ('Created', 'Document created, URL follows'),
    202: ('Accepted',
          'Request accepted, processing continues off-line'),
    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    204: ('No Content', 'Request fulfilled, nothing follows'),
    205: ('Reset Content', 'Clear input form for further input.'),
    206: ('Partial Content', 'Partial content follows.'),

    300: ('Multiple Choices',
          'Object has several resources -- see URI list'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    303: ('See Other', 'Object moved -- see Method and URL list'),
    304: ('Not Modified',
          'Document has not changed since given time'),
    305: ('Use Proxy',
          'You must use proxy specified in Location to access this '
          'resource.'),
    307: ('Temporary Redirect',
          'Object moved temporarily -- see URI list'),

    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    401: ('Unauthorized',
          'No permission -- see authorization schemes'),
    402: ('Payment Required',
          'No payment -- see charging schemes'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this server.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with '
          'this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone',
          'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
}
debug("Preparing database..", "db")
try:
	with requests.Session() as s:
		debug("Downloading csv..", "db")
		download = s.get(CSV_URL)
		debug(download, "request")
		decoded_content = download.content.decode('utf-8')
		debug("Parsing CSV", "db")
		cr = csv.reader(decoded_content.splitlines(), delimiter=',')
		executions = list(cr)
		debug("No errors", "db")
except Exception as e:
	debug("Encountered errors! ", "db", 3, e)
malecount = 0
executiondict = {}
skip = True
gender = {
	'm':"Male",
	'f':"Female",
	'':""
}

def printRes(msg, extra = ""):
	global args
	if args.pretty_print:
		return json.dumps(msg, indent=4) + extra
	else:
		return str(msg) + extra

def getPl(victim):
	if victim:
		if int(str(victim).split()[0]) > 1:
			victim += "s"
	return victim
for each in executions:
	curexecuted = {}
	if not skip:
		curexecuted['Date']=executions[executions.index(each)][0]
		curexecuted['Name']=executions[executions.index(each)][1]
		curexecuted['Age']=executions[executions.index(each)][2]
		curexecuted['Sex']=gender[executions[executions.index(each)][3]]
		curexecuted['Race']=executions[executions.index(each)][4]
		curexecuted['Number / Race / Sex of Victims']=json.dumps(list(filter(None, [getPl(victim) for victim in str(executions[executions.index(each)][5]).split("(s)") if "(s)" not in victim])), indent=4).replace(",\n    \"(s)\"","")
		curexecuted['State']=executions[executions.index(each)][6]
		curexecuted['Region']=executions[executions.index(each)][7]
		curexecuted['Method']=executions[executions.index(each)][8]
		curexecuted['Juvenile']=executions[executions.index(each)][9]
		curexecuted['Federal']=executions[executions.index(each)][10]
		curexecuted['Volunteer']=executions[executions.index(each)][11]
		curexecuted['Foreign National']=executions[executions.index(each)][12]
		curexecuted['County']=executions[executions.index(each)][13]
		executiondict[executions[executions.index(each)][0]] = curexecuted
	else:
		skip = False


with open("executionlist.json", 'w') as f:
	f.write(json.dumps(executiondict, indent=4))

found = []
if len(args.searchterm) > 0:
	sr = args.searchterm
	print("Searchterms present. Searching..")
else:
	print("Total Executions: {}, Total Male: {}, Total female: {}".format(len(executions), len([count for count in executions if count[3] == 'm']), len([count for count in executions if count[3] == 'f'])))
	print("##########################################################################################\nReady to Search!")

	sr = input()
	if "," not in sr:
		st = str(sr)
		sr = []
		sr.append(st)
	else:
		sr = str(sr).replace(" , ", ",").replace(" ,", ",").replace(", ",",").split(",")

print(sr)
all = len(sr)
possible = 0
for key, it in executiondict.items():
	jj = []
	for key2, it2 in executiondict[key].items():
		for search in sr:
			if (search.lower() in str(it2).lower()) or (search.lower() == "volunteer" and executiondict[key]['Volunteer'] == "Yes") or (search.lower() == "foreign national" and executiondict[key]['Foreign National'] == "Yes") or (search.lower() == "juvenile" and executiondict[key]['Juvenile'] == "Yes") or (search.lower() == "federal" and executiondict[key]['Federal'] == "Yes"):
				jj.append(search)
				possible += 1
				debug("Found possible match.. Adding to review-queue ({}) - ({}/{}) | {}:{}".format(possible, len(jj), len(sr), jj, sr), "lookup")

	cc = 0
	for ss in sr:
		if ss in jj:
			cc += 1

	if cc == len(sr) or (len(sr) == 1 and sr[0] == ""):
		if executiondict[key] not in found:
			found.append(executiondict[key])
			debug("Match confirmed! All searchterms satisfied.. ({}/{}) | {}:{}".format(len(jj), len(sr), jj, sr), 'lookup')
		else:
			debug("Match already matched..", "lookup", errno=4, exc="Match ({}) already exists in found matches..".format(key))
	else:
		debug("Match discarded.. Accuracy: ({}/{})".format(len(jj), len(sr)), 'lookup')
pl = ""
if len(found) > 1:
	pl = "s"
print("Found {} result{}.. ".format(len(found), pl))
input()
cc = 0
maxOnScreen = 3

print('##########################################################################################')
for each in found:
	if cc >= maxOnScreen:
		cc = 0
		if not args.format:
			print("Press enter to view more \n...")
			input()
	cc += 1
	if args.format:
		if args.format[0].lower() == 'dict':
			printRes(each, ",")
		elif args.format[0].lower() == "str" or args.format[0].lower() == "string":
			print('Date: {Date}\nName: {Name}\nAge: {Age}\nSex: {Sex}\nRace: {Race}\nVictims: {Number / Race / Sex of Victims}\nState: {State}\nRegion: {Region}\nDeath by: {Method}\nJuvenile: {Juvenile}\nFederal: {Federal}\nVolunteer: {Volunteer}\nForeign National: {Foreign National}\nCounty: {County}\n##########################################################################################\n'.format(**found[found.index(each)]), end='\r')
		elif args.format[0].lower() == "list":
			keys = each.keys()
			values = each.values()
			print(printRes(list(keys)))
			print(printRes(list(values)))
	else:
		print('Date: {Date}\nName: {Name}\nAge: {Age}\nSex: {Sex}\nRace: {Race}\nVictims: {Number / Race / Sex of Victims}\nState: {State}\nRegion: {Region}\nDeath by: {Method}\nJuvenile: {Juvenile}\nFederal: {Federal}\nVolunteer: {Volunteer}\nForeign National: {Foreign National}\nCounty: {County}\n##########################################################################################\n'.format(**found[found.index(each)]), end='\r')
	kk = [["-" + name.lower() for name in found[found.index(each)]['Name'].split()][:-1][cc] for cc in range(len(found[found.index(each)]['Name'].split())-1)]
	first = found[found.index(each)]['Name'].split()[len(found[found.index(each)]['Name'].split())-1].lower()
	for hh in kk:
		first += hh
	link = "http://murderpedia.org/{}.{}/{}/{}.htm".format(found[found.index(each)]['Sex'].lower(), found[found.index(each)]['Name'].split()[len(found[found.index(each)]['Name'].split())-1][:1], found[found.index(each)]['Name'].split()[len(found[found.index(each)]['Name'].split())-1][:1].lower(), first)
	data = requests.get(link)
	debug(str(data.status_code) + " " + str(responses[data.status_code][0]) + " | " + link, "request")
	dd = "Not Found"
	printstuff = []
	printstuffDict = {}
	if data.status_code == 200:
		dd = data.text
		soup = BeautifulSoup(dd, 'html.parser')
		td = soup.find_all('td')
		con = False
		for c in td:
			if found[found.index(each)]['Name'].split()[:1][0] in td[td.index(c)].get_text().strip().split():
				con = True
			if "Status" in td[td.index(c)].get_text().strip():
				break
			if con:
				try:
					try:
						oki = td[td.index(c)].style.font.b.text.replace('\n', '')
					except:
						oki = td[td.index(c)].b.text.replace('\n', '')
					printstuff.append(" ".join(td[td.index(c)].get_text().strip().split()).replace(td[td.index(c)].b.text.replace('\n', ''), "") + oki)
					printstuffDict[" ".join(td[td.index(c)].get_text().strip().split()).replace(td[td.index(c)].b.text.replace('\n', ''), "").replace(":", "")] = oki
				except:
					printstuff.append(td[td.index(c)].get_text().strip())
					printstuffDict[td[td.index(c)].get_text().strip().split(':')[0]] = td[td.index(c)].get_text().strip().split()
	if args.format:
		if args.format[0] == "list":
			debug(printRes(list(filter(None, printstuff))), "response")
		elif args.format[0] == "dict":
			debug(printRes(printstuffDict), "debug")
		elif args.format[0] == "string" or args.format[0] == "str":
			for stf in printstuff[2:]:
				if stf:
					print(stf)
	else:
		for stf in printstuff[2:]:
			if stf:
				print(stf)
		if len(list(filter(None, printstuff))) == 0:
			print("No additional info.")
		print('##########################################################################################')
