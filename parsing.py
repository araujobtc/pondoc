from pyparsing import (CharsNotIn, Word, Literal, OneOrMore, alphanums, delimitedList, printables, alphas, nums)

def makeDecoratingParseAction(marker):
    def parse_action_impl(s,l,t):
		#
        return (marker, t)
    return parse_action_impl

def parseRef(citation_str):
	family_name = CharsNotIn(',')

	first_init = Word(alphas.upper(), '.', max=2)

	author = (family_name("LastName") + Literal(',').suppress() + 
				OneOrMore(first_init("FirstInitials") ) )

	last_author = (family_name("LastName") + Literal(',').suppress() + 
				OneOrMore(first_init("FirstInitials") ) )

	author.setParseAction(makeDecoratingParseAction("author"))

	last_author.setName("last_author").setDebug()

	author_list = (delimitedList(author, delim = ';') + Literal('.').suppress()) 

	sentence = (OneOrMore(Word(printables, excludeChars='.'), stopOn=Literal('.')))

	title = sentence('Title')
	title = title.setParseAction(makeDecoratingParseAction("title"))

	journal = sentence('Journal')
	journal = journal.setParseAction(makeDecoratingParseAction("journal"))

	year = Word(nums, exact=4) + Literal('.').suppress()
	year = year.setParseAction(makeDecoratingParseAction("year"))

	remaining_stuff = OneOrMore(Word(printables), stopOn=year)

	# to track the matching expressions
	author.setName("author").setDebug()
	author_list.setName("author_list").setDebug()
	sentence.setName("Sentence").setDebug()
	title.setName("title").setDebug()
	journal.setName("Journal").setDebug()
	remaining_stuff.setName("Remaining").setDebug()
	family_name.setName("family_name").setDebug()

	citation = (author_list('AuthorLst') + title + Literal('.') + journal + Literal('.') + remaining_stuff + year)

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

def getRefComponents(citation):
    result = parseRef(citation)
    return infosCitation(result)