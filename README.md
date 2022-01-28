
# SOSum: A dataset of extractive summaries of Stack Overflow posts and associated labeling tools

This repository contains SOSum: a dataset of extractive summaries of 2278 Stack Overflow (SO) posts under 506 most popular SO questions. We also publish necessary tools used for dataset construction which include (1) a GUI for labeling CSV files of SO posts in the same format of SOSum and (2) a chrome extension for labeling posts on SO website. It is our vision that SOSum will foster research on sentence-level summarization of SO posts and has the potential to facilitate text summarization research on other types of textual software artifacts such as programming tutorials. More details of the dataset can be found in our MSR 2022 paper that's currenty under review (SOSum: A Dataset of Extractive Summaries of Stack Overflow Posts).

## SOSum 
### Sentence-level SO post summarization
Stack Overflow (SO) is becoming an indispensable part of the modern software development workflow. However, navigating SO posts and comparing different solutions is time-consuming and cumbersome given the limited time, attention, and memory capacity of programmers. Recent research has proposed to summarize SO posts to concise text to help programmers quickly decide the relevance and quality of SO posts. Yet there is no large, comprehensive dataset of high-quality SO post summaries, which hinders the development and evaluation of post summarization techniques. We present SOSum, a dataset of 2278 popular SO posts with manually labeled summative sentences. Questions in SOSum cover 669 tags with a median view count of 253K and a median post score of 17. This dataset will foster research on sentence-level summarization of SO posts and has the potential to facilitate text summarization research on other types of textual software artifacts such as programming tutorials.

### Data format
SOSum is stored in two separate CSV files: `question.csv` and `answer.csv`. Both can be found in `data` folder.

`question.csv` contains metadata of 506 popular SO questions. We summarize its fields as below:
|Field | Description|
| ----------- | ----------- |
|Question Id| Post Id of the SO question|
|Question Type| 1 for conceptual questions, 2 for how-to questions, 3 for debug-corrective questions|
|Question Title |Question title as a string|
|Question Body |A list of sentences from the question post content|
|Tags |SO tags associated with a question|
|Answer Posts| A list of post ids separated by comma|

`answer.csv` contains metadata of 506 popular SO questions. We summarize its fields as below:
|Field | Description|
| ----------- | ----------- |
|Answer Id |Post Id of a SO answer post|
|Answer Body |A list of sentences from the post content|
|Summary |Summative sentences from the post content|

## Labeling tools
Both the GUI and chrome extension can be found in `labeling_tools` folder.
### GUI for labeling CSV files
A GUI tool is developed to facilitate labeling of SO posts in CSV files with the same format of `question.csv` and `answer.csv`. A screenshot of our GUI is displayed below.
![A screenshot of GUI](screenshot_wide.jpg)

### Chrome extension for online labeling
As many new SO posts are posted everyday, one may also be interested in labeling SO posts from the website rather than the data dump. Therefore, we also developed a Chrome extension for labeling SO posts in the web browser. A user can select one or more sentences from a post, right click, and choose ``Mark as Summative Sentence'' to label them as summative sentences. Once the labeling is done, the user can press ``CTRL+ENTER'' to download the post content as well as the labeled summative sentences into a CSV file.

A link for tutorial video: https://youtu.be/Xo5JyW486O4


