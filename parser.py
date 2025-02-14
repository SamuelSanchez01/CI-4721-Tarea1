import re
from parsec import *

#Espacios en blanco
whiteSpace = regex(r'\s*', re.MULTILINE)

lexeme = lambda p: p << whiteSpace

#Atomos
leftBrace = lexeme(string('{'))
rightBrace = lexeme(string('}'))
leftBracket = lexeme(string('['))
rightBracket = lexeme(string(']'))
colonSymbol = lexeme(string(':'))
commaSymbol = lexeme(string(','))
trueValue = lexeme(string("true"))
falseValue = lexeme(string("false"))
nullValue = lexeme(string("null"))

#Numeros
def integer():
    return lexeme(
        regex(r'-?(0|[1-9][0-9]*)')
    )

#Strings
def stringContents():
    return regex(r'[^"\\]')

#Funcion que parsea un string entre comillas dobles
@lexeme
@generate
def parseQuotedString():
    yield string('"')
    body = yield many(stringContents())
    yield string('"')

#Funcion que parsea una lista de pares clave-valor separados por comas
@generate
def parseKeyValuePairList():
    yield parseQuotedString
    yield colonSymbol
    yield jsonValue
    yield parseKeyValueListCont

#Funcion que parsea la continuación de la lista de pares clave-valor
@generate
def parseKeyValueListContExists():
    yield commaSymbol
    yield parseKeyValuePairList

#Funcion que parsea el contenido de la lista de pares clave-valor
@generate
def parseKeyValueListCont():
    yield parseKeyValueListContExists | whiteSpace

#Funcion que parsea una lista de valores separados por comas
@generate
def parseValueList():
    yield jsonValue
    yield parseValueListCont

#Funcion que parsea la continuación de la lista de valores
@generate
def parseValueListContExists():
    yield commaSymbol
    yield parseValueList

#Funcion que parsea el contenido de la lista de valores
@generate
def parseValueListCont():
    yield parseValueListContExists | whiteSpace

#Funcion que parsea un arreglo JSON
@generate
def parseJsonArray():
    yield leftBracket
    yield parseValueList | whiteSpace
    yield rightBracket

#Funcion que parsea un objeto JSON
@generate
def parseJsonObject():
    yield leftBrace
    yield (parseKeyValuePairList | whiteSpace)
    yield rightBrace

#Definiciones para valores
boolean = trueValue | falseValue
jsonValue = boolean | integer() | parseQuotedString | parseJsonObject | parseJsonArray

#Parseo del JSON
json = whiteSpace >> parseJsonObject

#Test
#True en vez de true
false1 = '''
{
"name":"John",
"age":30,
"cars":["Ford", "BMW", "Fiat"],
"work":True
}
'''
#una coma de mas
false2 = '''
{
"name":"John",
"age":30,
"cars":["Ford", "BMW", "Fiat"],
"work":true,
}
'''
#una comilla menos
false3 = '''
{
"name":"John,
"age":30,
"cars":["Ford", "BMW", "Fiat"],
"work":true
}
'''
true1 = '''
{
"name":"John",
"age":30,
"cars":["Ford", "BMW", "Fiat"],
"work":true
}
'''

try:
    json.parse(false1)
    print("JSON object parsed successfully!")
except:
    print("Failed to parse JSON object.")

try:
    json.parse(false2)
    print("JSON object parsed successfully!")
except:
    print("Failed to parse JSON object.")
  
try:
    json.parse(false3)
    print("JSON object parsed successfully!")
except:
    print("Failed to parse JSON object.")

try:
    json.parse(true1)
    print("JSON object parsed successfully!")
except:
    print("Failed to parse JSON object.")
