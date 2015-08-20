##Piggydash
---

###Objectives
Use the [Amazon Dash button](https://www.amazon.com/oc/dash-button) as a modern day piggybank. Specifically, use a Raspberry Pi and Python to intercept the Dash's HTTP requests to Amazon and redirect them to a web server inside my LAN that (ab)uses the [Simple](https://simple.com) API to transfer money out of my checking account into a rainy day fund.

Inspired by [Ted  Benson's Medium post](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8) on his Dash hack.


###Requirements
- Python 3.4 or 2.7
- An appropriate version of Pip
- Everything in `requirements.txt` (`pip install -r requirements.txt`)
- An Amazon Dash button (or similar)
- A Raspberry Pi or other dedicated server inside your LAN
- A router you have administrative access over (MAC filtering)
- An Instapush account (optional)

Full instructions to come via my own Medium post.
