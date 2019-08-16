''' 
Microservice that performs a variety of functions:
1) Squares every odd number in a vector of integers
2) Generate string:encoding key store from a list of strings
3) Decode an encoded string
'''
# Nameko import
from nameko.rpc import rpc

# Huffman encoder/decoder
from dahuffman import HuffmanCodec

### Use NLTK Gutenberg corpus to create a frequency distribution of letters
### Use that to perform static Huffman encoding
from nltk.corpus import gutenberg 

# Define the service
class InvictusService():
    name = "invictus_service"
    codec = HuffmanCodec.from_data(gutenberg.raw())

    # Function that squares a number if it's odd
    def odd_square(self, number):
        if (number % 2 != 0):
            return number * number
        return number

    # RPC to apply odd_square to a list of integers
    @rpc
    def apply_odd_square(self, array):
        return list(map(self.odd_square, array))

    # Function that takes a string and produces the huffman encoding
    def to_huffman(string):
        return {string: codec.encode(string)}

    # RPC to apply to_huffman to a list of strings
    @rpc 
    def apply_to_huffman(array):
        return list(map(self.to_huffman, array))

   # RPC to decode a given Huffman encoded string 
    @rpc
    def decode_huffman(code):
        return codec.decode(code)
