
import secrets
import datetime

words1 = [
    "красный",
    "синий",
    "розовый",
    "чёрный",
    "фиолетовый",
    "белый",
    "жёлтый",
    "зелёный",
]

words2 = [
    "банан",
    "слон",
    "бык",
    "пёс",
    "лось",
    "орех",
    "плов",
    "утконос",
]

class Auth:
    @staticmethod
    def create_code_phrase():
        return "%s %s" % (secrets.choice(words1), secrets.choice(words2))

    @staticmethod
    def check(question, answer):
        word1, word2 = question.split()
        
        word1_index = words1.index(word1)
        word2_index = words2.index(word2)

        minute = datetime.datetime.minute - 1
        shift = minute // 20

        answer1_index = (word1_index + 1) * -1 - shift
        answer2_index = (word2_index + 1) * -1 - shift

        return answer == "%s %s" % (words1[answer1_index], words2[answer2_index])
