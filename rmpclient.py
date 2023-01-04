import requests


class RateMyProfessorsClient:
    cache = {}

    def __init__(self):
        self.auth_token = "dGVzdDp0ZXN0"
        self.base_url = "https://www.ratemyprofessors.com/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "authorization": f"Basic {self.auth_token}"
        }
        self.autocomplete_school_query = """
            query AutocompleteSearchQuery($query: String!) {
                autocomplete(query: $query) {
                    schools {
                        edges {
                            node {
                                id
                                name
                                city
                                state
                            }
                        }
                    }
                }
            }
        """

        self.autocomplete_teacher_query = """
            query AutocompleteSearchQuery($query: String!) {
                autocomplete(query: $query) {
                    teachers {
                        edges {
                            node {
                                id
                                firstName
                                lastName
                                school {
                                    name
                                    id
                                }
                            }
                        }
                    }
                }
            }
        """

        self.search_teacher_query = """
            query NewSearchTeachersQuery($text: String!, $schoolID: ID!) {
                newSearch {
                    teachers(query: { text: $text, schoolID: $schoolID }) {
                        edges {
                            cursor
                            node {
                                id
                                firstName
                                lastName
                                school {
                                    name
                                    id
                                }
                            }
                        }
                    }
                }
            }
        """

        self.get_teacher_query = """
            query TeacherRatingsPageQuery($id: ID!) {
                node(id: $id) {
                    ... on Teacher {
                        id
                        firstName
                        lastName
                        school {
                            name
                            id
                            city
                            state
                        }
                        avgDifficulty
                        avgRating
                        department
                        numRatings
                        legacyId
                        wouldTakeAgainPercent
                    }
                    id
                }
            }
        """

    def search_school(self, query):
        if query in RateMyProfessorsClient.cache:
            return RateMyProfessorsClient.cache[query]

        body = {
            "query": self.autocomplete_school_query,
            "variables": {
                "query": query
            }
        }

        response = requests.post(self.base_url, headers=self.headers, json=body)
        json_response = response.json()
        RateMyProfessorsClient.cache[query] = [edge["node"] for edge in
                                               json_response["data"]["autocomplete"]["schools"]["edges"]]
        return RateMyProfessorsClient.cache[query]

    def search_teacher(self, name, school_id):
        cache_key = f"{name}-{school_id}"
        if cache_key in RateMyProfessorsClient.cache:
            return RateMyProfessorsClient.cache[cache_key]

        body = {
            "query": self.search_teacher_query,
            "variables": {
                "text": name,
                "schoolID": school_id
            }
        }

        response = requests.post(self.base_url, json=body, headers=self.headers)
        json_response = response.json()
        if json_response["data"]["newSearch"]["teachers"] is None:
            return []

        RateMyProfessorsClient.cache[cache_key] = [edge["node"] for edge in
                                                   json_response["data"]["newSearch"]["teachers"]["edges"]]
        return RateMyProfessorsClient.cache[cache_key]

    def get_teacher(self, teacher_id):
        if teacher_id in RateMyProfessorsClient.cache:
            return RateMyProfessorsClient.cache[teacher_id]
        body = {
            "query": self.get_teacher_query,
            "variables": {
                "id": teacher_id
            }
        }

        response = requests.post(self.base_url, headers=self.headers, json=body)
        json_response = response.json()
        RateMyProfessorsClient.cache[teacher_id] = json_response["data"]["node"]
        return RateMyProfessorsClient.cache[teacher_id]
