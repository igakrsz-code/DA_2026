#1
import random

# Step 1
def get_words_from_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    return content.split()


# Step 2
def get_random_sentence(length):
    words = get_words_from_file("words.txt")
    chosen_words = []

    for _ in range(length):
        chosen_words.append(random.choice(words))

    sentence = " ".join(chosen_words).lower()
    return sentence


# Step 3
def main():
    print("This program generates a random sentence from a word list.")

    try:
        length = int(input("Enter sentence length (2–20): "))

        if length < 2 or length > 20:
            print("Error: length must be between 2 and 20.")
            return

    except ValueError:
        print("Error: please enter a valid integer.")
        return

    sentence = get_random_sentence(length)
    print("Generated sentence:")
    print(sentence)


main()

#2
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

# Step 1: Load JSON
data = json.loads(sampleJson)

# Step 2: Access salary
salary = data["company"]["employee"]["payable"]["salary"]
print("Salary:", salary)

# Step 3: Add birth_date
data["company"]["employee"]["birth_date"] = "1990-05-15"

# Step 4: Save to file
with open("employee.json", "w") as f:
    json.dump(data, f, indent=4)

print("Modified JSON saved to employee.json")
