from TextInterfaces.TextFromTwitter import TextFromTwitter



tft = TextFromTwitter()
user = "abcd"
status = tft.get_status_from_user(user=user,tweet_number=3)
print(status)