# YouTube Word Searcher (YWS)

#### Video Demo:  https://www.youtube.com/watch?v=S3mc4vIKo7c


#### Description:

    A Word searcher that looks for the specific time a word is spoken in a video. When clicking in the timeline with the name of the searched word your will see when that word was spoken.


## Project Structure

    The project is organized into the following main files:

`app.py`: This is the main Python script that manages the routes.

`Data.py`: It manages the data, get from youtube and populate the Trie, and retrieve requested information from Trie

`Trie.py`: The Trie object

`youtube.py`: This file manages youtube data

`data/`: This directory contains serialized trie and a json with videos details
- video-list.json: A binary json with channel and video details
- search_video.jls: A binary trie with all words of indexed videos

`templates/`: This directory contains HTML templates for the user interface.
- index.html: the home html
- more.html: An about page
- layout.html: The main layout
- channel.html: A page to index channels

`static/`: This directory holds static files such as CSS styles and JavaScript.
- ico.png: The icon.
- video-list.js: The video list manager from the user side, it receives the video data and manage creating the video list, the pagination, the video frames and sorting.
- styles.css: The style sheet.

`requirements.txt`: A list of required Python libraries and dependencies for running the project locally. You can install them using pip by running pip install -r requirements.txt.


## Search Behavior

The search functionality in this tool operates as follows:

- Words are searched from left to right in the video's content.
- The default result includes videos in which all searched words occur, except when a special character precedes a word.


## Special Characters

Special characters modify the search behavior:

- `&` - Concatenates the answer: Every word starting with an '&' will have all their results concatenated to the list.
- `-` - Removes from the answer: Every word starting with an '-' will have all the videos containing this word removed from the list.


## Usage

To use the YouTube Word Searcher:


1.   Search words in video: 127.0.0.1:5000
- 1.1. Enter your search query, if needed specify any special characters to modify the - search.
- 1.2. Click the "Search" button.
- 1.3. The results will display the videos where the specified words occur, along with timestamps.
- 1.4. Clicking at the timestamps you will see the video at that specific time.
2.   Add Channel: 127.0.0.1:5000/add/channel
- 2.1. Enter the channel url (url must have a video collection - https://www.youtube.com/@channel-name/videos)
- 2.2 Click Add and wait, it will scan for every video on this channel and populate the trie, when finished the page will be redirected to home. Be patient, it could spend several hours per channel.


## Limitations

    - Anyway, it is good to know that actually Pickle will have trouble serializing data with more than 2gb (check the `./data/search_video.jls` file size).
    - If you change the Trie, keep in mind some limitations like recursion limit and size. Abuse of pointers will made the system stop without a debug message.


## Installation

To run the project locally, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies from the requirements.txt (`pip install requirements.txt`).
3. Run the application using `flask run`.
4. The home address should be: 127.0.0.1:5000


## Acknowledgments

I want to extend my gratitude to the authors and maintainers of the following third-party modules and libraries used in this project:

- [yt_dl](https://github.com/ytdl-org/youtube-dl): Used for YouTube video downloading and processing.
- [Youtube iframe_api](https://www.youtube.com/iframe_api): Used to manage youtube frames in user side.

These modules and libraries have been instrumental in the development of this project


## Contact

If you have any questions or need assistance, please feel free to reach out to `Jefferson Lopes de Sousa` at github.com/jeffersonpp

Enjoy searching for words in YouTube videos with the YouTube Word Searcher!