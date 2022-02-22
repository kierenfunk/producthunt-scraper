"""ProductHunt Web Scraper

"""

import requests
import base64

if __name__ == "__main__":

    has_next_page = True
    cursor = 0
    increment = 100
    all_topics = []
    while has_next_page:
        session = requests.Session()
        query = "query TopicsPage($cursor:String$query:String$order:String){topics(query:$query first:"+str(increment)+" after:$cursor order:$order){edges{node{id ...TopicsPageItemFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}}fragment TopicsPageItemFragment on Topic{id name slug description ...TopicFollowButton ...TopicImage __typename}fragment TopicFollowButton on Topic{id slug name isFollowed followersCount ...TopicImage __typename}fragment TopicImage on Topic{name imageUuid __typename}"
        response = session.post('https://www.producthunt.com/frontend/graphql',
            json={
                'query': query, 
                'operationName': "TopicsPage",
                'variables': {
                    'query': None,
                    'cursor': base64.b64encode(str.encode(f'{cursor}')).decode("utf-8"),
                    'order': 'trending'
                    }
                },
            headers={
                'content-type': 'application/json; charset=utf-8'
            }
        ).json()
        print(base64.b64encode(str.encode(f'{cursor}')).decode("utf-8"))
        print(response['data']['topics']['pageInfo'])
        #print(response['data']['topics']['pageInfo']['hasNextPage'])
        all_topics.extend([edge['node'] for edge in response['data']['topics']['edges']])
        #print([topic['name'] for topic in topics])
        #print(len(topics))
        print(len(all_topics))
        cursor += increment
        has_next_page = response['data']['topics']['pageInfo']['hasNextPage']
        #if cursor > 99:
        #    has_next_page = False

    #for topic in topics:
    #    print(topic['name'], topic['description'], topic['followersCount'])
    #print(len(topics))

    #print(response.json())