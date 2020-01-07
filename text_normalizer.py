"""
Author: Tessa Pham
LING 208 Final Project: Text Normalizer
"""

import re
import os
import locale
import splitter
from string import punctuation
from num2words import num2words
from nltk.corpus import cmudict

abbrevs = {'Jan.': 'January', 'Feb.': 'February', 'Mar.': 'March', 'Apr.': 'April',
            'Jun.': 'June', 'Jul.': 'July', 'Aug.': 'August','Sep.': 'September',
            'Oct.': 'October', 'Nov.': 'November', 'Dec.': 'December', 'Rd.': 'Road',
            'St.': 'Street', 'Ave.': 'Avenue', 'Mr.': 'Mister', 'Mrs.': 'Missus',
            'Dr.': 'Doctor', 'Jr.': 'Junior', 'Sr.': 'Senior', 'Sen.': 'Senator'}
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December']
tlds = ['com', 'net', 'org', 'gov', 'mil'] # no tlds that need spelling out (e.g., 'edu')
cmu_entries = dict(cmudict.entries())
punctuations = punctuation.replace('$', '')
   
def normalize(text):
    acronym_or_letter_sequence = re.compile('^[A-Z]{2,}$')
    date = re.compile('^([1-9]|0[1-9]|1[0-2])/([1-9]|[12][0-9]|3[0-1])/[0-9][0-9]$')
    email = re.compile('^[^@\.]+@[^@\.]+\.[a-zA-Z]{3}$')
    abbrev = re.compile('^[A-Z][a-z]{0,3}\.$')
    currency = re.compile('^\$([1-9]{1}[0-9]{0,2}(\,[0-9]{3})*(\.[0-9]{1,10})?|[1-9]{1}[0-9]{0,}(\.[0-9]{1,10})?|0(\.[0-9]{1,10})?|(\.[0-9]{1,10})?)$')
    year = re.compile('^(19|20)\d{2,4}$')
    num = re.compile('^(\d*\.?\d+|\d{1,3}(,\d{3})*(\.\d+)?)$')
    time = re.compile('^[0-9]{1,2}(:[0-9]{1,2})+$')
    
    normalization = []

    for w in text.split():
        # handle abbreviation case where ending period matters
        if abbrev.match(w):
            norm = normalize_abbrev(w)
            if norm[-1] != '.':
                normalization.append(norm)
                continue
        
        # remove trailing punctuations
        w = w.strip(punctuations)

        # split hyphenated string
        if '-' in w:
            parts = w.split('-')
            for p in parts:
                normalization.append(normalize(p))
            continue
        
        # identify, categorize, and handle NSWs
        if acronym_or_letter_sequence.match(w):
            normalization.append(normalize_acronym_ls(w))
        elif date.match(w):
            normalization.append(normalize_date(w))
        elif email.match(w):
            normalization.append(normalize_email(w))
        elif currency.match(w):
            normalization.append(normalize_currency(w))
        elif time.match(w):
            normalization.append(normalize_time(w))
        elif year.match(w):
            normalization.append(num2words(int(w), to='year'))
        elif num.match(w):
            normalization.append(num2words(locale.atof(w)))
        else: # not an NSW
            normalization.append(w)
    
    return ' '.join(normalization).replace('-', ' ').replace(',', '')

def pronounce(text):
    pronunciation = []
    words = text.split()
    for w in text.split():
        # choose to ignore part after apostrophe for now
        if '\'' in w:
            w = w.split('\'')[0]
        if w.lower() in cmu_entries: # all entries in NLTK's cmudict are lowercase
            pronunciation.append(str(cmu_entries[w.lower()]))
        else:
            pronunciation.append(w)
    return '  '.join(pronunciation)

def normalize_date(w):
    """Normalizes a date in MM/DD/YY or MM/DD/YYYY format."""
    date = []
    w = w.split('/')
    month, day, year = w[0], w[1], w[2]
    if len(year) != 4: # if year format is YY
        # 20xx years only count up to 2025, otherwise 19xx
        if 0 <= int(year) <= 25:
            year = '20' + year
        else:
            year = '19' + year
    date.append(months[int(month) - 1])
    date.append(num2words(int(day), ordinal=True))
    date.append(num2words(int(year), to='year'))
    return ' '.join(date)

def normalize_acronym_ls(w):
    """
    Normalizes an acronym or a letter sequence that are two or more
    letters long.
    """
    return w if w.lower() in cmu_entries else ' '.join(w)

def normalize_email(w):
    """
    Normalizes an e-mail address with only one dot in the domain
    and whose top-level domain is three letters long.
    """
    email = []
    w = w.split('@')
    name, domain = w[0], w[1]
    email.extend(list(name))
    email.append('at')
    domain = domain.split('.')
    sld, tld = domain[0], domain[1]
    # handle sld
    if sld == 'gmail': # special case not handled by splitter
        email.extend(['g', 'mail'])
    elif splitter.split(sld) != '':
        email.extend(splitter.split(sld))
    else:
        email.extend(list(sld))
    email.append('dot')
    # handle tld
    if tld not in tlds:
        email.append(list(tld))
    else:
        email.append(tld)
    return ' '.join(email)

def normalize_abbrev(w):
    """
    Normalizes an abbreviation with a single capital letter followed
    by between zero and three lower case letters and a period.
    """
    return abbrevs[w] if w in abbrevs else w

def normalize_currency(w):
    """Normalizes a monetary amount in US dollars."""
    if w[0] == '$': w = w[1:]
    num = locale.atof(w)
    return num2words(num, to='currency', currency='USD').replace(',', '')

def normalize_time(w):
    """Normalizes time in HH:MM:SS or MM:SS format."""
    w = w.split(':')
    time = ''
    if len(w) == 3:
        h, m, s = w[0], w[1], w[2]
        return f'{num2words(h)} hours {num2words(m)} minutes and {num2words(s)} seconds'
    elif len(w) == 2:
        m, s = w[0], w[1]
        return f'{num2words(m)} minutes and {num2words(s)} seconds'

def main():
    # set locale for parsing numerical values with commas
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    choice = input('Test with a given file or self-input a text? (type F for file, S for self-input)\n')
    if choice == 'F':
        filename = input('Enter filename (choose from text1, text2, or text3): ')
        file = open(f'{filename}.txt', 'r')
        text = file.read()
        norm = normalize(text)
        f = open(f'output/{filename}_norm.txt', 'w')
        f.write(norm)
        f.close()
        pron = pronounce(norm)
        f = open(f'output/{filename}_pron.txt', 'w')
        f.write(pron)
        f.close()
        with open(f'output/{filename}_norm_pron.txt', 'w') as f:
            for n, p in zip(norm.split(), pron.split('  ')):
                f.write(f'{n}\t{p}\n')
    elif choice == 'S':
        text = input('Enter your text with NSWs below:\n')
        print('\nNormalized:')
        norm = normalize(text)
        print(norm)
        print('\nMatched to pronunciation:')
        pron = pronounce(norm)
        print(pron)
        print('\nPairs of normalized text - pronunciation:')
        for n, p in zip(norm.split(), pron.split('  ')):
            print(f'{n}\t{p}')
    else:
        print('Please choose either F or S when you rerun the program!')

if __name__ == '__main__':
    main()