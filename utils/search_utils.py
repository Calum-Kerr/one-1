import re
from utils.text_extractor import TextExtractor

class SearchUtils:
    @staticmethod
    def search_text(pdf_loader, query, case_sensitive=False):
        """Search for text across PDF pages"""
        results = []
        flags = 0 if case_sensitive else re.IGNORECASE
        
        for page_num in range(pdf_loader.page_count):
            page_dict = pdf_loader.get_page_text(page_num)
            text_elements = TextExtractor.extract_text_with_styles(page_dict)
            
            for element in text_elements:
                matches = list(re.finditer(query, element['text'], flags))
                if matches:
                    for match in matches:
                        results.append({
                            'page': page_num,
                            'text': match.group(),
                            'bbox': element['bbox'],
                            'style': element['style']
                        })
        
        return results
