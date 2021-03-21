import re
import redis

rds = redis.Redis(host='localhost', port=6379, db=0)
reg = r"[^a-zA-Z0-9.,;'\":\ !$%&*\(\)\+\-\\\?\/\~\`\{\}\[\]\<\>\€\?\_]+"


def GetVideo(youtubeVideoId, startTime, endTime):
    response = """
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/{}?start={}&end={}" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media;" 
        allowfullscreen
    >
    </iframe>
    """
    return response.format(youtubeVideoId, startTime, endTime)

def GetPhrases(wordsString):
    words = re.split('(\W)', wordsString)
    synonyms = []
    for word in words:
        wordSynonyms = GetSynonyms(word)
        for synonym in wordSynonyms:
            synonyms.append(synonym)
    sentencesDict = dict()
    for word in synonyms:
        sentences = rds.smembers(word + ":sentences")
        for sentence in sentences:
            key = Decode(sentence)
            sentenceText = Decode(rds.get(key+ ":text"))
            sentenceWords = re.split('(\W)', sentenceText)
            value = GetSimilarityValue(words, sentenceWords)
            sentencesDict[key] = sentencesDict.get(key, 0) + value
    resultSentences = {k: v for k, v in sorted(sentencesDict.items(), key=lambda item: item[1], reverse=True)}
    return resultSentences

def GetPhrasesReport(wordsString):
    resultSentences = GetPhrases(wordsString)
    counter = 0
    result = []
    topN = 3
    for resultSentence in resultSentences.items():
        sentenceId = resultSentence[0]
        sentenceText = Decode(rds.get(sentenceId+ ":text"))
        sentenceVideo = Decode(rds.get(sentenceId + ":video"))
        videoData = sentenceVideo.split(';')
        result.append((sentenceText, videoData[0], videoData[1], videoData[2]))
        counter += 1
        if topN == counter:
            break
    return result

def Decode(bytesStr):
    if bytesStr is not None:
        return bytesStr.decode("utf-8")
    else:
        return None
    