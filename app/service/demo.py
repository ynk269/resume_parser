# !pip install pymupdf
# Python import name of the PyMuPDF library is fitz.

from unidecode import unidecode 

import fitz
import re

from pdfminer.high_level import extract_text

doc = fitz.open()

previous_block_id = 0


def pymudf_parser(filepath):
    doc = fitz.open(filepath)
    for page in doc:

        text = page.get_text()

        print('\t \n text forom the modeukw \n', text)

        output = page.get_text("blocks")
        for block in output:
            if block[6] == 0:
                if previous_block_id != block[5]:
                    print("\n")

                plain_text = unidecode(block[4])

                print(plain_text)

    # text =  extract_text(filepath)
    # print(text)