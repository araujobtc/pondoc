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

    unicodePrintablesConferJournal = ''.join(chr(c) for c in range(sys.maxunicode) 
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

    sentence = (OneOrMore(Word(unicodePrintablesConferJournal, excludeChars='.'), stopOn=Literal('.')))
    
    title = sentence('Title')
    title = title.setParseAction(makeDecoratingParseAction("title"))

    conference = Literal('EM: ').suppress() + OneOrMore(Word(unicodePrintablesConferJournal, excludeChars='.,'), stopOn=Literal('.'))
    journal = OneOrMore(Word(unicodePrintablesConferJournal, excludeChars='.'), stopOn=Literal('.'))
    
    conferjournal_name = (conference|journal)
    conferjournal = conferjournal_name('conferjournal_name') + (Literal(',').suppress()|Literal('.').suppress())
    conferjournal = conferjournal.setParseAction(makeDecoratingParseAction("conference_journal"))

    valid_year = Word(nums, exact=4) + Literal('.').suppress()

    year = (valid_year | Literal('0') + Literal('.').suppress())
    year = year.setParseAction(makeDecoratingParseAction("year"))

    remaining_stuff = ZeroOrMore(Word(printables), stopOn=year)
    remaining_stuff = remaining_stuff.setParseAction(makeDecoratingParseAction("Remaining"))

    valid_qualis = (Word(alphanums, exact=2) | Literal('C')) + ZeroOrMore(Word(printables, excludeChars='.'))
    ni_qualis =  (Literal('NÃO IDENTIFICADO') + OneOrMore(Word(printables, excludeChars='.')))

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
        conferjournal.setName("conference_journal").setDebug()
        year.setName("year").setDebug()
        remaining_stuff.setName("Remaining").setDebug()
        qualis.setName("qualis").setDebug()
    
    citation = (author_list('AuthorLst') + 
                title + 
                Literal('.') + 
                conferjournal + 
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
        elif element[0] == 'conference_journal':
            conference_journal = element[1].asList()
            conference_journal = ' '.join(word for word in conference_journal)
        elif element[0] == 'Remaining':
            remaining = element[1].asList()
            remaining = ' '.join(word for word in remaining)
            if 'ISSN' in remaining:                
                l = remaining.find('ISSN: ') + 6
                issn = remaining[l:l+9]
        elif element[0] == 'year':
            year = element[1][0]
        elif element[0] == 'qualis':
            qualis = element[1].asList()
            qualis = ' '.join(word for word in qualis)

    try: return authors, title, conference_journal, issn, year, qualis
    except: return authors, title, conference_journal, year, qualis

def parsePublication(citation, debug = False):
    result = parseRef(citation, debug = debug)
    return infosCitation(result)
