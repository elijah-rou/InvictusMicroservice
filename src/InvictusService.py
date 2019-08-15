''' 
Microservice that performs a variety of functions:
1) Squares every odd number in a vector of integers
2) Generate string:encoding key store from a list of strings
3) Decode an encoded string
'''
# Nameko import
from nameko.rpc import rpc, RpcProxy

# Define the service
class InvictusService():
    name = "invictus_service"

    # Function that squares a number if it's odd
    def odd_square(self, number):
        if (number % 2 != 0):
            return number * number
        return number

    # RPC to apply odd_square to a list of integers
    @rpc
    def apply_odd_square(self, array):
        return list(map(odd_square, array))
