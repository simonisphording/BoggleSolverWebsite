f = open("wordlist_raw.txt", "r")
lines = f.readlines()
f.close()

f = open("wordlist.txt", "w")
for line in lines:
    if not line[0].isupper():
        if len(line.strip()) > 2 and not any(not c.isalpha() for c in line.strip()):
            f.write(line)
f.close()
