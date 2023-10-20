import requests as r
import json
import random

def write_arq(url):
  res = r.get(url)
  dic = json.loads(res.text)
  jsonStr = json.dumps(dic)
  with open("personagens.json", "w") as arq:
    arq.write(jsonStr)

def read_crud(url):
  res = r.get(url)
  if res.text == "[]":
    print("A API esta vazia")
    return
  dic = json.loads(res.text)
  for elem in dic:
    print("\nid = %s, nome = %s, descricao = %s, genero = %s, raca = %s" %(elem["_id"], elem["name"], elem["descricao"], elem["genero"], elem["raca"]))

def search_crud(url, id):
  res = r.get(url)
  if res.text == "[]":
    print("\nA API esta vazia")
    return
  res = r.get(url+"/"+id)
  if not res:
    print("\nNao existe personagem com esse id")
    return
  dic = json.loads(res.text)
  print("\nid = %s, nome = %s, descricao = %s, genero = %s, raca = %s" %(dic["_id"], dic["name"], dic["descricao"], dic["genero"], dic["raca"]))

def post_crud(url, nome, descricao, genero, raca):
  newCharacter = {
      "name": nome,
      "descricao": descricao,
      "genero": genero, 
      "raca": raca
    }
  r.post(url, json=newCharacter, timeout = 5)

def insert_manually(url):
  nome = input("\nInsira o nome do novo personagem: ")
  descricao = input("\nInsira a descricao do novo personagem: ")
  genero = input("\nInsira o genero do novo personagem: ")
  raca = input("\nInsira a raca do novo personagem: ")
  post_crud(url,nome,descricao,genero,raca)
  
def update_crud(url, id):
  res = r.get(url)
  if res.text == "[]":
    print("\nA API esta vazia")
    return  
  nome = input("Insira a atualizazao que deseja para o nome: ")
  descricao = input("Insira a atualizazao que deseja para a descricao: ")
  genero = input("Insira a atualizazao que deseja para o genero: ")
  raca = input("Insira a atualizazao que deseja para a raca: ")
  attCharacter = {
      "name": nome,
      "descricao": descricao,
      "genero": genero, 
      "raca": raca
    }
  res = r.put(url+"/"+id, json=attCharacter, timeout=5)
  if not res:
    print("\nNao existe personagem com esse id")
    return
  print(res.text)
  """
  dic = json.loads(res.text)
  print(dic)
  print(dic["count"])
  if dic["count"] == 0:
    print("\nNao existe personagem com esse id")
  """
def delete_crud(url, id):
  res = r.get(url)
  if res.text == "[]":
    print("\nA API esta vazia")
    return  
  res = r.get(url+"/"+id)
  if not res:
    print("\nNao existe personagem com esse id")
    return
  res = r.delete(url+"/"+id, timeout=5)  
  
def search_name(url, nom):
  res = r.get("https://zelda.fanapis.com/api/characters?name="+nom)
  dic = json.loads(res.text)
  qtd = dic["count"] 
  if qtd == 0:
    print("Nao foi possivel achar esse nome")
  i = 0
  while qtd != 0:
    res = r.get("https://zelda.fanapis.com/api/characters?name="+nom+"&page="+str(i))
    dic = json.loads(res.text)
    qtd = dic["count"]
    if qtd == 0:  
      break
    
    for elem in dic["data"]:
      resp = input("\n%s - e esse personagem que voce que adicionar? (Insira s para sim}: " %elem["name"])
      if resp == "s" or resp == "S":
        nome = elem["name"]
        descricao = elem["description"]
        genero = elem["gender"] #é possível que ele recebe null, que no caso não é um str
        if genero == None or genero == " ":
          genero = "-"
        raca = elem["race"] #é possível que ele recebe null, que no caso não é um str
        if raca == None or raca == " ":
          raca = "-" 
        post_crud(url, nome, descricao, genero, raca)
        break
    i+=1

def search_aleatory_name(url):
  res = r.get("https://zelda.fanapis.com/api/characters")
  dic = json.loads(res.text)
  qtd = dic["count"]
  sort_i = random.randint(0,83)
  j = 0
  response = r.get("https://zelda.fanapis.com/api/characters?limit=20&page=%s"%str(sort_i)) #sao 83 pags ao todo
  dic = json.loads(response.text)
  qtd = dic["count"]
      
  sort_j = random.randint(0,qtd-1)
  for elem in dic["data"]:
    if j == sort_j:
      nome = elem["name"]
      descricao = elem["description"]
      genero = elem["gender"]
      if genero == None or genero == " ":
        genero = "-"
      raca = elem["race"]
      if raca == None or raca == " ":
        raca = "-" 
      print("\nPersonagem escolhido: nome = %s, descricao = %s, genero = %s, raca = %s" %(nome, descricao, genero, raca))
      post_crud(url,nome,descricao,genero,raca)
      break
    else:
      j += 1

  #return l

def get_from_API(url):
  op = input("\nDeseja procurar um personagem especifico pelo nome?(responda usando s para sim. Senao, pegara um personagem aleatorio): ")
  if op == "s" or op == "S":
    nom = input("\nInsira o nome: ")
    nom = nom[0].upper() + nom[1:].lower()
    search_name(url,nom)
  else:
    search_aleatory_name(url)
  
def main():
  url = "https://crudcrud.com/api/142a6b99f2fb4c92951ca73402c71e31/characters"
  
  op = input("Insira a opcao desejada (Se deseja pegar alguma personagem do Zelda API, insira o numero 6 e se deseja terminar o programa, insira 7): ")
    
  while op != "7":
    if op == "1":
      read_crud(url)
    
    elif op == "2":
      id = input("Insira o id do personagem que deseja encontrar: ")
      search_crud(url, id)
    
    elif op == "3":
      insert_manually(url)
    
    elif op == "4":
      id = input("Insira o id do personagem que deseja atualizar: ")
      update_crud(url, id)
    
    elif op == "5":
      id = input("Insira o id do personagem que deseja deletar: ")
      delete_crud(url, id)
    
    elif op == "6":
      get_from_API(url)
    
    elif op == "7":
      break
    
    else:
      print("Codigo para comando inexistente, insire um valor valido")
    print("\n")
    op = input("Insira a opcao desejada (Se deseja pegar alguma personagem do Zelda API, insira o numero 6 e se deseja terminar o programa, insira 7): ")

  write_arq(url)  
  
main()