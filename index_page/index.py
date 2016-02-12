HTML_INDEX_PAGE = 'index.html'

def main():
	try:
		html_file = open(HTML_INDEX_PAGE, 'r')
	except:
		return 'error: open index.html'
		
	html_text = html_file.read()
	html_file.close()
	return html_text