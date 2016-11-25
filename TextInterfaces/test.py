from TextInterfaces.TextFromFacebook import TextFromFacebook



tff = TextFromFacebook()
page = "DonaldTrump"
posts = tff.get_posts_from_page(page_name=page,post_number=10)

post="153080620724_10158184936910725"
comments = tff.get_comments_from_post(post_id=post,comment_number=10)

reactions = tff.get_reactions_from_post(post_id=post)
print(reactions)