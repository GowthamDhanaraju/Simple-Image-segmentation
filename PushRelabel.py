from queue import Queue
import numpy as np
import sys

class PushRelabel:
    @staticmethod
    def preFlows(C, F, heights, eflows, s):
        heights[s] = len(heights)
        F[s, :] = C[s, :]
        for v in range(len(C)):
            if C[s, v] > 0:
                eflows[v] += C[s, v]
                C[v, s] = 0
                F[v, s] = -C[s, v]

    @staticmethod
    def overFlowVertex(vertices, s, t):
        for v in range(len(vertices)):
            if v != s and v != t and vertices[v, 1] > 0:
                return v
        return None

    @staticmethod
    def push(edges, vertices, u):
        for v in range(len(edges[u])):
            if edges[u, v, 1] != edges[u, v, 0]:
                if vertices[u, 0] > vertices[v, 0]:
                    flow = min(edges[u, v, 0] - edges[u, v, 1], vertices[u, 1])
                    vertices[u, 1] -= flow
                    vertices[v, 1] += flow
                    edges[u, v, 1] += flow
                    edges[v, u, 1] -= flow
                    return True
        return False

    @staticmethod
    def relabel(edges, vertices, u):
        mh = float("inf")
        for v in range(len(edges[u])):
            if edges[u, v, 1] != edges[u, v, 0] and vertices[v, 0] < mh:
                mh = vertices[v, 0]
        vertices[u, 0] = mh + 1

    @staticmethod
    def dfs(rGraph, V, s, visited):
        stack = [s]
        while stack:
            v = stack.pop()
            if not visited[v]:
                visited[v] = True
                stack.extend([u for u in range(V) if rGraph[v][u] > 0])

    @staticmethod
    def pushRelabel(C, s, t):
        print("Running push relabel algorithm")
        V = len(C)
        F = np.zeros((V, V))
        heights = np.zeros(V)
        excess = np.zeros(V)

        def preFlows():
            heights[s] = V
            F[s, :] = C[s, :]
            for v in range(V):
                if C[s, v] > 0:
                    excess[v] = C[s, v]
                    excess[s] -= C[s, v]
                    F[v, s] = -C[s, v]

        def overFlowVertex():
            for v in range(V):
                if v != s and v != t and excess[v] > 0:
                    return v
            return None

        def push(u):
            for v in range(V):
                if C[u, v] > F[u, v] and heights[u] == heights[v] + 1:
                    flow = min(C[u, v] - F[u, v], excess[u])
                    F[u, v] += flow
                    F[v, u] -= flow
                    excess[u] -= flow
                    excess[v] += flow
                    return True
            return False

        def relabel(u):
            mh = float("inf")
            for v in range(V):
                if C[u, v] > F[u, v] and heights[v] < mh:
                    mh = heights[v]
            heights[u] = mh + 1

        preFlows()

        while True:
            u = overFlowVertex()
            if u is None:
                break
            if not push(u):
                relabel(u)

        print("Max flow", excess[t])

        visited = np.zeros(V, dtype=bool)
        PushRelabel.dfs(C - F, V, s, visited)

        cuts = []
        for u in range(V):
            for v in range(V):
                if visited[u] and not visited[v] and C[u, v]:
                    cuts.append((u, v))
        return cuts
