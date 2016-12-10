from .new_snt_to_ldg import get_dep_str
from nltk.parse import DependencyGraph
import nltk
import records
from copy import deepcopy
from pprint import pprint
from collections import Counter



def snt_has_words(snt, words):
    """
    check whether sentence has words
    :param snt: a string
    :param words: a list of words
    :return: boolean
    """
    wlst = nltk.word_tokenize(snt)
    for word in words:
        if word not in wlst:
            return False
    return True


def make_word_list_from_phrase(phrase):
    """
    phrase is a string may containing words, and '.'
    remove all '.', and return a list of words
    :param phrase:
    :return: a list of words
    """
    phrase = phrase.replace('.', ' ').strip()
    return nltk.word_tokenize(phrase)


def get_root_address_from_nltkg(g, rootRels=['root', 'HED']):
    """
    get root address from an nltk graph instance
    :param g:
    :return: an integer
    """
    rlt = []
    for i in g.nodes.keys():
        if g.nodes[i]['rel'] in rootRels:
            rlt.append(i)
    return rlt


def get_address_of_word(nltkg, word):
    """
    get all node addresses with 'word'=word
    :param nltkg:
    :param word:
    :return:
    """
    rlt = []
    for i in nltkg.nodes.keys():
        if word in nltkg.nodes[i].values():
            rlt.append(i)
    if len(rlt) > 1:
        print("{} appears in more than one place \n".format(word))
    return rlt


def get_addresses_from_child_to_ancestor(g, startAddress, endAddress, stop=[]):
    """
    return addresses located between startAddress and endAddress, may be interrupted if encounters ids in stop list.
    :param startAdress: start address
    :param Endaddress: end address
    :return: a list of address
    """
    rlt = []
    if not stop:
        stop = get_root_address_from_nltkg(g)
    assert type(endAddress) != list
    currentAddress = startAddress
    while currentAddress != endAddress and currentAddress not in stop:
        if currentAddress != endAddress:
            rlt.append(currentAddress)
        if currentAddress in stop:
            break
        currentAddress = g.nodes[currentAddress]['head']
    if currentAddress == endAddress:
        return rlt[1:]
    else:
        return []


def get_root_of_node(nltkg, nodeAddress, rootRels=['root', 'HED']):
    """
    get root address of node with nodeAddress
    :param nltkg:
    :param address:
    :return:
    """
    address = nodeAddress
    while nltkg.nodes[address]['rel'] not in rootRels:
        address = nltkg.nodes[address]['head']
    return address


def minimal_connected_graph(nltkg, wlst):
    """
    create a new graph, which is a sub-graph of nltkg, and contains words in wlst
    :process find the root address; find address of each word  in wlst, record back-trace from each word to root
    :param nltkg: an instance of nltkg
    :param wlst: a list of words
    :return: a new graph
    """
    newg = deepcopy(nltkg)
    addressLst = []
    rootAddress = get_root_address_from_nltkg(newg)
    for word in wlst:
        wordAddress = get_address_of_word(newg, word)
        for address in wordAddress:
            root = get_root_of_node(nltkg, address)
            addressBetween = get_addresses_from_child_to_ancestor(newg, address, root,  stop=rootAddress)
            if root not in addressLst:
                addressLst += [root]
            addressLst += [address] + addressBetween
    for i in list(newg.nodes.keys()):
        if i not in addressLst:
            newg.remove_by_address(i)
    return newg


def minimal_connected_frame_graph(nltkg, wlst):
    """
    extend minimal_connected_graph, if word in wlst is has frame word in its children
    replace it with its v/a child
    :param nltkg: an instance of nltkg
    :param wlst: word list
    :return: a new graph
    """
    g = minimal_connected_graph(nltkg, wlst)
    for address in list(g.nodes.keys()):
        if g.nodes[address]['word'] in wlst:
            for key in get_children_addresses(nltkg, address):
                if is_frame_word(nltkg.nodes[key]) and not is_frame_word(g.nodes[address]):
                    g.nodes[key]=nltkg.nodes[key]
    return g


def get_children_addresses(nltkg, address):
    """

    :param nltk:
    :param address:
    :return:
    """
    return sum(nltkg.nodes[address]['deps'].values(),[])


def is_frame_word(nltkNode, ffeat=['V', 'A']):
    """
    :param nltkNode:
    :return: boolean
    """
    print(nltkNode)
    if nltkNode['tag'].upper() in ffeat or nltkNode['ctag'] in ffeat:
        return True
    return False


def nltkg_to_cnll(nltkg):
    """
    transform an nltk graph into cnll10 string
    :param nltkg: a nltk graph
    :return: cnll10 string of nltkg
    """
    cnll10=""
    pprint(nltkg.nodes)
    for key in nltkg.nodes:
        node = nltkg.nodes[key]
        for key in ["address", "lemma", "ctag", "tag", "feats", "head", "rel"]:
            cnll10 += "{} ".format(node.get(key, '_'))
        cnll10 += " _ _ \n"
    print(cnll10)
    return cnll10


def create_conjunction_pattern(conjStr, sampleSnt, lan='de'):
    """
    ! for learning, conjStr appear in sampleSnt only in the expected sub-graph !
    conjStr is a string of conjunction words, e.g. because, weil, not only...but also
    sampleStr is a sample sentence containing conjStr
    the function is to identify the graphical pattern of conjStr in the ldg of sampleStr
    Step 1: get ldg (cnll10) of sampleSnt, transform into nltk format
    Step 2: copy out the minimal connected sub-component of nltk graph containing words in conjStr and root
    Step 3: transform back to cnll10 format
    Step 4: print out cnll10, if needs, save to database
    if saveDb is true, the result will be saved in database
    :param conjStr: a string of conjunction words
    :param sampleSnt: a sample usage of conjunction words
    :param lan: language
    :param saveDb: boolean
    :return: cnll10 format of a sub-graph
    """
    # conjStr = conjStr.upper()
    # sampleSnt = sampleSnt.upper()
    cnll = get_dep_str(sampleSnt,lan=lan)
    cnll = cnll.replace('_ _ _', '_ _') + '\n'
    print(cnll)
    nltkg = DependencyGraph(cnll)
    wlst = make_word_list_from_phrase(conjStr)
    assert snt_has_words(sampleSnt, wlst)
    subg = minimal_connected_graph(nltkg, wlst)
    subgf = minimal_connected_frame_graph(nltkg, wlst)
    cnllStr = nltkg_to_cnll(subg)
    cnllStr1 = nltkg_to_cnll(subgf)
    return cnllStr, cnllStr1


def get_query_result_from_db(database, queryStr):
    """

    :param database:
    :param queryStr:
    :return: a list of records, each record is a list
    """
    db = records.Database(database)
    rlt = [list(map(lambda ele: ele.strip(), rd.as_dict().values())) for rd in db.query(queryStr)]
    return rlt


def is_valid_sample(phrase, snt):
    """
    snt is a valid sample for phrase, if phrase appears in snt, words of phrase only appear in
    the phrase.
    :param phrase:
    :param snt:
    :return:
    """
    phrase0 = ' '.join(phrase.split())
    snt0 = nltk.word_tokenize(snt)
    while '..' in phrase0:
        phrase0 = phrase0.replace('..', '.')
    phraseParts = phrase0.split('.')
    for part in phraseParts:
        if part not in snt0:
            return False
    phrase0 = phrase0.replace('.', ' ')
    wlst = nltk.word_tokenize(phrase0)
    wDic = Counter(wlst)
    sDic = Counter(snt0)
    for word in wDic.keys():
        if sDic[word] > wDic[word]:
            return False
    return True


def do_transaction(database, queryTranscation):
    db = records.Database(database)
    tx = db.transaction()
    try:
        print(queryTranscation)
        db.query(queryTranscation)
        tx.commit()
    except:
        tx.rollback()
        return False


def learn_phrase_patterns(lan='en', database='', phraseQuery='', sampleQuery='', queryFormat=''):
    """
    we know a phrase, and (search for) sample sentences containing this phrase.
    get ldg pattern of this phrase, and save phrase,sample sentence, pattern into pattern-dic table in database
    ! words in the phrase shall appear only in the phrases !, otherwise, that is a bad sample, not choose as a sample
    Step 1: get phrase lists
    Step 2: get sample lists
    Step 3: for each phrase in phrase list:
              for each sample in list:
                   if (1) phrase appears in sample, and (2) phrase words only appear in phrase
                        cnllStr, cnllStr1 = create_conjunction_pattern(phrase, sample, lan=lan, saveDb=True)
                        save cnllStr and cnllStr1 into database
                        increase counter
    :param lan:
    :param database: name of the database
    :param phraseQuery:
    :param sampleQuery:
    :param saveQueryFormat:
    :return: number of phrase patterns learned
    """
    phraseLst = sum(get_query_result_from_db(database, phraseQuery), [])
    sampleLst = sum(get_query_result_from_db(database, sampleQuery), [])
    count = 0
    for phrase in phraseLst:
        for snt in sampleLst:
            if is_valid_sample(phrase, snt):
                cnllStr, cnllStr1 = create_conjunction_pattern(phrase, snt, lan=lan)
                cnllStr = cnllStr.replace('\n', '*')
                cnllStr1 = cnllStr1.replace('\n', '*')
                do_transaction(database, queryFormat.format(count, phrase, cnllStr, cnllStr1, snt, 1))
                count += 1
    return count
