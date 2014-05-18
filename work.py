import re
import json
from urllib2 import Request, urlopen
from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO
import config
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
import lxml.html.clean as clean
import os
import tempfile
import subprocess


class AK_lobby(object):
    def __init__(self, filter_str=''):
        self.url = "http://doa.alaska.gov/apoc/Lobbyist/lobcovc.html"
        self.filter_str = filter_str
        self.filenames = []
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        content = self.driver.page_source
        cleaner = clean.Cleaner()
        content = cleaner.clean_html(content)
        table = self.driver.find_element_by_xpath(
            "//div[@id='content_partial']/div[@class='content']/table[1]")
        self.trs = table.find_elements(By.TAG_NAME, "tr")
        self.filenames = self.get_files()
        self.download_dir = config.DOWNLOAD_DIR
        self.data_dir = config.DATA_DIR
        self.text_conv_dir = config.TEXT_CONV_DIR
        self.set_up_directories()
    def __del__(self):
        self.driver.close()
        print "AKLobby closed"

    def get_files(self):
        lst = []
        for row in self.trs:
            tds = row.find_elements(By.TAG_NAME, "td")
            year = "NOYEAR"
            if len(tds) > 0:
                year = tds[0].text
            for td in tds:
                hrefs = td.find_elements(By.TAG_NAME, "a")
                for h in hrefs:
                    url = h.get_attribute("href")
                    a_text = re.sub(' +', '_', h.text)
                    lst.append([year + "_" + a_text, url,year])
        return [l for l in lst if not re.search("Employer", l[0])]

    def print_files(self):
        for _file in self.list_files():
            print _file[0]
            print str(_file[1])
            print "----"

    def list_files(self):
        filt = re.sub(' +', ' ', self.filter_str)
        for filename in self.filenames:
            filt_lst = filt.split(" ")
            list_filter = '.*' + '.*'.join(filt_lst) + '.*'
            regex = re.compile(list_filter, re.IGNORECASE)
            if re.match(regex, filename[0]):
                yield filename

    def download_pdfs(self):
        for _file in self.list_files():
            print "downloading " + _file[0]
            writer = PdfFileWriter()
            remotefile = urlopen(Request(_file[1])).read()
            memoryfile = StringIO(remotefile)
            pdffile = PdfFileReader(memoryfile)
            for pagenum in xrange(pdffile.getNumPages()):
                currentpage = pdffile.getPage(pagenum)
                writer.addPage(currentpage)
                outputstream = file(self.download_dir +  "/" +
                                    _file[0] + ".pdf", "w+")
                writer.write(outputstream)
                outputstream.close()
            print "download complete"
            print "----"

    def convert_pdfs_to_text(self):
        for _file in self.list_files():
            print "Converting " + _file[0] + " from pdf to text."
            fin = open(os.getcwd() + "/downloads/" + _file[0] + ".pdf", 'r')
            fpout = open(
               self.text_conv_dir + "/" 
                + _file[0] + ".txt", 'w+')
            pdfdata = fin.read()
            tempf = tempfile.NamedTemporaryFile()
            tempf.write(pdfdata)
            tempf.seek(0)
            outputtf = tempfile.NamedTemporaryFile()
            if (len(pdfdata) > 0):
                out, err = subprocess.Popen(
                    ["pdftotext", "-layout",
                     tempf.name, outputtf.name]).communicate()
                fpout.write(outputtf.read())
            else:
                print _file[0] + " did not convert to txt file"

    def isolate_txt(self, txt, fname):
        txt = re.sub("(?s).*?(Lobbyist\s\s\s)", "\\1", txt, 1)
        txt = re.sub("\A(Lobbyist\s\s\s\s).*?\n", "", txt)
        txt = re.sub("\n.*(Lobbyist \s\s\s\s).*\n", "\n", txt)
        txt = re.sub('\f', '', txt)
        txt_split = [line for line in txt.split('\n') if line.strip()]
        spacere = re.compile("^\s{50}.*?")
        txt_split = [line for line in txt_split
                        if not spacere.match(line)]
        totalre = re.compile("     TOTAL")
        txt_split = [line for line in txt_split if not totalre.search(line)]
        txt_split = [
            line for line in txt_split if len(line.strip().split(' ')) > 1]
        txt_split = [
            line for line in txt_split
            if not re.compile("Page\s[0-9]{1,2}\sof\s[0-9]{1,2}").search(line)]
        return txt_split

    def make_rows(self, txt_split):
        a1 = "$0.00"
        a1non = "$0.00"
        lobbyist = ""
        for i, line in enumerate(txt_split):
            if line[0] is not " ":
                lobbyist = line[:100].strip()
                match = re.compile(".*(\$\d.*\s).*(\$\d.*)").match(line)
                if match is not None:
                    a1 = match.group(1)[:-1]
                    a1non = match.group(2)
                else:
                    a1 = "$0.00"
                    a1non = "$0.00"
            else:
                match = re.compile("^\s{5}.*").match(line)
                if match:
                    txt_split[i] = lobbyist + "    " + txt_split[i].strip()
                    txt_split[i] = txt_split[i] + '    ' + a1 + '    ' + a1non

                txt_split[i] = re.sub('  +', '*!*', txt_split[i])

        txt_split = [line for line in txt_split if
                     re.compile("(\*\!\*)").search(line)]
        return txt_split

    def t_split_to_dictionary_list(self, txt_split, header_list,year):
        final_dict_list = []
        bad_lst = []
        i = 0
        for line in txt_split:
            i += 1
            lst = line.split("*!*")
            dict_tmp = {}
            dict_tmp["id"] = i
            bad = False
            for j in range(0, 7):
                try:
                    dict_tmp[header_list[j]] = lst[j]
                except:
                    bad = True
            if bad == True:
                bad_lst.append("--".join(lst))
            final_dict_list.append(dict_tmp)
        if len(bad_lst) > 0 :
            fpout = open(self.data_dir + "/" + year + "/bad_data.txt","w+")
            fpout.write("\n".join(bad_lst))
            fpout.close()
        return final_dict_list

    def text_to_json(self, txt, fname, year):
        header_list = ['Lobbyist', 'Employer', 'Fee','Reimbursable'
                      ,'Non Reimbursable','Schedule A1 Reimbursable',
                      'Schedule A1 Non Reimbursable']
        txt_split = self.isolate_txt(txt, fname)
        txt_split = self.make_rows(txt_split)
        final_dict_list = self.t_split_to_dictionary_list(
            txt_split, header_list,year)
        for d in final_dict_list:
            with open(self.data_dir + "/" + year + "/" + str(d['id']) +
                      ".json", 'wb') as outfile:
                json.dump(d, outfile)

    def convert_text_file_to_json(self):
        for _file in self.list_files():
            print "Converting - " + _file[0]
            if not os.path.exists(self.data_dir + "/" +  _file[2]):
                os.makedirs(self.data_dir + "/" +  _file[2])
            fin = open(os.getcwd() +
                       "/downloads/text_conv/" + _file[0] + ".txt", 'r')
            txt = fin.read()
            fin.close()
            self.text_to_json(txt, _file[0], _file[2])
            print _file[0] + " - Converted "
            print "------"

    def set_up_directories(self):
        if config.USE_ALTERNATE is False:
            current_directory = os.path.dirname(os.path.realpath(__file__))
            if not os.path.exists(current_directory + "/data"):
                os.makedirs(current_directory + "/data")
            if not os.path.exists(current_directory + "/downloads"):
                os.makedirs(current_directory + "/downloads")
            if not os.path.exists(current_directory + "/downloads/text_conv"):
                os.makedirs(current_directory + "/downloads/text_conv")


    def report(self):
        for direct in os.walk(self.data_dir).next()[1]:
            files = os.walk(self.data_dir + "/" + direct).next()[2]
            print  direct + ": " + str(len(files)) + \
                " files"


