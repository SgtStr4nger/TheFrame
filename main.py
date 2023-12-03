from API_Access import CurrentlyPlaying

import json



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(type(CurrentlyPlaying()["cover_url"]))
    print (json.dumps(CurrentlyPlaying(), indent=2))

