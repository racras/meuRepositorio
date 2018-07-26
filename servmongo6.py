# mongo.py

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['MONGO_DBNAME'] = 'produtos'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/produtos'
app.wsgi_app
mongo = PyMongo(app)


## Mapeia a url , define ,o metodo , da uma lupada na collections(tabela), escreve o json e o retorna todos os produtos
@app.route('/produto', methods=['GET'])
def get_all_produtos():
  produto = mongo.db.prod
  output = []
  for s in produto.find():
    output.append({'produto_id' : s['produto_id'],'nome' : s['nome'], 'num_max_parcela' : s['num_max_parcela'],'seguradora_cod_susep' : s['seguradora_cod_susep']})
  return jsonify({'result': output})
    

## Mapeia a url , define ,o metodo , receb o parametro ,o busca na collections(tabela), escreve o json e o retorna o produto
@app.route('/produto/<int:produto_id>', methods=['GET'])
def get_one_produtos(produto_id):
  print(produto_id)
  produto = mongo.db.prod
  s = produto.find_one({'produto_id' : produto_id})
  if s:
    output = {'produto_id' : s['produto_id'],'nome' : s['nome'], 'num_max_parcela' : s['num_max_parcela'],'seguradora_cod_susep' : s['seguradora_cod_susep']}
  else:
     output = {'produto_id' : 0,'nome':'nadauuuuuudada'}
  return jsonify({'result' : output})

@app.route('/produto', methods=['POST'])
def add_produto():
  produto = mongo.db.prod
  nome = request.json['nome']
  produto_id = request.json['produto_id']
  num_max_parcela = request.json['num_max_parcela']
  seguradora_cod_susep = request.json['seguradora_cod_susep']
  
  insere_produto = produto.insert({'nome': nome , 'produto_id': produto_id ,'num_max_parcela' : num_max_parcela, 'seguradora_cod_susep' : seguradora_cod_susep})
  novo_produto = produto.find_one({'produto_id': produto_id })
  output = {'nome' : novo_produto['nome'], 'produto_id' : novo_produto['produto_id'] , 'num_max_parcela' : novo_produto['num_max_parcela'] , 'seguradora_cod_susep' : novo_produto['seguradora_cod_susep']}
  
  return jsonify({'result' : output})

@app.route('/produto/excluir/<int:produto_id>', methods=['GET'])
def deleta_produtos(produto_id):
  produto = mongo.db.prod
  s = produto.find_one({'produto_id' : produto_id})
  if s:
    deleta_produto = produto.remove({'produto_id' : produto_id})
    output = "Produto - " + str(produto_id) + " removido com sucesso"
  else:
    output = "Nada, Não achou nada"
  return jsonify({'result' : output})

if __name__ == '__main__':
   app.run(debug=True)
