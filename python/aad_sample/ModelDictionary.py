class ModelDictionary(dict):

    # __init__ function
    def __init__(self):
        self = dict()

    # Function to add key:value
    def add(self, key, value):
        self[key] = value

    def get(self,key):
        return self[key]



# Main Function
#dict_obj = ModelDictionary()

# Taking input key = 1, value = Geek
#dict_obj.key = input("Enter the key: ")
#dict_obj.value = input("Enter the value: ")

#dict_obj.add(dict_obj.key, dict_obj.value)
#dict_obj.add(2, 'forGeeks')

#print(dict_obj)