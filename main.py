from short_link_maker import ShortLinkMaker

shortLinkMaker = ShortLinkMaker()

shortLinkMaker.new_link("www.a1.com")


while True:
    link = input()
    shortLinkMaker.reference_link(link)
