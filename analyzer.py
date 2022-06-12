from pyparsing import (CharsNotIn, 
                       Word, 
                       Literal, 
                       OneOrMore, 
                       alphanums, 
                       delimitedList, 
                       printables, 
                       alphas,
                       alphas8bit,
                       nums,
                       oneOf,
                       Or, 
                       Combine,
                       ZeroOrMore)

import sys

def makeDecoratingParseAction(marker):
    def parse_action_impl(s,l,t):
        return (marker, t)
    return parse_action_impl

def parseRef(citation_str, debug = False):
    author_name_before_comma = CharsNotIn(',')
    abbreviated_name = Combine(Word(alphas.upper(), exact=1) + '.'|' ')

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

    remaining_stuff = ZeroOrMore(Word(printables), stopOn=year)
    remaining_stuff = remaining_stuff.setParseAction(makeDecoratingParseAction("Remaining"))

    valid_qualis = (Word(alphanums, exact=2) | Literal('C')) + ZeroOrMore(Word(printables, excludeChars='.'))
    ni_qualis =  (Literal('Não identificado') + OneOrMore(Word(printables, excludeChars='.')))

    qualis = (valid_qualis | ni_qualis + Literal('.').suppress())
    qualis = qualis.setParseAction(makeDecoratingParseAction("qualis"))

   
    if debug:
        # to track the matching expressions
        non_abbreviated_name.setName("non_abbreviated_name").setDebug()
        abbreviated_name.setName("abbreviated_name").setDebug()
        author.setName("author").setDebug()
        author_list.setName("author_list").setDebug()
        sentence.setName("Sentence").setDebug()
        title.setName("title").setDebug()
        journal.setName("Journal").setDebug()
        year.setName("year").setDebug()
        remaining_stuff.setName("Remaining").setDebug()
        qualis.setName("qualis").setDebug()
    
    citation = (author_list('AuthorLst') + 
                title + 
                Literal('.') + 
                journal + 
                Literal('.') + 
                remaining_stuff +
                year +
                qualis)

    result = citation.parseString(citation_str)

    return result

def parseConferenceRef(citation_str, debug = False):
    author_name_before_comma = CharsNotIn(',')
    author_name_before_comma.setParseAction(makeDecoratingParseAction("author_name_before_comma"))
    abbreviated_name = Combine(Word(alphas.upper(), exact=1) + '.'|' ')

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

    sentence = (OneOrMore(Word(unicodePrintablesConference, excludeChars='.'), stopOn=Literal('. Em:')))
    sentence.ignore('.')
    
    title = sentence('Title')
    title = title.setParseAction(makeDecoratingParseAction("title"))

    conference_name = Literal('Em: ').suppress() + OneOrMore(Word(unicodePrintablesConference, excludeChars='.,'), stopOn=Literal('.'))
    conference = conference_name('conference_name') + Literal(',').suppress()
    conference = conference.setParseAction(makeDecoratingParseAction("conference"))

    year = Word(nums, exact=4) + Literal('.').suppress()
    year = year.setParseAction(makeDecoratingParseAction("year"))

    remaining_stuff = ZeroOrMore(Word(printables), stopOn=year)

    valid_qualis = (Word(alphanums, exact=2) | Literal('C')) + ZeroOrMore(Word(unicodePrintablesConference, excludeChars='.'))
    ni_qualis =  (Literal('Não identificado') + OneOrMore(Word(unicodePrintablesConference, excludeChars='.')))

    qualis = (valid_qualis | ni_qualis + Literal('.').suppress())
    qualis = qualis.setParseAction(makeDecoratingParseAction("qualis"))

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
        qualis.setName("qualis").setDebug()
    
    citation = (author_list('AuthorLst') + 
                title + 
                Literal('.') + 
                conference + 
                remaining_stuff +
                year +
                qualis)

    result = citation.parseString(citation_str)

    return result

def infosCitation(result):
    authors = []
    for element in result.asList():
        if element[0] == 'author':
            try: authors.append(element[1][0][1].asList() + element[1][1][1].asList())
            except: authors.append(element[1].asList())
        elif element[0] == 'title':
            title = element[1].asList()
            title = ' '.join(word for word in title)
        elif element[0] == 'journal':
            journal = element[1].asList()
            journal = ' '.join(word for word in journal)
        elif element[0] == 'conference':
            conference = element[1].asList()
            conference = ' '.join(word for word in conference)
        elif element[0] == 'Remaining':
            remaining = element[1].asList()
            remaining = ' '.join(word for word in remaining)                
            l = remaining.find('issn: ') + 6
            issn = remaining[l:l+9]
        elif element[0] == 'year':
            year = element[1][0]
        elif element[0] == 'qualis':
            qualis = element[1].asList()
            qualis = ' '.join(word for word in qualis)

    try: return authors, title, journal, issn, year, qualis
    except: return authors, title, conference, year, qualis

def parseJournalPublication(citation, debug = False):
    result = parseRef(citation, debug = debug)
    return infosCitation(result)

def parseConferencePublication(citation, debug = False):
    result = parseConferenceRef(citation, debug = debug)
    return infosCitation(result)
