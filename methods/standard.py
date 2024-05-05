def combinations(k, n, start_idx):
    def backtrack(start, combination):
        if len(combination) == k:
            combinations_list.append(combination[:])
            return
        for i in range(start, n + 1):
            combination.append(i + start_idx)
            backtrack(i + 1, combination)
            combination.pop()

    combinations_list = []
    backtrack(1, [])
    return combinations_list
