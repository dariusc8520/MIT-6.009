def search(successors, start_state, goal_test, dfs=False):
    if goal_test(start_state):
        return (start_state,)

    agenda = [(start_state,)]
    visited = {start_state}

    while agenda:
        current_path = agenda.pop(-int(dfs))
        terminal_vertex = current_path[-1]

        for child in successors(terminal_vertex):
            if child in visited:
                continue
            new_path = current_path + (child,)
            if goal_test(child):
                return new_path
            visited.add(child)
            agenda.append(new_path)
