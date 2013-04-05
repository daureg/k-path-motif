#! /usr/bin/python
# vim: set fileencoding=utf-8


if __name__ == '__main__':
    with open('answer') as f:
        answer = [line.strip() for line in f.readlines()]
    with open('timing') as f:
        timing = [int(line.strip()) for line in f.readlines()]
    with open('gold') as f:
        gold = f.readline().strip()

    buff = ""
    mean = 0
    num_correct = 0.0
    for a, t in zip(answer, timing):
        correct = 1 if a == gold else 0
        buff += "{}\t{}\n".format(t, correct)
        mean += t
        num_correct += correct

    mean /= len(timing)
    num_correct /= len(answer)
    buff += "#{}\n#{:.2f}\n".format(num_correct, mean)
    with open('run.dat', 'w') as f:
        f.write(buff)
