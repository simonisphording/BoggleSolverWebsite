########  imports  ##########
from flask import Flask, jsonify, request, render_template
import pickle as pkl
import numpy as np
app = Flask(__name__)

#############################
# Additional code goes here #
#############################

infile = open(r'wordlist_trie.pkl', 'rb')
trie = pkl.load(infile)
infile.close()

class GameField:

    def __init__(self, d):

        self.board = np.array([["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""]],
                            dtype='U100')

        i = 0
        for x in range(4):
            for y in range(4):
                letter = d[i]
                self.board[x, y] = letter
                i += 1


def is_word(s):
    if len(s) >= 3:
        return s in trie.values(s)
    else:
        return False


def is_prefix(s):
    if not trie.values(s):
        return False
    else:
        return True


def adjacent_coords(x, y):
    result = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            x2 = x + dx
            y2 = y + dy
            if -1 < x2 < 4 and -1 < y2 < 4:
                if x2 != x or y2 != y:
                    result.append([x2, y2])
    return result

def search_from_dice(board, all_words, s, x, y, visited_coords, debug=False):
    temp = visited_coords.copy()
    temp.append([x, y])

    if debug:
        print(temp, s)

    if is_word(s):
        all_words.add(s)

    for coord in adjacent_coords(x, y):
        if coord not in temp:
            x2, y2 = coord
            a = board[x2, y2]
            if is_prefix(s + a):
                search_from_dice(board, all_words, s + a, x2, y2, temp)

def all_important_stuff(input):

    all_words = set()

    g = GameField(input)

    for x in range(4):
        for y in range(4):
            search_from_dice(g.board, all_words, g.board[x, y], x, y, [])

    result = ""
    for item in list(all_words):
        result += item + "/"

    return result

######## Data fetch ############
@app.route('/getdata/<diceString>', methods=['GET', 'POST'])
def data_get(diceString):
    if request.method == 'POST':  # POST request
        print(request.get_text())  # parse as text
        return 'OK', 200

    else:  # GET request
        result = all_important_stuff(diceString)
        return result

@app.route('/')
def home_page():
    example_embed = 'This string is from python'
    return render_template('index.html', embed=example_embed)

##########  run app  ########
if __name__ == "__main__":
    app.run(debug = True)
