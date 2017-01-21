##Piggydash
---

###Objectives
Use the [Amazon IoT Dash button](https://aws.amazon.com/iotbutton/) as a modern day piggybank. Uses the [Simple](https://simple.com) API to transfer money out of my checking account into a rainy day fund.

Inspired by [Ted  Benson's Medium post](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8) on his Dash hack.

Originally this project ran on a normal Dash button and a local Raspberry Pi, but since the IoT Dash Button was released I've moved it to AWS Lambda. If you want to run it yourself you can deploy it out to your own Lambda and link the IoT button as a trigger, or potentially use a normal Dash button to send an HTTP request to API Gateway and trigger the Lambda that way, if you've hacked your v1 Dash button to send custom HTTP requests.
