import re
from ensure import ensure_annotations
from src.transcribtiondatasetcreation.components import nlp
from src.transcribtiondatasetcreation import logger

@ensure_annotations
def clean_text(input_text: str) -> str:
    text = _clean_special_chars(input_text)
    text = _clean_person_initials(text)
    text = _clean_joined_left_lines(text)
    text = _clean_started_ended_lines(text)
    text = _clean_not_alpha_lines(text)
    text = _clean_times(text)
    text = _clean_empty_lines(text)
    text = _clean_consecutive_duplicate_lines(text)
    text = _clean_time_lines(text)
    return text

@ensure_annotations
def name_entity_process(text: str) -> str:
    person_names = set()
    spacy_parser = nlp(text)
    for entity in spacy_parser.ents:
        if entity.label_ == 'PERSON':
            person_names.add(entity.text)
    logger.info(f'Person names found: {person_names}')
    clean_text = text
    for name in person_names:
        pattern = rf'^{name}\n'
        clean_text = re.sub(pattern, f'{name}: ', clean_text, flags=re.MULTILINE)
    return clean_text

def _clean_person_initials(text: str) -> str:
    # From Copying texts from Teams some lines are Person's initials 
    clean_text = re.sub(r'^[A-Z]{2}$', '', text, flags=re.MULTILINE)
    return clean_text

def _clean_special_chars(text: str):
    for s in ['\ue7c8', '\uea3f', '\ue8fa']:
        text = text.replace(s, '')
    return text

def _clean_joined_left_lines(text: str):
    lines = text.splitlines()
    lines = [line for line in lines if not line.endswith('joined the meeting') and not line.endswith('left the meeting')]
    return '\n'.join(lines)

def _clean_started_ended_lines(text: str):
    lines = text.splitlines()
    lines = [line for line in lines if not line.endswith('started transcription') and not line.endswith('stopped transcription')]
    return '\n'.join(lines)
    
def _clean_not_alpha_lines(text: str):
    # Split the input string into lines
    lines = text.splitlines()
    
    # Keep only the lines that contain at least one letter
    lines_with_letters = [line for line in lines if any(char.isalpha() for char in line)]
    
    # Join the lines back into a string
    result_string = '\n'.join(lines_with_letters)
    return result_string

def _clean_times(text: str):
   # Use regex to remove lines that match the pattern
   pattern = r'(\s+\d+ hour[s]?)?(\s+\d+\s+minute[s]?)?\s+(\d+\s+second[s]?)?(\s*(\d+:)?\d+:\d{2})?$'  # Pattern to match
   cleaned_string = re.sub(pattern, '', text, flags=re.MULTILINE)
   pattern = r'^(\d+ hour[s]?)?(\s+\d+\s+minute[s]?)?\s+(\d+\s+second[s]?)?(\s*(\d+:)?\d+:\d{2})?$'
   cleaned_string = re.sub(pattern, '', cleaned_string, flags=re.MULTILINE)
   return cleaned_string.strip()

def _clean_empty_lines(text: str):
    # Split the text into lines, remove empty lines, and join the non-empty lines
    lines = [line for line in text.splitlines() if line.strip()]
    return '\n'.join(lines)

def _clean_consecutive_duplicate_lines(text: str):
    lines = text.splitlines()
    result_lines = []
    prev_line = None

    for line in lines:
        if line != prev_line:
            result_lines.append(line)
            prev_line = line

    result_string = '\n'.join(result_lines)
    return result_string

def _clean_time_lines(text: str):
    pattern = r'^\d{2,3}:\d{2,3}$'  # Pattern to match
    cleaned_string = re.sub(pattern, '', text, flags=re.MULTILINE)
    return cleaned_string