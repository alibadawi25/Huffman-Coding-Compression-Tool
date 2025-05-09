import heapq


# inputString = input("Enter a string:")

def huffmanCoding(inputString):
    charFreq = {}
    heap = []

    for i in inputString:
        charFreq[i] = charFreq.get(i, 0) + 1

    for char, freq in charFreq.items():
        heap.append([freq, [char, ""]])

    heapq.heapify(heap)

    while len(heap) > 1:
        tree = ""
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        newNodeFreq = lo[0] + hi[0]
        tree = (f"{newNodeFreq}\n|\n|_ {lo[0]}{lo[1:]}\n|\n|_ {hi[0]}{hi[1:]}\n\n")
        print(tree)
        heapq.heappush(heap, [newNodeFreq] + lo[1:] + hi[1:])
        print("------------------------------------------------------------")

    huffmanCode = {}

    for i in heap[0][1:]:
        huffmanCode[i[0]] = i[1]

    return huffmanCode