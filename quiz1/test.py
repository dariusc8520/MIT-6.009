#!/usr/bin/env python3
import os
import copy
import lzma
import math
import quiz
import types
import pickle
import hashlib

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)

##################################################
#  Problem 1
##################################################

def _run_foo_test(n):
    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'foo_%02d_in.pickle' % n), 'rb') as f:
        inp = pickle.load(f)

    result = quiz.foo(inp)

    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'foo_%02d_out.pickle' % n), 'rb') as f:
        expected = pickle.load(f)

    assert result == expected


def test_problem1_01():
    for testnum in range(6):
        _run_foo_test(testnum)

def test_problem1_02():
    for testnum in range(6, 34):
        _run_foo_test(testnum)



##################################################
#  Problem 2
##################################################


def _run_islands_test(n):
    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'islands_%02d_in.pickle' % n), 'rb') as f:
        inputs = pickle.load(f)

    results = [quiz.get_islands(inp) for inp in inputs]

    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'islands_%02d_out.pickle' % n), 'rb') as f:
        expected = pickle.load(f)

    for inp, res, exp in zip(inputs, results, expected):
        assert isinstance(res, list), "Your function should return a list"
        assert all(isinstance(i, set) for i in res), "Each island should be represented by a Python set"
        assert len(res) == len(exp)
        r = {frozenset(i) for i in res}
        e = {frozenset(i) for i in exp}
        assert r == e, "For input %r, expected %r, but got %r" % (inp, exp, res)


def test_problem2_examples():
    assert quiz.get_islands({'A': []}) == [{'A'}]

    x = quiz.get_islands({'A': [], 'B': ['B']})
    assert len(x) == 2
    assert {'B'} in x and {'A'} in x

    assert quiz.get_islands({'A': [], 'B': ['A']}) == [{'A', 'B'}]

    g1 = {'A': ['B', 'C'], 'B': [], 'C': [], 'D': []}
    r1 = quiz.get_islands(g1)
    assert len(r1) == 2
    assert {'A', 'B', 'C'} in r1 and {'D'} in r1

    g2 = {'A': ['B'], 'C': ['A'], 'B': ['C'], 'D': ['E'],
          'E': [], 'F': ['F'], 'G': [],}
    r2 = quiz.get_islands(g2)
    assert len(r2) == 4
    assert all(i in r2 for i in ({'A', 'B', 'C'}, {'D', 'E'}, {'F'}, {'G'}))



@pytest.mark.parametrize('testnum', list(range(5)))
def test_problem2_large(testnum):
    _run_islands_test(testnum)


##################################################
#  Problem 3
##################################################


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


def cats_and_dogs(cats, dogs):
    result = search(*quiz.setup_cats_and_dogs(cats, dogs))
    return quiz.interpret_result(result)


def _run_cats_test(n):
    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'cats_%02d_in.pickle' % n), 'rb') as f:
        inputs = pickle.load(f)

    results = [cats_and_dogs(*inp) for inp in inputs]

    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'cats_%02d_out.pickle' % n), 'rb') as f:
        expected = pickle.load(f)

    for inp, res, exp in zip(inputs, results, expected):
        if exp is None:
            assert res is None, "For input %r, expected no path but got %r" % (inp, res)
        else:
            assert res is not None, "For input %r, expected a path but got %r" % (inp, res)
            assert len(res) == exp, "For input %r, expected path of length %r but got %r" % (inp, exp, len(res))
            path_ok, msg = _check_valid_path(inp, res)
            assert path_ok, msg


@pytest.mark.parametrize('testnum', list(range(10)))
def test_problem3_large(testnum):
    _run_cats_test(testnum)


################################################
# Extra Code for Problem 3 Test Cases
################################################

with open(os.path.join(TEST_DIRECTORY, 'valid_path_checker.py.lzma'), 'rb') as f:
    exec(lzma.decompress(f.read()).decode('utf-8'))

################################################
# Standard pytest Boilerplate
################################################


if __name__ == '__main__':
    import sys
    import json

    class TestData:
        def __init__(self):
            self.results = {'passed': []}

        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtestloop(self, session):
            yield

        def pytest_runtest_logreport(self, report):
            if report.when != 'call':
                return
            self.results.setdefault(report.outcome, []).append(report.head_line)

        def pytest_collection_finish(self, session):
            self.results['total'] = [i.name for i in session.items]

        def pytest_unconfigure(self, config):
            print(json.dumps(self.results))

    if os.environ.get('CATSOOP'):
        args = ['--color=yes', '-v', __file__]
        if len(sys.argv) > 1:
            args = ['-k', sys.argv[1], *args]
        kwargs = {'plugins': [TestData()]}
    else:
        args = ['-v', __file__]
        if len(sys.argv) > 1:
            args = ['-k', sys.argv[1], *args]
        kwargs = {}
    res = pytest.main(args, **kwargs)
