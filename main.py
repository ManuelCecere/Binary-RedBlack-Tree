import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(10000)


class Node:
    def __init__(self, key=None):
        self.key = key
        self.left = None
        self.right = None
        self.p = None
        self.color = None


class ABR:
    def __init__(self):
        self.root = None
        self.height = 0

    def setRoot(self, key):
        self.root = Node(key)

    def search(self, value):
        x = self.root
        while x is not None and value != x.key:
            if x.key < value:
                x = x.right
            else:
                x = x.left
        return x

    def inorder(self):
        def _inorder(X):
            if X is None:
                return
            if X.left is not None:
                _inorder(X.left)
            # print(X.key)
            if X.right is not None:
                _inorder(X.right)

        _inorder(self.root)

    def treeMax(self):
        x = self.root
        if x is not None:
            while x.right is not None:
                x = x.right
        return x

    def insert(self, key):
        depth = 1
        if self.root is None:
            self.setRoot(key)
        else:
            x = self.root
            inserted = False
            while not inserted:
                if key <= x.key:
                    if x.left is not None:
                        x = x.left
                    else:
                        x.left = Node(key)
                        inserted = True
                else:
                    if x.right is not None:
                        x = x.right
                    else:
                        x.right = Node(key)
                        inserted = True
                depth = depth + 1
        if depth > self.height:
            self.height = depth


class ARN:
    def __init__(self):
        self.NIL = Node()
        self.NIL.color = "Black"
        self.root = self.NIL
        self.height = 0

    def setRoot(self, key):
        self.root = Node(key)
        self.root.color = "Black"

    def search(self, value):
        x = self.root
        while x is not self.NIL and value != x.key:
            if x.key < value:
                x = x.right
            else:
                x = x.left
        return x

    def inorder(self):
        def _inorder(X):
            if X is self.NIL:
                return
            if X.left is not self.NIL:
                _inorder(X.left)
            # print(X.key)
            if X.right is not self.NIL:
                _inorder(X.right)

        _inorder(self.root)

    def treeMax(self):
        x = self.root
        if x is not self.NIL:
            while x.right is not self.NIL:
                x = x.right
        return x

    def leftRotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.p = x
        y.p = x.p
        if x.p is None:
            self.root = y
        elif x is x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def rightRotate(self, x):
        y = x.left
        x.left = y.right
        if y.right is not self.NIL:
            y.right.p = x
        y.p = x.p
        if x.p is None:
            self.root = y
        elif x is x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.right = x
        x.p = y

    def insert(self, z):
        depth = 1
        z.left = self.NIL
        z.right = self.NIL
        if self.root is self.NIL:
            self.root = z
            self.root.color = "Black"
        else:
            x = self.root
            inserted = False
            while not inserted:
                if z.key <= x.key:
                    if x.left is not self.NIL:
                        x = x.left
                    else:
                        x.left = z
                        z.p = x
                        inserted = True
                else:
                    if x.right is not self.NIL:
                        x = x.right
                    else:
                        x.right = z
                        z.p = x
                        inserted = True
                depth = depth + 1
            z.color = "Red"
        if depth > self.height:
            self.height = depth
        if z.p is None or z.p.p is None:
            return
        self.insertFixup(z)

    def insertFixup(self, z):
        while z is not self.root and z.p.color is "Red":
            if z.p is z.p.p.left:
                y = z.p.p.right
                if y.color is "Red":
                    z.p.color = "Black"
                    y.color = "Black"
                    z.p.p.color = "Red"
                    z = z.p.p

                else:
                    if z is z.p.right:
                        z = z.p
                        self.leftRotate(z)
                    z.p.color = "Black"
                    z.p.p.color = "Red"
                    self.rightRotate(z.p.p)
                    self.height -= 1

            else:
                y = z.p.p.left

                if y.color is "Red":
                    z.p.color = "Black"
                    y.color = "Black"
                    z.p.p.color = "Red"
                    z = z.p.p

                else:
                    if z is z.p.left:
                        z = z.p
                        self.rightRotate(z)
                    z.p.color = "Black"
                    z.p.p.color = "Red"
                    self.leftRotate(z.p.p)
                    self.height -= 1
        self.root.color = "Black"


def testRandInsert():
    abrTotAvgRand = []
    arnTotAvgRand = []
    size = range(0, 10001, 500)
    nsamples = 80
    for s in size:
        abrAvgRand = 0
        arnAvgRand = 0
        for r in range(nsamples):
            A = np.random.randint(0, s, s)
            abr = ABR()
            arn = ARN()
            start = timer()
            for i in A:
                abr.insert(i)
            abrAvgRand += timer() - start

            start = timer()
            for i in A:
                arn.insert(Node(i))
            arnAvgRand += timer() - start
        abrAvgRand = abrAvgRand / nsamples
        arnAvgRand = arnAvgRand / nsamples
        abrTotAvgRand.append(abrAvgRand * 1000)
        arnTotAvgRand.append(arnAvgRand * 1000)
    plt.plot(size, abrTotAvgRand, label="ABR")
    plt.plot(size, arnTotAvgRand, label="ARN")
    plt.legend()
    plt.ylabel("Time in ms")
    plt.xlabel("Input's dimension ")
    plt.show()


def testOrdInsert():
    abrTotAvgOrd = []
    arnTotAvgOrd = []
    size = range(0, 5001, 500)
    nsamples = 10
    for s in size:
        abrAvgOrd = 0
        arnAvgOrd = 0
        for r in range(nsamples):
            A = np.array(range(s))
            abr = ABR()
            arn = ARN()
            start = timer()
            for i in A:
                abr.insert(i)
            abrAvgOrd += timer() - start

            start = timer()
            for i in A:
                arn.insert(Node(i))
            arnAvgOrd += timer() - start
        abrAvgOrd = abrAvgOrd / nsamples
        arnAvgOrd = arnAvgOrd / nsamples
        abrTotAvgOrd.append(abrAvgOrd * 1000)
        arnTotAvgOrd.append(arnAvgOrd * 1000)
    plt.plot(size, abrTotAvgOrd, label="ABR")
    plt.plot(size, arnTotAvgOrd, label="ARN")
    plt.legend()
    plt.ylabel("Time in ms")
    plt.xlabel("Input's dimension ")
    plt.show()


def testRandHeight():
    abrTotAvgRand = []
    arnTotAvgRand = []
    size = range(0, 10001, 200)
    nsamples = 10
    for s in size:
        abrAvgRand = 0
        arnAvgRand = 0
        for r in range(nsamples):
            A = np.random.randint(0, s, s)
            abr = ABR()
            arn = ARN()
            for i in A:
                abr.insert(i)
                arn.insert(Node(i))
            abrAvgRand += abr.height
            arnAvgRand += arn.height
        abrAvgRand = (abrAvgRand / nsamples)
        arnAvgRand = (arnAvgRand / nsamples)
        abrTotAvgRand.append(abrAvgRand)
        arnTotAvgRand.append(arnAvgRand)
    plt.plot(size, abrTotAvgRand, label="ABR")
    plt.plot(size, arnTotAvgRand, label="ARN")
    plt.legend()
    plt.ylabel("Height")
    plt.xlabel("Input's dimension ")
    plt.show()


def testOrdHeight():
    abrTotAvgOrd = []
    arnTotAvgOrd = []

    size = range(0, 10001, 200)
    nsamples = 1
    for s in size:
        abrAvgOrd = 0
        arnAvgOrd = 0
        for r in range(nsamples):
            A = np.array(range(s))
            abr = ABR()
            arn = ARN()
            for i in A:
                abr.insert(i)
                arn.insert(Node(i))
            abrAvgOrd += abr.height
            arnAvgOrd += arn.height
        abrAvgOrd = (abrAvgOrd / nsamples)
        arnAvgOrd = (arnAvgOrd / nsamples)
        abrTotAvgOrd.append(abrAvgOrd)
        arnTotAvgOrd.append(arnAvgOrd)
    plt.plot(size, abrTotAvgOrd, label="ABR")
    plt.plot(size, arnTotAvgOrd, label="ARN")
    plt.legend()
    plt.ylabel("Height")
    plt.xlabel("Input's dimension ")
    plt.show()


def testRandWalk():
    abrTotAvgRand = []
    arnTotAvgRand = []
    size = range(0, 5001, 500)
    nsamples = 200
    for s in size:
        abrAvgRand = 0
        arnAvgRand = 0
        for r in range(nsamples):
            A = np.random.randint(0, s, s)
            abr = ABR()
            arn = ARN()
            for i in A:
                arn.insert(Node(i))
                abr.insert(i)

            start = timer()
            abr.inorder()
            abrAvgRand += timer() - start
            start = timer()
            arn.inorder()
            arnAvgRand += timer() - start
        abrAvgRand = abrAvgRand / nsamples
        arnAvgRand = arnAvgRand / nsamples
        abrTotAvgRand.append(abrAvgRand * 1000)
        arnTotAvgRand.append(arnAvgRand * 1000)
    plt.plot(size, abrTotAvgRand, label="ABR")
    plt.plot(size, arnTotAvgRand, label="ARN")
    plt.legend()
    plt.ylabel("Time in ms")
    plt.xlabel("Input's dimension ")
    plt.show()


def testOrdWalk():
    abrTotAvgOrd = []
    arnTotAvgOrd = []
    size = range(0, 2001, 50)
    nsamples = 200
    for s in size:
        abrAvgOrd = 0
        arnAvgOrd = 0
        A = np.array(range(s))
        abr = ABR()
        arn = ARN()
        for i in A:
            arn.insert(Node(i))
            abr.insert(i)
        for r in range(nsamples):
            start = timer()
            abr.inorder()
            abrAvgOrd += timer() - start
            start = timer()
            arn.inorder()
            arnAvgOrd += timer() - start
        abrAvgOrd = abrAvgOrd / nsamples
        arnAvgOrd = arnAvgOrd / nsamples
        abrTotAvgOrd.append(abrAvgOrd * 1000)
        arnTotAvgOrd.append(arnAvgOrd * 1000)

    plt.plot(size, abrTotAvgOrd, label="ABR")
    plt.plot(size, arnTotAvgOrd, label="ARN")
    plt.legend()
    plt.ylabel("Time in ms")
    plt.xlabel("Input's dimension ")
    plt.show()


def testOrdSearch():
    abrTotAvgOrd = []
    arnTotAvgOrd = []
    size = range(1, 2001, 200)
    nsamples = 100
    for s in size:
        abrAvgOrd = 0
        arnAvgOrd = 0
        for r in range(nsamples):
            A = np.array(range(s))
            abr = ABR()
            arn = ARN()
            for i in A:
                abr.insert(i)
                arn.insert(Node(i))
            values = np.random.randint(0, s, 10)
            start = timer()
            for value in values:
                abr.search(value)
            abrAvgOrd += timer() - start
            start = timer()
            for value in values:
                arn.search(value)
            arnAvgOrd += timer() - start
        abrAvgOrd = abrAvgOrd / nsamples
        arnAvgOrd = arnAvgOrd / nsamples
        abrTotAvgOrd.append(abrAvgOrd * 1000)
        arnTotAvgOrd.append(arnAvgOrd * 1000)
    plt.plot(size, abrTotAvgOrd, label="ABR")
    plt.plot(size, arnTotAvgOrd, label="ARN")
    plt.legend()
    plt.ylabel("Time in ms")
    plt.xlabel("Input's dimension ")
    plt.show()


def main():
    testRandInsert()
    testOrdInsert()
    testRandHeight()
    testOrdHeight()
    testRandWalk()
    testOrdWalk()
    testOrdSearch()

if __name__ == '__main__':
    main()