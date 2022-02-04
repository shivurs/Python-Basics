import opposites
import datetime

def read_words(filename):
    result = [ ]
    for line in open(filename, "r"):
        result.append(line.strip())
    return result

def find_longest(pairs):
    max_len = 0
    max_pair = "", ""
    for (w1, w2) in opp:
        if len(w1) > max_len:
            max_len = len(w1)
            max_pair = w1, w2

    return max_pair

   
if __name__ == "__main__":
    words = read_words("words.txt")
    print("Read", len(words), "words")
    
    # running the function
    start_time = datetime.datetime.now()
    opp = opposites.find_opposites(words)
    end_time = datetime.datetime.now()
    total_time = (end_time - start_time).total_seconds()
    
    print("All found:", len(opp), "(correct: 857)")
    print("It took", str(total_time) + "s", "(correct: less than 10s)")

    # additional test to see if everything is fine
    longest = find_longest(opp)
    print("Longest pair is:", longest, "(correct: 'stressed', 'desserts')")
