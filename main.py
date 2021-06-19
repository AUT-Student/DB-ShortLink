from short_link_maker import ShortLinkMaker


shortLinkMaker = ShortLinkMaker()

print(
    "Commands list:\n"
    "* EXIT\n"
    "* SUBMIT\n"
    "* REF\n"
    "* DASHBOARD\n"
)

while True:
    command = input("Enter command:")

    if command == "EXIT":
        break

    elif command == "SUBMIT":
        url = input("Enter url:")
        link = shortLinkMaker.submit_url(url)
        print(f"Link: {link}")

    elif command == "REF":
        link = input("Enter link:")
        print(shortLinkMaker.reference_link(link))

    elif command == "DASHBOARD":
        shortLinkMaker.dashboard()
