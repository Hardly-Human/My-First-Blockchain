# Module 1 -- Create a Block Chain

#installed libraries 
# pip install flask==0.12.2
# install postman app


#importing libraries
import datetime
import hashlib
import json
from flask import Flask,jsonify

# part 1 = Buliding Blockchain
class Blockchain:
    
    def __init__(self):
        self.chain = []     #block chain variable
        # creating Genesis block
        self.create_block(proof = 1,previous_hash = '0000')
        
    def create_block(self, proof, previous_hash):
       
        block = { 'index' : (len(self.chain)+1),
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof ,
                 'previous_hash' : previous_hash
                }
        self.chain.append(block)
        return block
     
    def get_previous_block(self):
        
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False :   #designing problem for miners.....
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
                
        return new_proof        
      
    def hash(self, block):  # creating hash of a block by converting it into json string and feeding to sha256...
        
        encoded_block = json.dumps(block, sort_keys = True).encode()
        
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1 
        
        while block_index < len(chain):
            current_block = chain[block_index]
            
            # validating previous hash
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            
            # validating proof of work as '0000'
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            
            hash_operation = hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:4] != '0000':
                return False
            
            previous_block = current_block
            block_index +=1
            
        return True   
    


        
# part 2 = Mining our Blockchain

# create a web app
app = Flask(__name__)    
    

# Creating a Block chain
        
blockchain = Blockchain()

# Mining a new Block 

@app.route('/mine_block',methods = ['GET'])

def mine_block():
    
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    
    previous_hash = blockchain.hash(previous_block)
    
    block = blockchain.create_block(proof,previous_hash)
    
    response = {
                'Message' : 'Congrats!!you have successfully mined a block',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']
            }
    
    return jsonify(response),200
    

# getting full Blockchain displayed...
    
@app.route('/get_chain',methods = ['GET'])

def get_chain():
    response = {
                'chain' : blockchain.chain,
                'length' : len(blockchain.chain)    
                }
    return jsonify(response),200


# validating block chain
    
@app.route('/is_valid',methods =['GET'])

def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    response = { 'Blockchain is valid' : is_valid }
    
    return jsonify(response), 200
# Running the app
    
app.run(host = '0.0.0.0',port = 5000)





