HTML_INDEX_PAGE = 'index.html'

def main():
	html_file = open(HTML_INDEX_PAGE, 'r')
	html_text = html_file.read()
	html_file.close()
	return html_text