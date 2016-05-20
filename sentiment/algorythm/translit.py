# код взят с http://paxoblog.blogspot.ru/2006/11/translitpy.html

# -*- coding: utf-8 -*-
#dron@amerigo 200611031405

def translit(s):
  "Russian translit: converts 'привет'->'privet'"
  # assert s is not str, "Error: argument MUST be string"
  print(type(s))
  table1 = str.maketrans("абвгдеёзийклмнопрстуфхъыьэАБВГДЕЁЗИЙКЛМНОПРСТУФХЪЫЬЭ",
        "abvgdeezijklmnoprstufh'y'eABVGDEEZIJKLMNOPRSTUFH'Y'E")
  table2 = {'ж':'zh','ц':'ts','ч':'ch','ш':'sh','щ':'sch','ю':'ju','я':'ja',
          'Ж':'Zh','Ц':'Ts','Ч':'Ch','Ш':'Sh','Щ':'Sch','Ю':'Ju','Я':'Ja'}

  for k in table2.keys():
     s = str(s.replace(k,table2[k]))

  return s.translate(table1)

if __name__=="__main__":
    print(translit("Привет питон. Что транслитерировать-то, я чёт не понял!"))