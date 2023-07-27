import json
import re
#import fitz


class PDFProcessor:
    def __init__(self, doc):
        self.doc = doc
        self.all_paragraphs = self.get_paragraphs()


    def get_paragraphs(self, start=0, end='a'):
        """
        Creates a list of paragraphs from the document

        Args:
            start (int, optional): Page to start obtaining paragraphs from. Defaults to 0.
            end (str, optional): Last page to obtain paragraphs from. Defaults to 'a', signaling all.

        Raises:
            ValueError: if start < 0
            ValueError: if start > total pages in document
            ValueError: if start > end

        Returns:
            list[str]: List of strings corresponding to the paragraphs
        """
        
        if end == 'a':
            end = int(self.doc.page_count)
        else:
            end = int(end)
        
        ## HOW TO DEBUG
        if start < 0:
            raise ValueError('start must be >= 0')
        elif start >= self.doc.page_count:
            raise ValueError('start must be < the doc page count')
        elif start > end:
            raise ValueError('start must be < end')
        
        if end > int(self.doc.page_count):
            end = self.doc.page_count
        
        pars1 = self.__get_pars_per_page(start, end)
        return self.__clean_up_pars(pars1)
    
    

    def __get_pars_per_page(self, start, end):
        all_paragraphs = []

        # iterate over pages of document
        for i in range(start, end):
            # make a dictionary
            json_data = self.doc[i].get_text('json')
            json_page = json.loads(json_data)
            page_blocks = json_page['blocks']

            page_paragraphs = []
            new_paragraph = ''
            bold_txt = ''
            start_bold = False

            for j in range(len(page_blocks)):
                line = page_blocks[j]

                if 'lines' in list(line.keys()):
                    for n in line['lines']:
                        text_boxes = n['spans']

                        for k in range(len(text_boxes)):
                            font = text_boxes[k]['font']
                            text = text_boxes[k]['text'].replace('\n', '')
                            flags = int(text_boxes[k]['flags']) # to check if it is a superscript

                            if not re.search('S\d+', text) or (re.search('S\d+', text) and ('Bold' in font or 'bold' in font)) or re.search('[T|t]able', text) or re.search('[F|f]igure',text):
                                
                                if flags&2**0:
                                    text = ' ' + text
                                
                                if k == (len(text_boxes) - 1) and j == (len(page_blocks) - 1):
                                    new_paragraph += text
                                    if start_bold:
                                        page_paragraphs.append(['bold', new_paragraph])
                                    else:
                                        page_paragraphs.append(['plain', new_paragraph])
                                    new_paragraph = ''
                                else:
                                    if 'Bold' in font or 'bold' in font:
                                        bold_txt += text
                                    else:
                                        if len(bold_txt) > 5:
                                            if start_bold:
                                                page_paragraphs.append(['bold', new_paragraph])
                                            else:
                                                page_paragraphs.append(['plain', new_paragraph])

                                            start_bold = True
                                            new_paragraph = ''
                                            new_paragraph += bold_txt
                                            bold_txt = ''
                                        else:
                                            new_paragraph += bold_txt
                                            bold_txt = ''

                                        if new_paragraph == '':
                                            start_bold = False

                                        new_paragraph += text

            all_paragraphs.extend(page_paragraphs)

        return all_paragraphs



    def __clean_up_pars(self, pars):
        all_paragraphs = []
        new_paragraph = ''

        for par in pars:
            if par[0] == 'bold':
                all_paragraphs.append(new_paragraph)
                new_paragraph = ''
            new_paragraph += par[1]

        clean_up = [par for par in all_paragraphs if par != '' and not par.isspace()]
        
        #paragraphs = []
        
        # for par in clean_up:
        #     new_par = Paragraph(par)
        #     paragraphs.append(new_par)

        return clean_up

 
 
 
 

# class Paragraph:
#     def __init__(self, text):
#         self.text = text
#         self.len = len(self.text)
    
#     def get_text(self):
#         return self.text