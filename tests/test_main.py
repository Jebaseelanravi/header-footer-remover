from unittest import TestCase
from src.main import headerfooterremover


class test_headerfooterremover(TestCase):

    def setUp(self) -> None:
        self.test_obj = headerfooterremover()
        self.test_obj.initialize_data()


    def test_read_file_return_true_content(self):
        content = self.test_obj.read_file("../resources/test_file.txt")
        assert content == "helloworld"

    def test_read_file_return_error(self):
        self.assertRaises(FileNotFoundError,self.test_obj.read_file,"file-not-exists.txt")

    def test_split_pages_return_2_pages(self):
        pages = self.test_obj.split_pages("page1\x0cpage2")
        assert len(pages) == 2

    def test_process_header_section_return_identifed_duplicate(self):
        lines ="helloworld\nhelloworld\nsampleline"
        lines = lines.split("\n")
        self.test_obj.process_header_section(lines[:2])
        assert self.test_obj.header.get("helloworld") == 2

    def test_process_footer_sections_return_identified_duplicate(self):
        lines = "helloworld\nhelloworld\nsampleline"
        lines = lines.split("\n")
        self.test_obj.process_footer_sections(lines[-2:])
        assert self.test_obj.footer.get("helloworld") == 1

    def test_remove_headers_return_content_header_removed_string(self):
        lines = "sample-header-line\nsecond-header-line\nrest of the line\n furthermoreline"
        lines = lines.split("\n")
        self.test_obj.strtoremove.add("sample-header-line")
        header_removed_lines = self.test_obj.remove_headers(lines)
        assert header_removed_lines[0] == ""

    def test_remove_footer_return_removed_footer_lines(self):
        lines = "sample-paragraph\nPage 2 of 10" # example with footer to be removed
        footer_removed_string = self.test_obj.remove_footer(lines.split("\n"))
        assert  footer_removed_string[1] == ""

    def test_processed_file_return_save_processed_file(self):
        filepath = "../input/076fa1308b0a7eeeffe4b4a34c7cdbdb.txt"
        self.test_obj.process_file(filepath)
        assert "Anti-Money Laundering Act, 2008 Act 749" in self.test_obj.strtoremove

