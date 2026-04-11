# dictionaries

#Access the value of key history

sample_dict = { 
   "class":{ 
      "student":{ 
         "name":"Mike",
         "marks":{ 
            "physics":70,
            "history":80
         }
      }
   }
}
print(sample_dict["class"]["student"]["marks"]["history"])
# output: 80

#Delete set of keys from Python Dictionary


sample_dict = {
  "name": "Kelly",
  "age":25,
  "salary": 8000,
  "city": "New york"

}
keys_to_remove = ["name", "salary"]
# {'city': 'New york', 'age': 25}
for key in keys_to_remove:
    sample_dict.pop(key)
print(sample_dict)



