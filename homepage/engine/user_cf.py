import math
from operator import itemgetter


def user_similarity(train):
    # build inverse table for item_users
    item_users = dict()
    for u, items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)
    # calculate co-rated items between users
    co_table = dict()
    num_list = dict()
    for i, users in item_users.items():
        for u in users:
            if not num_list.get(u):
                num_list[u] = 0
            num_list[u] += 1
            for v in users:
                if u == v:
                    continue
                if not co_table.get(u):
                    co_table[u] = {}
                if not co_table[u].get(v):
                    co_table[u][v] = 0
                co_table[u][v] += 1
    # calculate finial similarity matrix sim_table
    sim_table = dict()
    for u, related_users in co_table.items():
        for v, cuv in related_users.items():
            if not sim_table.get(u):
                sim_table[u] = {}
            if not sim_table[u].get(v):
                sim_table[u][v] = 0.0
            sim_table[u][v] = cuv / math.sqrt(num_list[u] * num_list[v])
    return sim_table


def Recommend(user_id, train, sim_table, K):
    rank = dict()
    interacted_items = train[user_id]
    for v, wuv in sorted(sim_table[user_id].items(), key=itemgetter(1), reverse=True)[0:K]:
        for i, rvi in train[v].items():
            if i in interacted_items:
                # we should filter items user interacted before
                continue
            if not rank.get(i):
                rank[i] = 0.0
            rank[i] += wuv * rvi
    return rank
