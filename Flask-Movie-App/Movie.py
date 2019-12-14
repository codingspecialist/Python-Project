class Movie:
    def __init__(self, rating, title, synopsis, medium_cover_image):
        self.rating = rating
        self.title = title
        self.synopsis = synopsis
        self.medium_cover_image = medium_cover_image

    def __str__(self):
        return f"rating : '{self.rating}' title :'{self.title}'"

# m = Movie('9999', 'oldboy','kill everyone', 'http://www.naver.com')
# print(m)