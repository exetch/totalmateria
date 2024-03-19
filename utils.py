import json

import requests


cookies = {
    '_ga': 'GA1.1.1830800357.1710769040',
    '_hjSession_939928': 'eyJpZCI6ImM5OGQwMDhhLTM1NTctNDI0Mi04MWNkLTNjYzNiZGYxZjEyMiIsImMiOjE3MTA3NjkwNDI5OTgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
    '_hjSessionUser_939928': 'eyJpZCI6IjFjMGRhNDVmLWI3ZTAtNWY2Ni05Y2QwLWM4NmVlODJmZTRlNiIsImNyZWF0ZWQiOjE3MTA3NjkwNDI5OTYsImV4aXN0aW5nIjp0cnVlfQ==',
    'idsrv.session': 'F06C1D75D793AFCDFB9C286BA25A8A75',
    'totalmateria.session': 'CfDJ8DXxndW5yTRJm_OXW-4I-xIGzl6hcJrS7v3_IJri4NyUxJPE6Ihlz5tv-huSpdpFMOnsMPoEAHV3JQmPpD4dx_jqKY8JMGRXoPrBdFtmFXb1r8g5SssGaL6IE1W98RdwANH6hehU0b9YceUYISgicmtQx5uoFk0XLvoP_9elXGeQJdQx5U5pGW7hvETa7yxkl3OFJ9-NEEo34Ry52o3Z0iJjTsciJozb8w9UXwunDS_GizJRPWt3Ca7bHxGR7JNTnexg7e9nnmYsPM54wl1uwpaVch81MIY5MQ2Oi9NT5y3Po5fwyVtEf79U8B3_y1uTlUAtj7fOYHlDYZ_v6GOVF91WaBaUZtIjaZdwoj1wNqOKoSmqR3ulbEDRcUpCDMAl8G5lpoEmZZLiT0Ij5FfY9nS7xyk7IzK9Xz13Un8Zu4At5vw0j8As-zV8jvb5K9Jr1Lsih1JTx9sn9xW-NXUPtw_9oLoPqd9AWg9RLkf4bI29z9IREYBA5CUQS7zLFYad1dzrospx8H4uhOTMLaEtdPqvTXpDFkDljgaI4NggYcdH2KcO4ciGtEjTQtm9dEfBw8xIG9LHN-UC3mq3t73Wu8jSZWIzB7ddyT5-ESXID5uSRq74Ch3dwWUwzHhOJZ_x0PLO9rglOF9_NbuZTyX7Mona9EnSRdHh3jIJxAM4bXBZErLYUb9hN2G6k-HboWtYCyHopzaX65AeqA0GRHsh47o',
    '_ga_CTW8QM09XY': 'GS1.1.1710769039.1.1.1710769260.8.0.0',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjVDNkExQzcwOUNBQzE2M0FENDk3OTQ3Qjg1QjQ5ODkxQ0MzRDg0QkFSUzI1NiIsInR5cCI6IkpXVCIsIng1dCI6IlhHb2NjSnlzRmpyVWw1UjdoYlNZa2N3OWhMbyJ9.eyJuYmYiOjE3MTA3NjkyNTQsImV4cCI6MTcxMDgwNTI1NCwiaXNzIjoiaHR0cHM6Ly9wb3J0YWwudG90YWxtYXRlcmlhLmNvbS9pZGVudGl0eSIsImF1ZCI6InNwYSIsIm5vbmNlIjoiYm5wRGRtNVNNMFo1VEc5UFJGQmlSMnBmYTNKaVR5MWxSbFZUYVROLVFWaHBSWEpxYTFCdmIwZHFVVEp4IiwiaWF0IjoxNzEwNzY5MjU0LCJhdF9oYXNoIjoiRWl2MWZCdFdqakxaUjlLTnBqcGFfQSIsInNfaGFzaCI6IjIxTlYwSkxVaXF3bG5xdVMxNDc4UHciLCJzaWQiOiJGMDZDMUQ3NUQ3OTNBRkNERkI5QzI4NkJBMjVBOEE3NSIsInN1YiI6IjE3ODE3NjgyMTU3MzIwMjQxODQwMTQ0MkdZVkw1NklSUUlROFBGNFVfMTAwIiwiYXV0aF90aW1lIjoxNzEwNzY5MjQzLCJpZHAiOiJsb2NhbCIsIkZ1bGxOYW1lIjoiR2VnaWsgUGVwZWwiLCJVc2VyVHlwZSI6IjEwMCIsIkhhc0NvcnBvcmF0ZVVzZXJJZCI6IkZhbHNlIiwiSXNTaW5nbGVVc2VyIjoiRmFsc2UiLCJFbWFpbCI6ImFseXNzb241NXRvd25laGpkQGhvdG1haWwuY29tIiwiU3Vic2NyaXB0aW9uRGF0ZSI6IjA1LzE3LzIwMjQiLCJDb3JlIjoiUnwwfDAiLCJTbWFydCBDb21wIjoiUnwwfDAiLCJFeHRlbmRlZCBSYW5nZSI6IlJ8MHwwIiwiU3VwcGxpZXJzIjoiUnwwfDAiLCJQb2x5bWVyc1BMVVMiOiJSfDB8MCIsImVYcG9ydGVyIjoiUnwwfDUiLCJUcmFja2VyIjoiUnwwfDAiLCJEYXRhUExVUyI6IlJ8MHwwIiwiRW52aXJvIjoiUnwwfDAiLCJDb21wbGlhbmNlIjoiUnwwfDAiLCJNYXRlcmlhbENvbnNvbGUiOiJSfDB8MCIsImFtciI6WyJwd2QiXX0.HsFrs4_TkPQ5yH0vvQ46ikgR4Bk2zScN3jI-pwx3u6lkmlupOXQb5dO50fElh-L3oy8UYMRA4HqK8AiFyEJEfvPkCyBddsXVcdwdyqyU5U8lx_nMbio3AS-6DHBgvrEo49tEJ-ZM9Dfji4-I-AmBxWSvBoBQLi2fDCOk56cq_t_x-baH7fewE0Ol836-G0oGpC2UnmUSILWTotwmy1kOLwaunMDVrGw81W3Isom6C6tQsMwJJQ4_lx4tQvk3CmKPB73zt1ds3XaN1FKHj_oTfCoaCWD1e6GTdY36L5RamN2UFcFL6z3fTzvJ0prl23J1GbaYT1ihULjHZ46uUb9E5g',
    'Connection': 'keep-alive',
    # 'Cookie': '_ga=GA1.1.1830800357.1710769040; _hjSession_939928=eyJpZCI6ImM5OGQwMDhhLTM1NTctNDI0Mi04MWNkLTNjYzNiZGYxZjEyMiIsImMiOjE3MTA3NjkwNDI5OTgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _hjSessionUser_939928=eyJpZCI6IjFjMGRhNDVmLWI3ZTAtNWY2Ni05Y2QwLWM4NmVlODJmZTRlNiIsImNyZWF0ZWQiOjE3MTA3NjkwNDI5OTYsImV4aXN0aW5nIjp0cnVlfQ==; idsrv.session=F06C1D75D793AFCDFB9C286BA25A8A75; totalmateria.session=CfDJ8DXxndW5yTRJm_OXW-4I-xIGzl6hcJrS7v3_IJri4NyUxJPE6Ihlz5tv-huSpdpFMOnsMPoEAHV3JQmPpD4dx_jqKY8JMGRXoPrBdFtmFXb1r8g5SssGaL6IE1W98RdwANH6hehU0b9YceUYISgicmtQx5uoFk0XLvoP_9elXGeQJdQx5U5pGW7hvETa7yxkl3OFJ9-NEEo34Ry52o3Z0iJjTsciJozb8w9UXwunDS_GizJRPWt3Ca7bHxGR7JNTnexg7e9nnmYsPM54wl1uwpaVch81MIY5MQ2Oi9NT5y3Po5fwyVtEf79U8B3_y1uTlUAtj7fOYHlDYZ_v6GOVF91WaBaUZtIjaZdwoj1wNqOKoSmqR3ulbEDRcUpCDMAl8G5lpoEmZZLiT0Ij5FfY9nS7xyk7IzK9Xz13Un8Zu4At5vw0j8As-zV8jvb5K9Jr1Lsih1JTx9sn9xW-NXUPtw_9oLoPqd9AWg9RLkf4bI29z9IREYBA5CUQS7zLFYad1dzrospx8H4uhOTMLaEtdPqvTXpDFkDljgaI4NggYcdH2KcO4ciGtEjTQtm9dEfBw8xIG9LHN-UC3mq3t73Wu8jSZWIzB7ddyT5-ESXID5uSRq74Ch3dwWUwzHhOJZ_x0PLO9rglOF9_NbuZTyX7Mona9EnSRdHh3jIJxAM4bXBZErLYUb9hN2G6k-HboWtYCyHopzaX65AeqA0GRHsh47o; _ga_CTW8QM09XY=GS1.1.1710769039.1.1.1710769260.8.0.0',
    'Referer': 'https://portal.totalmateria.com/ru/search/quick/materials/5048801/mechanical',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'UnitSystem': '0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'ValueReturnMode': 'ActualAndFormattedValue',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

cookies_property = {
    '_hjSessionUser_939928': 'eyJpZCI6ImI5YjAzNTQ0LTBmMTItNTAzOS1hNDc0LTIyODc1NTA3YWQyOSIsImNyZWF0ZWQiOjE3MDM0MzAyNjE4ODMsImV4aXN0aW5nIjp0cnVlfQ==',
    '_ga': 'GA1.1.936484580.1703430260',
    'idsrv.session': 'C0CF1942811495385CF2F09022A48812',
    'totalmateria.session': 'CfDJ8DXxndW5yTRJm_OXW-4I-xKRarkkembfdI6_Jl0pNO4vA7TCv2vUPJsh2JNITvowR_tZHa9D_E6M50pXK_cLyp6ND3M6Ockf0jfFWy1MJyE9mNAkG72BxH6qBMS89pu4Vu4C-jOuzM4davqq842t2HgtXlcdoOYPVB03DrSCfI7Bictsa8o143T0CIQ-9m4t6aaKDJKB_S3KMRarjHSYe81RvjVdJWp2C5UNO8ilxC9Zo5sUQZeh3FeKu9MsRCtCCglKgTVRop4byA3lZdQ2BZQtAHNKntlnjW6eq1LM7UsT9MOO33gEp5jj-bwxS8Byqs7JkYzRHXrkm1C4QKFnJVk1PBiSLlpljDjgxalya8k6_VXt4bo8kdls6ov0umaG0O5dloxJgpQrvyiaJSwuRmHGvzqEzvGFdh6gUsq0axgFE5e4gqMNuyJAAjNv304_krQmPI3wlVLkzs1X0grmpeC24WAFkvCDWz9n5VQZBugV23_GH81TvP-W2I-0_sa7q56q7kgyKeSEvQtwVoZQi5VmsyebRjB6OFHsPGhoZywE9nzjjpnMmMB3ExUDPlHG9ide3oCZW-RW0o2hyeYSQ2UXB_r8mMir6mLydZfCFdhVXLo-f258H8ypNfRwwE8qWRshRPCOTPBAA6lATicZPBgcBtJ8IImd4x8oKm79KM40JQO1Os70lOvZ39UotGEJNOmdrmrr4W5RQFhpxxplYfg',
    '_ga_CTW8QM09XY': 'GS1.1.1709537440.8.1.1709540103.56.0.0',
}

headers_property = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjVDNkExQzcwOUNBQzE2M0FENDk3OTQ3Qjg1QjQ5ODkxQ0MzRDg0QkFSUzI1NiIsInR5cCI6IkpXVCIsIng1dCI6IlhHb2NjSnlzRmpyVWw1UjdoYlNZa2N3OWhMbyJ9.eyJuYmYiOjE3MDk1NDAwODIsImV4cCI6MTcwOTU3NjA4MiwiaXNzIjoiaHR0cHM6Ly9wb3J0YWwudG90YWxtYXRlcmlhLmNvbS9pZGVudGl0eSIsImF1ZCI6InNwYSIsIm5vbmNlIjoiTlUwMGRrRkZjVkpoTjFaSVVGRlljakpMU3paWmRqQm1iM1pIVjBOWmJsZEVlRnBpUkVzM1oydFZXR2g1IiwiaWF0IjoxNzA5NTQwMDc4LCJhdF9oYXNoIjoiQVFHTksybEVQb3VjVm1lTHRyNERrZyIsInNfaGFzaCI6IkVFV1BpOVdUV09NRG00anlXQTRFSHciLCJzaWQiOiJDMENGMTk0MjgxMTQ5NTM4NUNGMkYwOTAyMkE0ODgxMiIsInN1YiI6IjUxMTU4MTEzNDMyMDI0NDU0ODNYNzlRTVkzRDlaNEkyT0s5QU9IMThfMTAwIiwiYXV0aF90aW1lIjoxNzA5NTM4ODQ0LCJpZHAiOiJsb2NhbCIsIkZ1bGxOYW1lIjoiUG9wb3YgUm9tYW4iLCJVc2VyVHlwZSI6IjEwMCIsIkhhc0NvcnBvcmF0ZVVzZXJJZCI6IkZhbHNlIiwiSXNTaW5nbGVVc2VyIjoiRmFsc2UiLCJFbWFpbCI6ImNpcmV4aTU2MDZAaGlkZWx1eC5jb20iLCJTdWJzY3JpcHRpb25EYXRlIjoiMDUvMDIvMjAyNCIsIkNvcmUiOiJSfDB8MCIsIlNtYXJ0IENvbXAiOiJSfDB8MCIsIkV4dGVuZGVkIFJhbmdlIjoiUnwwfDAiLCJTdXBwbGllcnMiOiJSfDB8MCIsIlBvbHltZXJzUExVUyI6IlJ8MHwwIiwiZVhwb3J0ZXIiOiJSfDB8NSIsIlRyYWNrZXIiOiJSfDB8MCIsIkRhdGFQTFVTIjoiUnwwfDAiLCJFbnZpcm8iOiJSfDB8MCIsIkNvbXBsaWFuY2UiOiJSfDB8MCIsIk1hdGVyaWFsQ29uc29sZSI6IlJ8MHwwIiwiYW1yIjpbInB3ZCJdfQ.c-kxpSQ-I-s9dhYE6UvWIFqKmJa7j8uS-aPPy3PBQBkqYOeBlZfLUnl57vcCVS2H2ab8-d7m4c-A-qTgv2Vsp0Nd5LWS2UUGS75PHziWO88Nb2SBYnVFbz2F4KkLPAg6e6mm1SlcIphFR1_4MgJbvE2vDyfxdt-kWEYOoLe_JU7_HunvT7saw_jPP0MiL1d_mHE1AgmMKSSR-4MrXkMlK6aAn4-lNhjfG9tCpydCQKLXH4qTWKGvxiVvrPxthP2zxcxKr7G2gqVYFeYqLhtshWMWcDndX4CItL3IQAMwTaBHNbAd2y30MSyR9ahCDxhYYkN7BtaB_B2gfUvAK-NyNA',
    'Connection': 'keep-alive',
    # 'Cookie': '_hjSessionUser_939928=eyJpZCI6ImI5YjAzNTQ0LTBmMTItNTAzOS1hNDc0LTIyODc1NTA3YWQyOSIsImNyZWF0ZWQiOjE3MDM0MzAyNjE4ODMsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.1.936484580.1703430260; idsrv.session=C0CF1942811495385CF2F09022A48812; totalmateria.session=CfDJ8DXxndW5yTRJm_OXW-4I-xKRarkkembfdI6_Jl0pNO4vA7TCv2vUPJsh2JNITvowR_tZHa9D_E6M50pXK_cLyp6ND3M6Ockf0jfFWy1MJyE9mNAkG72BxH6qBMS89pu4Vu4C-jOuzM4davqq842t2HgtXlcdoOYPVB03DrSCfI7Bictsa8o143T0CIQ-9m4t6aaKDJKB_S3KMRarjHSYe81RvjVdJWp2C5UNO8ilxC9Zo5sUQZeh3FeKu9MsRCtCCglKgTVRop4byA3lZdQ2BZQtAHNKntlnjW6eq1LM7UsT9MOO33gEp5jj-bwxS8Byqs7JkYzRHXrkm1C4QKFnJVk1PBiSLlpljDjgxalya8k6_VXt4bo8kdls6ov0umaG0O5dloxJgpQrvyiaJSwuRmHGvzqEzvGFdh6gUsq0axgFE5e4gqMNuyJAAjNv304_krQmPI3wlVLkzs1X0grmpeC24WAFkvCDWz9n5VQZBugV23_GH81TvP-W2I-0_sa7q56q7kgyKeSEvQtwVoZQi5VmsyebRjB6OFHsPGhoZywE9nzjjpnMmMB3ExUDPlHG9ide3oCZW-RW0o2hyeYSQ2UXB_r8mMir6mLydZfCFdhVXLo-f258H8ypNfRwwE8qWRshRPCOTPBAA6lATicZPBgcBtJ8IImd4x8oKm79KM40JQO1Os70lOvZ39UotGEJNOmdrmrr4W5RQFhpxxplYfg; _ga_CTW8QM09XY=GS1.1.1709537440.8.1.1709540103.56.0.0',
    'Referer': 'https://portal.totalmateria.com/en/search/quick/results',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'UnitSystem': '0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'ValueReturnMode': 'ActualAndFormattedValue',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}



# Функция для рекурсивного извлечения ID только тех элементов, у которых нет дочерних элементов
def extract_leaf_ids(node):
    ids = []
    if 'children' in node:
        if not node['children']:  # Проверка на отсутствие дочерних элементов
            if 'id' in node:
                ids.append(node['id'])
        else:
            for child in node['children']:
                ids.extend(extract_leaf_ids(child))
    return ids


def fetch_material_data(group_id, cookies, headers):
    json_data = {
        'commonSearchType': 2,
        'materialGroups': [{'id': group_id}],
    }

    response = requests.post(
        'https://portal.totalmateria.com/referencedata/ru/total-search/quick-search',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False
    )

    if response.status_code == 200:
        return response.json()
    else:
        print("Ошибка запроса для группы ID:", group_id, "Статус код:", response.status_code)
        return None

# Функция для сохранения данных в файл
def save_to_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)




# response = requests.get('https://portal.totalmateria.com/referencedata/ru/material-groups', cookies=cookies, headers=headers)
# if response.status_code == 200:
#     # Преобразование ответа в JSON
#     data = response.json()
#
#     # Запись данных в файл
#     with open('data.json', 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)
# else:
#     print("Ошибка запроса: Статус код", response.status_code)

# Изменённая функция для сбора ID всех групп
def collect_group_ids(entry):
    """
    Рекурсивно собирает ID и имена всех групп из данной структуры данных.
    """
    groups = []
    # Добавление информации о текущей группе, если у неё есть ID
    if 'id' in entry and 'name' in entry:
        groups.append({'id': entry['id'], 'name': entry['name']})
    # Рекурсия по детям, если они существуют
    if 'children' in entry:
        for child in entry['children']:
            groups.extend(collect_group_ids(child))
    return groups