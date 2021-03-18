#!/usr/bin/env python3
import quiz
import os, collections, types
from copy import deepcopy

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


##################################################
##  Problem 1
##################################################

def test_problem1_01():
    S = [1, 2]; W = [0.8, 0.7]
    expect = [1.5, 2.3]
    result = quiz.trailing_weighted_average(deepcopy(S), deepcopy(W))
    assert expect == result

def test_problem1_02():
    S = [1, 5, 6, 7]; W = [1]
    expect = [1, 5, 6, 7]
    result = quiz.trailing_weighted_average(deepcopy(S), deepcopy(W))
    assert expect == result

def test_problem1_03():
    S = [1, 5, 6, 7]; W = [0.5, 0.5]
    expect = [1.0, 3.0, 5.5, 6.5]
    result = quiz.trailing_weighted_average(deepcopy(S), deepcopy(W))
    assert expect == result

def test_problem1_04():
    S = [1, 5, 6, 7]; W = [0, 1]
    expect = [1, 1, 5, 6]
    result = quiz.trailing_weighted_average(deepcopy(S), deepcopy(W))
    assert expect == result

def test_problem1_05():
    S = [1, 5, 6, 7]; W = [1, 0]
    expect = [1, 5, 6, 7]
    result = quiz.trailing_weighted_average(S, W)
    assert expect == result
    result = quiz.trailing_weighted_average(S, W)
    assert expect == result, "okay on first call, but not second!"

def test_problem1_06():
    S = [1, 5, 6, 7]; W = [2, 0, 0, 0, 100]
    expect = [102, 110, 112, 114]
    result = quiz.trailing_weighted_average(deepcopy(S), deepcopy(W))
    assert expect == result

def test_problem1_07():
    S = list(range(1,18)); W = list(range(10,0,-1))
    expect = [55, 65, 84, 111, 145, 185, 230, 279, 331, 385, 440, 495, 550, 605, 660, 715, 770]
    result = quiz.trailing_weighted_average(deepcopy(S), deepcopy(W))
    assert expect == result


##################################################
##  Problem 2
##################################################

def test_problem2_01():
    s = set(range(5))
    n = 1
    expect = {(0,), (1,), (2,), (3,), (4,)}
    result = quiz.all_consecutives(s, n)
    assert expect == result

def test_problem2_02():
    s = set(range(5))
    n = 2
    expect = {(0, 1), (3, 4), (2, 3), (1, 2)}
    result = quiz.all_consecutives(s, n)
    assert expect == result

def test_problem2_03():
    s = set(range(5))
    n = 5
    expect = {(0, 1, 2, 3, 4)}
    result = quiz.all_consecutives(s, n)
    assert expect == result

def test_problem2_04():
    s = set(range(5))
    n = 6
    expect = set()
    result = quiz.all_consecutives(s, n)
    assert expect == result

def test_problem2_05():
    s = set(range(0, 5, 2))
    n = 1
    expect = {(2,), (0,), (4,)}
    result = quiz.all_consecutives(s, n)
    assert expect == result

    s = set(range(0, 5, 2))
    n = 2
    expect = set()
    result = quiz.all_consecutives(s, n)
    assert expect == result

def test_problem2_06():
    s = {0, 83, 2, 3, 81, 7, 82}
    n = 2
    expect = {(81, 82), (2, 3), (82, 83)}
    result = quiz.all_consecutives(s, n)
    assert expect == result

def test_problem2_07():
    # big set
    s1 = list(range(50)); r1 = {(a,b,c) for a,b,c in zip(s1,s1[1:],s1[2:])}
    s2 = list(range(200,300,2)); r2 = set()
    s3 = list(range(100,150)); r3 = {(a,b,c) for a,b,c in zip(s3,s3[1:],s3[2:])}
    s = set(s1) | set(s2) | set(s3)
    n = 3
    expect = r1 | r2 | r3
    result = quiz.all_consecutives(s, n)
    assert expect == result

def test_problem2_08():
    s = set(range(10))
    n = 11
    expect = set()
    result = quiz.all_consecutives(s, n)
    assert expect == result


##################################################
##  Problem 3
##################################################

# Tiny cases
def test_problem3_01():
    seq1, seq2 = '', ''
    expect = 0
    result = quiz.cost_to_consume(seq1, seq2)
    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"

def test_problem3_02():
    seq1, seq2 = 'a', ''
    expect = 1
    result = quiz.cost_to_consume(seq1, seq2)
    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"

    seq1, seq2 = '', 'a'
    expect = 1
    result = quiz.cost_to_consume(seq1, seq2)
    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"

def test_problem3_03():
    seq1, seq2 = 'a', 'b'
    expect = 1
    result = quiz.cost_to_consume(seq1, seq2)
    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"

def test_problem3_04():
    seq1, seq2 = 'ab', 'b'
    expect = 1
    result = quiz.cost_to_consume(seq1, seq2)
    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"

    seq1, seq2 = 'b', 'ab'
    expect = 1
    result = quiz.cost_to_consume(seq1, seq2)
    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"

def test_problem3_05():
    seq1, seq2 = 'aa', 'bb'
    expect = 2
    result = quiz.cost_to_consume(seq1, seq2)
    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"

# Small cases
subcases1 = [('mast', 'mast', 0),
            ('mast', 'must', 1),
            ('misty', 'must', 2),
            ('color', 'colour', 1),
            ('aba', 'bbb', 2),
            ('aba', 'bab', 2)]

@pytest.mark.parametrize('subcase', subcases1)
def test_problem3_06(subcase):
    seq1, seq2, expect = subcase
    result = quiz.cost_to_consume(seq1, seq2)
    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"

# Medium cases
subcases2 = [('car', 'boat', 3),
            ('a', 'bbbbbb', 6),
            ('frog', 'apple', 5)]
@pytest.mark.parametrize('subcase', subcases2)
def test_problem3_07(subcase):
    # Harder cases
    seq1, seq2, expect = subcase
    result = quiz.cost_to_consume(seq1, seq2)
    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"

# Long case
def test_problem3_08():
    size = 8
    seq1, seq2, expect = ('a'*size, 'b'*size, size)
    result = quiz.cost_to_consume(seq1, seq2)
    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"


# Long and/or difficult test cases not actually run on the quiz
#def test_problem3_09():
#    size = 9
#    seq1, seq2, expect = ('a'*size, 'b'*size, size)
#    result = quiz.cost_to_consume(seq1, seq2)
#    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"
#
#
#subcases3 = [
#    ('supercalafragilistic', 'sypercalafragilistic', 1),
#    ('supercalifragilisticexpialidocious', 'sypercalifragilisticexpialidocious', 1),
#    ('supercalifragilisticexpialidocious', 'supercalifragilisticexpialidoxious', 1),
#]
#@pytest.mark.parametrize('subcase', subcases3)
#def test_problem3_10(subcase):
#    #
#    # Try this one if you want a challenge!
#    #
#    seq, seq2, expect = subcase
#    result = quiz.cost_to_consume(seq1, seq2)
#    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"
#
#
#def test_problem3_11():
#    #
#    # Try this one if you want an even bigger challenge!
#    #
#    size = 20
#    seq1, seq2, expect = ('a'*size, 'b'*size, size)
#    result = quiz.cost_to_consume(seq1, seq2)
#    assert expect == result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")"


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
        args = ['-v', __file__] if len(sys.argv) == 1 else ['-v', *('%s::%s' % (__file__, i) for i in sys.argv[1:])]
        kwargs = {}
    res = pytest.main(args, **kwargs)
