import json

import requests


cookies = {
    '_hjSession_939928': 'eyJpZCI6IjhkOTRkNGNmLWJhNTAtNGM3NS04ODA5LTkxZGJhMDAzNzI4MiIsImMiOjE3MTA1MDg0Mjc3ODAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
    '_ga': 'GA1.1.91813129.1710508428',
    '_hjSessionUser_939928': 'eyJpZCI6Ijc4ODYyZDY5LWNiODItNTY5MC1hZjJmLTkwOGEwYWU1ZmJlYSIsImNyZWF0ZWQiOjE3MTA1MDg0Mjc3NzgsImV4aXN0aW5nIjp0cnVlfQ==',
    'idsrv.session': 'A80B467708F276D7C11EB08CCAD5F716',
    'totalmateria.session': 'CfDJ8DXxndW5yTRJm_OXW-4I-xKVIqu9Uk1aZUV8CQ03WFRKgQxXkgNTynTXpDX5Pmp3rwkYJ_3s51FiSK7kaX3U8Hq3ImM8CuI86ps2AINGxBtUe_HXai29iEJ_N38XBlokjVTE06wc01lCuUKbMI3ehJvjQgQ_E68KNfzMazgYWJ5knYpMQyoI-WZkU6mCP7fKrHIi9qRe_F87LlMktBkeqDX8WE_jmf0j2ir-d1JOoUESInsM59CO37x82UK73bKIEQtCdWhAY-t_BNJ9TT5PwQdbMb1n6URO43b2J6U1zUEs7Oq7RcZ1XI_6bAqnB6_fVQ_R99es24kUGVVQ3AClu6NggSRQv8NbVFMN4vPqPdUSh7twYJpCYzcfS6vCRxjAaTZEh2evDots43Ja_5L5A-HDvBkoBq-yIyOowv83XDMPeUwi7swZClWE0073dY_h_oYkSjQRw8ZSJ7N9FaYOVamhbKMHbtybq3bs72EJF6Fm-zC-yDQOy_NRr02Sqpr8uNAD9MlVeVlHI0n55Y5rkrD79VBfdh14tjWZRnDlzvDI6At17mplwpktnWxIDVNMqJGisdA4o3gke4ifbmsxx9z8aWY6FAjT-aTlO21eXSJ6kRzaXQ2dqDBvBSepaNxdGQI0DDdrTrT37cq0Fv0l34i2DL2YwAd9Zwkpg1EHWX8NsrkvH6pJQbdloIQt8qhvNdjV_wS3rsrQv6_M44I8bUQ',
    '_ga_CTW8QM09XY': 'GS1.1.1710508427.1.1.1710508595.14.0.0',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjVDNkExQzcwOUNBQzE2M0FENDk3OTQ3Qjg1QjQ5ODkxQ0MzRDg0QkFSUzI1NiIsInR5cCI6IkpXVCIsIng1dCI6IlhHb2NjSnlzRmpyVWw1UjdoYlNZa2N3OWhMbyJ9.eyJuYmYiOjE3MTA1MDg1OTYsImV4cCI6MTcxMDU0NDU5NiwiaXNzIjoiaHR0cHM6Ly9wb3J0YWwudG90YWxtYXRlcmlhLmNvbS9pZGVudGl0eSIsImF1ZCI6InNwYSIsIm5vbmNlIjoiWTBSRGFtcFhjRzFzVUdKVmEySlhMVmRMT0dORE1XWi1ka3QwV1ZST1VsWTFiV0oyTldrMlRsbzJVVWRFIiwiaWF0IjoxNzEwNTA4NTk1LCJhdF9oYXNoIjoiRlFXLUFHTmdtTmg0VnB4Vm54ZmVvZyIsInNfaGFzaCI6IjNSMDdqZ0N5b0VwVHl1M3UzOXJXMnciLCJzaWQiOiJBODBCNDY3NzA4RjI3NkQ3QzExRUIwOENDQUQ1RjcxNiIsInN1YiI6IjUxMTU0NTIzMjAyNDE1MTYxNDE5UzkyNkU2TFhWNUxFM0kyOTA0U0VfMTAwIiwiYXV0aF90aW1lIjoxNzEwNTA4NTgwLCJpZHAiOiJsb2NhbCIsIkZ1bGxOYW1lIjoi0KDQvtC80LDQvSDQn9C-0LvRg9C90LjQvSIsIlVzZXJUeXBlIjoiMTAwIiwiSGFzQ29ycG9yYXRlVXNlcklkIjoiRmFsc2UiLCJJc1NpbmdsZVVzZXIiOiJGYWxzZSIsIkVtYWlsIjoieGl3ZXZvdzM5N0Bpcm5pbmkuY29tIiwiU3Vic2NyaXB0aW9uRGF0ZSI6IjA1LzE0LzIwMjQiLCJDb3JlIjoiUnwwfDAiLCJTbWFydCBDb21wIjoiUnwwfDAiLCJFeHRlbmRlZCBSYW5nZSI6IlJ8MHwwIiwiU3VwcGxpZXJzIjoiUnwwfDAiLCJQb2x5bWVyc1BMVVMiOiJSfDB8MCIsImVYcG9ydGVyIjoiUnwwfDUiLCJUcmFja2VyIjoiUnwwfDAiLCJEYXRhUExVUyI6IlJ8MHwwIiwiRW52aXJvIjoiUnwwfDAiLCJDb21wbGlhbmNlIjoiUnwwfDAiLCJNYXRlcmlhbENvbnNvbGUiOiJSfDB8MCIsImFtciI6WyJwd2QiXX0.EWqIwM7MKFjlGHShnb6Bs86xz6x-aRqOOwGumtfs-QTuHNeXQLKImgqM-Uid02oNj38og2KpFDjA6DkiUu6t3uVvmtzQt1VrUXkR2MMps0oARAPSVoShTFF634rGYheX9rVnuFF3WzqS8r0k6Y3_KcPalil0yIZ1KbaZ1UrKa3ffIsHig8w2rt5-VgL30359yG1cQUUhkW_hfFin-yk4l4ZecKZ6HIxRIQBay7Ml2RvU7YxjSVg6qiQEE2AQ1rnaH-MYjZLtxjoaD-9fKJYsNfB48WtbtXjRahSdxuALC0UTHZx-ppFnfqBLB9yVH-TghvjkReQ_RcFad-KYfq2uyg',
    'Connection': 'keep-alive',
    # 'Cookie': '_hjSession_939928=eyJpZCI6IjhkOTRkNGNmLWJhNTAtNGM3NS04ODA5LTkxZGJhMDAzNzI4MiIsImMiOjE3MTA1MDg0Mjc3ODAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _ga=GA1.1.91813129.1710508428; _hjSessionUser_939928=eyJpZCI6Ijc4ODYyZDY5LWNiODItNTY5MC1hZjJmLTkwOGEwYWU1ZmJlYSIsImNyZWF0ZWQiOjE3MTA1MDg0Mjc3NzgsImV4aXN0aW5nIjp0cnVlfQ==; idsrv.session=A80B467708F276D7C11EB08CCAD5F716; totalmateria.session=CfDJ8DXxndW5yTRJm_OXW-4I-xKVIqu9Uk1aZUV8CQ03WFRKgQxXkgNTynTXpDX5Pmp3rwkYJ_3s51FiSK7kaX3U8Hq3ImM8CuI86ps2AINGxBtUe_HXai29iEJ_N38XBlokjVTE06wc01lCuUKbMI3ehJvjQgQ_E68KNfzMazgYWJ5knYpMQyoI-WZkU6mCP7fKrHIi9qRe_F87LlMktBkeqDX8WE_jmf0j2ir-d1JOoUESInsM59CO37x82UK73bKIEQtCdWhAY-t_BNJ9TT5PwQdbMb1n6URO43b2J6U1zUEs7Oq7RcZ1XI_6bAqnB6_fVQ_R99es24kUGVVQ3AClu6NggSRQv8NbVFMN4vPqPdUSh7twYJpCYzcfS6vCRxjAaTZEh2evDots43Ja_5L5A-HDvBkoBq-yIyOowv83XDMPeUwi7swZClWE0073dY_h_oYkSjQRw8ZSJ7N9FaYOVamhbKMHbtybq3bs72EJF6Fm-zC-yDQOy_NRr02Sqpr8uNAD9MlVeVlHI0n55Y5rkrD79VBfdh14tjWZRnDlzvDI6At17mplwpktnWxIDVNMqJGisdA4o3gke4ifbmsxx9z8aWY6FAjT-aTlO21eXSJ6kRzaXQ2dqDBvBSepaNxdGQI0DDdrTrT37cq0Fv0l34i2DL2YwAd9Zwkpg1EHWX8NsrkvH6pJQbdloIQt8qhvNdjV_wS3rsrQv6_M44I8bUQ; _ga_CTW8QM09XY=GS1.1.1710508427.1.1.1710508595.14.0.0',
    'Referer': 'https://portal.totalmateria.com/ru/search/quick/materials/5119685/mechanical',
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