def find_happiest(filename):
    results = {}
    file = open(filename, 'r')
    for line in file:
        line = line.strip('\n')
        line = line.split(',')
        continent = line[3]
        country = line[1]
        score = line[2]
        if continent not in results:
            results[continent] = [country, score]
        elif continent in results and score > results[continent][1]:
            results[continent] = [country, score]
    file.close()
    return results


print(find_happiest("C:/Users/siobh/Desktop/Coding Practice/PCL-Stutt/happiness.txt"))

        
