# -*- coding: utf-8 -*-

import sys
import re
import time
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

INPUT = "2015_financial_report_swissre_ar15.pdf"
OUTPUT = "result.txt"

def main():
	
	start = time.time()
	
	f = open("locations.txt")
	locations = f.read().splitlines()
	f.close
    
	pdf_name = INPUT
	output_name = OUTPUT
    
	if (len(sys.argv) > 1):
		if sys.argv[1]:
			pdf_name = sys.argv[1]
	if (len(sys.argv) > 2):    
		if sys.argv[2]:
			output_name = sys.argv[2]
    
	res = pdfparser(pdf_name, locations)
    
	print "------------------------------------------------------------"
	print "Results (you can find them in %s also) :"%output_name
    
	f = open(output_name, "w")
    
	for item in res:
		if item["pages"]:
			info = "%s -> Found on page %s"%(item["name"], ", ".join(str(page) for page in item["pages"]))
			print info
			f.write(info + "\n")
                
	f.close()

	end = time.time()
	elapsed = end - start
	print "Time taken: ", elapsed, "seconds."

def pdfparser(data, locations):
	res = [0] * len(locations)
	fp = file(data, 'rb')
	rsrcmgr = PDFResourceManager()
	codec = 'utf-8'
	laparams = LAParams()
	page_list = PDFPage.get_pages(fp)
    
	item_list = []
	for place in locations:
		new_item = dict()
		new_item["name"] = place
		new_item["found"] = 0
		new_item["pages"] = []
		item_list.append(new_item)
    
    # Process each page contained in the document
	for (index, page) in enumerate(page_list):
		retstr = StringIO()
		device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
		interpreter = PDFPageInterpreter(rsrcmgr, device)
        
		page_num = index + 1
		interpreter.process_page(page)
		data = retstr.getvalue()
		for item in item_list:
			if re.search("\W%s\W"%item["name"], data):
				print "Found %s on page %d"%(item["name"], page_num)
				item["pages"].append(page_num)
				item["found"] = item["found"] + 1
        
        #f = open("pages/page%d.txt"%page_num, "w")
        #locations = f.write(data)
        #f.close()

	return item_list
                
if __name__ == '__main__':
	main()