def find_happiest(filename):
    scores = {}
    results = {}
    file = open(filename, 'r')
    for line in file:
        line = line.strip('\n')
        line = line.split(',')
        continent = line[3]
        country = line[1]
        score = line[2]
        if continent not in results:
            results[continent] = country
            scores[continent] = score
        elif continent in results and score > scores[continent]:
            results[continent] = country
            scores[continent] = score
    file.close()
    return results
