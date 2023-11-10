

import requests
from geopy.distance import geodesic
from sklearn.cluster import KMeans


def calculate_distance(user1, user2):
    coords_user1 = (user1['address']['geo']['latitude'], user1['address']['geo']['longitude'])
    coords_user2 = (user2['address']['geo']['latitude'], user2['address']['geo']['longitude'])
    return geodesic(coords_user1, coords_user2).kilometers


def group_users_kmeans(users):
    coords = [(user['address']['geo']['latitude'], user['address']['geo']['longitude']) for user in users]
    kmeans = KMeans(n_clusters=8)  # You can adjust the number of clusters as needed
    kmeans.fit(coords)
    cluster_labels = kmeans.labels_
    groups = [[] for _ in range(max(cluster_labels) + 1)]

    for i, user in enumerate(users):
        group_index = cluster_labels[i]
        groups[group_index].append(user)

    return groups


def display_grouped_users(groups):
    total_groups = len(groups)
    for i, group in enumerate(groups, 1):
        print(f"Group {i}:")
        for user in group:
            print(user['fullName'])
        print(f"Total {len(group)} People in this group")
    print(f"Total Number of Groups: {total_groups}")
    group_with_highest_members = max(groups, key=len)
    group_with_lowest_members = min(groups, key=len)
    print(f"Group {groups.index(group_with_highest_members) + 1} has the highest number of members")
    print(f"Group {groups.index(group_with_lowest_members) + 1} has the lowest number of members")


if __name__ == "__main__":

    json_url = "https://ignite.zook.top/data.json"
    response = requests.get(json_url)
    if response.status_code == 200:
        data = response.json()
        grouped_users = group_users_kmeans(data)
        display_grouped_users(grouped_users)
    else:
        print("Failed to fetch data from the provided JSON URL.")

