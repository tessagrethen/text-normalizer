# Text Normalizer
## LING 208 Final Project - Tessa Pham

### Instructions
1. User can either input a text with NSWs or choose one of 3 files already given:
    * text input: output will be shown on the terminal
    * given file: output will be saved in `output` folder with 3 files (`<filename>_norm.txt` for normalized text, `<filename>_pron.txt` for pronunciations, `<filename>_norm_pron.txt` for list of normalized text - pronunciation pairs)
2. The `output` folder already has output files for all 3 example texts (for reference). User can choose to delete these files and regenerate them, or simply running the program again would overwrite these files.
3. Please refer to `requirements.txt` for required Python package installations.

### NSW Categories
This text normalizer identifies, categorizes, and normalizes text for these categories (with specified conditions for identification):

1. acronym or letter sequence: all capitalized, 2 or more letters long
2. date: in MM/DD/YY or MM/DD/YYYY format
3. e-mail address: only 1 dot in the domain, top-level domain is 3 letters long
4. abbreviation: a single capital letter followed by between zero and three lower case letters and a period
5. monetary amount: in US dollars, has '$' prepended
6. year: 19xx or 20xx, interpreted as a number otherwise
7. number: can have optional commas and decimal places, consistent comma pattern
8. time: in HH:MM:SS or MM:SS format
9. hyphenated string
10. string with apostrophe

### To Pronunciation
Normalized text is then matched with pronunciations from the CMU Pronouncing Dictionary provided in NLTK.

### Notes
* Punctuations are removed in order to get a higher number of words matched with their pronunciations. Sentence boundaries can still be easily identified by words with capitalized first letters for the most part.
* Strings with apostrophe are partly handled: apostrophe and the part that follows are discarded.

### References
* `text1.txt` was given in Lab 1.
* `text2.txt` is taken from the Text Normalization handout, which was modified from: https://www.boston.com/sports/sports-news/2017/11/05/watch-the-emotional-moments-of-shalane-flanagans-new-york-city-marathon-win.
* `text3.txt` is an article on CNN: https://www.cnn.com/2019/12/19/politics/pete-buttigieg-wine-cave-elizabeth-warren-debate/index.html.



