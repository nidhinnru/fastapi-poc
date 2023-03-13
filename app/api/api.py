import json
import random

def random_res(request):
    body = request.decode("utf-8")
    random_word = random.sample(body, len(body))
    jumbled = ''.join(random_word)
    return jumbled
