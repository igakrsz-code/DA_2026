
### 🌟 Exercise 2: Working with JSON (~15 minutes)

# Given this JSON string:


# sampleJson = """{
#    "company":{
#       "employee":{
#          "name":"emma",
#          "payable":{
#             "salary":7000,
#             "bonus":800
#          }
#       }
#    }
# }"""


# **Steps:**
# 1. Parse the JSON string using `json.loads()`
# 2. Access and print the employee's `salary`
# 3. Add a `"birth_date"` key to the employee with value `"1990-05-15"`
# 4. Save the modified data to a file called `employee.json` using `json.dump()` with `indent=2`
# 5. Read the file back and print it to verify

# **Expected output:**
# ```
# Salary: 7000
# Modified data saved to employee.json
# Verified — birth_date: 1990-05-15

import json

sampleJson = """{
   "company":{
      "employee":{
         "name":"emma",
         "payable":{
            "salary":7000,
            "bonus":800
         }
      }
   }
}"""


data = json.loads(sampleJson)
print(f"Full dict: {data}")


salary = data["company"]["employee"]["payable"]["salary"]
print(f"Salary: {salary}")


data["company"]["employee"]["birth_date"] = "1990-05-15"
print(f"Full modified dict: {data}")


with open("employee.json", "w") as f:
    json.dump(data, f, indent=2)
print("Modified data saved to employee.json")


with open("employee.json", "r") as f:
    verified = json.load(f)

print(f"Loaded file dictionary: {verified}")

