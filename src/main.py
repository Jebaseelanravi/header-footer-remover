import re
import os
from collections import defaultdict

"""
class responsible for removing the header and footer from text file
"""


class headerfooterremover:

    def __init__(self):
        """
        constructor method
        """
        self.header = None
        self.footer = None
        self.pagecount = 0
        self.strtoremove = set()

    def initialize_data(self):
        """
        data initialization method for parsing each document
        clean up the varibles needed for processing
        :return:
        """
        self.header = defaultdict(int)
        self.footer = defaultdict(int)
        self.pagecount = 0
        self.strtoremove = set()

    def process_file(self, path):

        """
        drive function for processing the file
        :param path: path of the input file
        :return: saves the processed file in output dir
        """
        self.initialize_data()
        content = self.read_file(path)
        pages = self.split_pages(content)
        for page in pages:
            lines = page.split("\n")
            self.process_header_section(lines[:2])
            self.process_footer_sections(lines[-2:])

        if not os.path.exists("../output"):
            os.makedirs("../output")
        self.save_processed_file(content, f"../output/{path.split('/')[-1]}")

    def read_file(self, path):

        """
        reads the content of the file
        :param path: path of the input file
        :return: content of the file
        """

        try:
            with open(path, encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError as ex:
            raise FileNotFoundError

        return content

    def split_pages(self, content):
        """
        split the content into multiple pages
        :param content:
        :return: list of pages
        """
        pages = content.split("\x0c")
        self.pagecount = len(pages)
        return pages

    def process_header_section(self, lines):
        """
        Pre process the input lines by removing the necessary spaces
        and map into dictionary for deduplication

        if a sentence occurs more than 5 times in dictionary it is marked  to be header

        :param lines: first two lines of the page
        :return:
        """

        headers = [re.sub(r' +', ' ', line).strip() for line in lines]
        for header in headers:
            self.header[header] += 1
            if self.header[header] > 5: # if the line occur more than 5 time mark it as header to be removed
                self.strtoremove.add(header)

    def process_footer_sections(self, lines):

        """
        Pre process the input lines by removing the necessary spaces
        and map into dictionary for deduplication

        if a sentence occurs more than 5 times in dictionary it is considered to be footer

        :param lines: last two lines of the page
        :return:
        """

        footers = [re.sub(' +', ' ', line).strip() for line in lines]
        for footer in footers:
            self.footer[footer] += 1
            if self.footer[footer] > 5:
                self.strtoremove.add(footer)

    def remove_headers(self, lines):
        """

        Receives the first two lines of the page

        if the line is detected as header by "process_header_section" function
        then the line is replace with None string

        :param lines: first two lines of the page
        :return: header removed lines of the page
        """
        for index, header in enumerate(lines[:2]):
            header = re.sub(' +', ' ', header).strip()
            if header in self.strtoremove: # if the line is marked as header the  remove
                lines[index] = ""
        return lines

    def remove_footer(self, lines):
        """

        Receives the last two lines of the page

        if the line is detected as footer by "process_footer_section" function
        or if the line contain page information such (page 2 of 20 or(1,2,3..)

        then the line is replace with None string

        :param lines: last two  lines of the page
        :return: footer removed lines of the page
        """

        numberoflines = len(lines)
        index = numberoflines - 2
        for footer in lines[-2:]:
            footer = re.sub(' +', ' ', footer).strip()
            if footer in self.strtoremove or re.search("(^page.*)|(^[0-9]+)", footer, re.IGNORECASE):
                lines[index] = ""
            index += 1
        return lines

    def save_processed_file(self, content, path):
        """
        save the processed file into the destination
        :param content: content of the input file
        :param path: filepath
        :return:
        """
        result_str = ""
        pages = content.split("\x0c")
        for page in pages:
            lines = page.split("\n")
            lines = self.remove_headers(lines)
            lines = self.remove_footer(lines)
            lines = "\n".join(lines)
            result_str = result_str + lines

        text_file = open(path, "w")
        text_file.write(result_str)
        text_file.close()


if __name__ == "__main__":
    formatter = headerfooterremover()
    for file in os.listdir('../input/'):
        filepath = os.path.join("../input/", file)
        formatter.process_file(path=filepath)
