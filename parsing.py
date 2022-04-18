from pyparsing import (CharsNotIn, Word, Literal, OneOrMore, alphanums, delimitedList, printables, alphas, nums, oneOf, Or, Combine, ZeroOrMore)
import sys

def makeDecoratingParseAction(marker):
    def parse_action_impl(s,l,t):
		#
        return (marker, t)
    return parse_action_impl

def parseRef(citation_str, debug = False):
  author_name_before_comma = CharsNotIn(',')
  abbreviated_name = Combine(Word(alphas.upper(), exact=1) + '.')

  unicodePrintables = ''.join(chr(c) for c in range(sys.maxunicode) 
                                        if not chr(c) in [' ', ';', ',', '.'])

  unicodePrintablesJournal = ''.join(chr(c) for c in range(sys.maxunicode) 
                                        if not chr(c) in [';', '.'])

  non_abbreviated_name = Word(unicodePrintables)

  name_component = (abbreviated_name | non_abbreviated_name)
  author_name_after_comma = OneOrMore(name_component)

  author = (author_name_before_comma("author_name_before_comma") + 
            Literal(',').suppress() + 
            author_name_after_comma("author_name_after_comma"))

  author_list = delimitedList(author, delim = ';')

  author.setParseAction(makeDecoratingParseAction("author"))

  author_list = (delimitedList(author, delim = ';') + Literal('.').suppress()) 

  sentence = (OneOrMore(Word(unicodePrintables, excludeChars='.'), stopOn=Literal('.')))

  title = sentence('Title')
  title = title.setParseAction(makeDecoratingParseAction("title"))

  sentenceJournal = OneOrMore(Word(unicodePrintablesJournal, excludeChars='.'), stopOn=Literal('.'))
  journal = sentenceJournal('Journal')
  journal = journal.setParseAction(makeDecoratingParseAction("journal"))

  valid_year = Word(nums, exact=4) + Literal('.').suppress()

  year = (valid_year | Literal('0') + Literal('.').suppress())
  year = year.setParseAction(makeDecoratingParseAction("year"))

  remaining_stuff = OneOrMore(Word(printables), stopOn=year)

  if debug:
    # to track the matching expressions
    non_abbreviated_name.setName("non_abbreviated_name").setDebug()
    abbreviated_name.setName("abbreviated_name").setDebug()
    author.setName("author").setDebug()
    author_list.setName("author_list").setDebug()
    sentence.setName("Sentence").setDebug()
    title.setName("title").setDebug()
    journal.setName("Journal").setDebug()
    remaining_stuff.setName("Remaining").setDebug()
  
  citation = (author_list('AuthorLst') + 
              title + 
              Literal('.') + 
              journal + 
              Literal('.') + 
              remaining_stuff +
              year)

  result = citation.parseString(citation_str)

  return result

def parseConferenceRef(citation_str, debug = False):
  author_name_before_comma = CharsNotIn(',')
  author_name_before_comma.setParseAction(makeDecoratingParseAction("author_name_before_comma"))
  abbreviated_name = Combine(Word(alphas.upper(), exact=1) + '.')

  unicodePrintables = ''.join(chr(c) for c in range(sys.maxunicode) 
                                        if not chr(c) in [' ', ';', ',', '.'])

  unicodePrintablesConference = ''.join(chr(c) for c in range(sys.maxunicode) 
                                        if not chr(c) in [';', '.'])

  non_abbreviated_name = Word(unicodePrintables)

  name_component = (abbreviated_name | non_abbreviated_name)
  author_name_after_comma = OneOrMore(name_component)
  author_name_after_comma.setParseAction(makeDecoratingParseAction("author_name_after_comma"))

  author = (author_name_before_comma("author_name_before_comma") + 
            Literal(',').suppress() + 
            author_name_after_comma("author_name_after_comma"))

  author_list = delimitedList(author, delim = ';')

  author.setParseAction(makeDecoratingParseAction("author"))

  author_list = (delimitedList(author, delim = ';') + Literal('.').suppress()) 

  sentence = (OneOrMore(Word(unicodePrintablesConference, excludeChars='.'), stopOn=Literal('.')))

  title = sentence('Title')
  title = title.setParseAction(makeDecoratingParseAction("title"))

  conference_name = Literal('Em: ').suppress() + OneOrMore(Word(unicodePrintablesConference, excludeChars='.,'), stopOn=Literal('.'))
  conference = conference_name('conference_name') + Literal(',').suppress()
  conference = conference.setParseAction(makeDecoratingParseAction("conference"))

  year = Word(nums, exact=4) + Literal('.').suppress()
  year = year.setParseAction(makeDecoratingParseAction("year"))

  remaining_stuff = ZeroOrMore(Word(printables), stopOn=year)

  if debug:
    # to track the matching expressions
    non_abbreviated_name.setName("non_abbreviated_name").setDebug()
    abbreviated_name.setName("abbreviated_name").setDebug()
    author.setName("author").setDebug()
    author_list.setName("author_list").setDebug()
    sentence.setName("Sentence").setDebug()
    title.setName("title").setDebug()
    conference.setName("conference_name").setDebug()
    year.setName("year").setDebug()
    remaining_stuff.setName("Remaining").setDebug()
  
  citation = (author_list('AuthorLst') + 
              title + 
              Literal('.') + 
              conference + 
              remaining_stuff +
              year)

  result = citation.parseString(citation_str)

  return result

def infosCitation(result):
    authors = []
    for element in result.asList():
        if element[0] == 'author':
            authors.append(element[1].asList())
        elif element[0] == 'title':
            title = element[1].asList()
            title = ' '.join(word for word in title)
        elif element[0] == 'journal':
            journal = element[1].asList()
            journal = ' '.join(word for word in journal)
        elif element[0] == 'year':
            year = element[1][0]
        
    return authors, title, journal, year

def parseJournalPublication(citation, c, debug = False):
    if c==0: result = parseRef(citation, debug = debug)
    elif c==1: result = parseConferenceRef(citation, debug = debug)
    return infosCitation(result)