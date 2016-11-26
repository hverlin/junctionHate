from facepy import GraphAPI

class TextFromFacebook():
    def __init__(self):
        app_id = "350491891978824"
        app_secret = "7ac945d57ec6ba7396bd770dd5474ab7"

        self.graph = GraphAPI(oauth_token=app_id + "|" + app_secret)

        # self.graph = GraphAPI(oauth_token=access_token)

    def get_page_id(self, page_name):
        request = page_name
        answer = self.graph.get(request)
        return answer["id"]

    # return a list with all the post message and their id
    def get_posts_from_page(self, page_name, post_number):
        id = self.get_page_id(page_name)

        post_list = []

        request = id + "/posts"
        posts = self.graph.get(path=request, limit=post_number)
        for p in posts["data"]:
            if "message" in p:
                self.string_list.append(p["message"])
                post = {"id": p["id"], "message": p["message"]}
                post_list.append(post)

        return post_list

    def get_comments_from_post(self, post_id, comment_number):

        request = post_id + "/comments"
        comments = self.graph.get(path=request, limit=comment_number)
        comment_list = []

        for c in comments["data"]:
            if "message" in c:
                comment_list.append(c["message"])

        return comment_list

    # return the number of reactions by type of reaction : "LIKE","LOVE","HAHA","WOW","SAD","ANGRY","THANKFUL"
    def get_reactions_from_post(self, post_id):

        request = post_id + "/reactions"
        summary = "total_count"
        reaction_possibility = {"LIKE", "LOVE", "HAHA", "WOW", "SAD", "ANGRY", "THANKFUL"}
        reaction_count = dict()

        for rp in reaction_possibility:
            reactions = self.graph.get(path=request, limit=0, type=rp, summary=summary)
            number_react = reactions["summary"]["total_count"]
            reaction_count[rp] = number_react

        return reaction_count
