# import pymorphy2
# import re
# morph = pymorphy2.MorphAnalyzer()
#
# q = 'THE STARKILLERS I Китайский Лётчик Джао Да 15.10 22/10 В.Самойлов / Агата Кристи / Все хиты ПСКОВ'
#
# # select * from events where tags is null
# # w = re.sub("/^[a-zа-яё\d]{1}[a-zа-яё\d\s]*[a-zа-яё\d]{1}$/i", q)
# for w in re.sub(r'[^\w\s]', '', q).split(' '):
#     p = morph.parse(w)[0]
#     if 'NOUN' in p.tag:
#         print(p.normal_form)