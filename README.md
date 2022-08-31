# Distributed System:Story visualization with image search engine


by David Musaev and Niv Dadush

# Motivation
Attaching image to many phrase to create more easy readable text
# Roadmap
#### 1 : Creating/Using  Google Image Scrapper for Scrapping image by phrase
#### 2 : Creating/Using IDF-TF Image Search by term
#### 3 : Creating Flask WebPage with Browser div and Story div



## Usage

### turn this
Glinda, the good Sorceress of Oz, sat in the grand court of her
palace, surrounded by her maids of honor--a hundred of the most
beautiful girls of the Fairyland of Oz. The palace court was built of
rare marbles, exquisitely polished.

### into this




![alt text](https://i.postimg.cc/FswBBDTn/Glindathegood-Sorceressof-Ozsatinthegrandcourtofher0.jpg)
Glinda, the good Sorceress of Oz, sat in the grand court of her
![alt text](https://i.postimg.cc/j5qg79jC/palacesurroundedbyhermaidsofhonorahundredofthemost0.jpg)
palace, surrounded by her maids of honor--a hundred of the most
![alt text](https://i.postimg.cc/bvhFzdcx/Thepalacecourtwasbuiltofraremarbles0.jpg)
beautiful girls of the Fairyland of Oz. The palace court was built of
![alt text](https://i.postimg.cc/Gpxg9rdZ/Thepalacecourtwasbuiltofraremarblesexquisitelypolished0.png)
rare marbles, exquisitely polished.


## architecture and use case
[![Architercture.png](https://i.postimg.cc/PxhWp824/Architercture.png)](https://postimg.cc/4KL7jnC7)
### Case 1: The user will request to visualize a story from story list and it will processed by Master-Worker Zookeeper topology and will returned as visualized story
### Case 2: The user will search an image and the request will be processed by master search of IDF-TF algorithms 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
