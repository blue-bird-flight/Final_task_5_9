from django import template
register = template.Library()

censor_words1 = [
    'дураки', 'дурака',
    'дураков', 'дурак',
    'сволочи', 'сволочь',
    'сволоч',
    'дебилы', 'дебил',
    'кретины', 'кретин',
    'недоумки', 'недоумок',
]


@register.filter()
def censor(value):
    try:
        words = value.lower()
        for word in censor_words1:
            if word in words:
                word_chenge = word[0] + "*" * (len(word) - 1) + '!'
                value = value.replace(word, word_chenge)
        return value

    except TypeError:
        print(f'фильтр не применим к {type(value)}')
    return f'{value} Р'


