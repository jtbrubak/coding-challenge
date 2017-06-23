# Publishing Service

This fun little API can do a few things for you: it can give you a status, tell you info about musical artists, and publish an image to an HTML page on S3 for you to look at. You can use it by plugging the address right into your web browser, or by using the ```curl``` command in the console. All responses come back in the form of plain text, so be sure to set your response type to text if you're using Postman or similar services.

The API root URL is located at ```https://92h6vidxpg.execute-api.us-east-1.amazonaws.com/dev```

# Status

You can get a status by accessing the root URL. It will give you a happy little message, a 200 OK status, and your IP address, like so:

```
Hello! You have reached Jeff's Rad Publishing Service!
Your IP address is [whatever]!
Here's a rad 200 OK Status for your troubles!
```

This is achieved very simply. Chalice logs certain attributes for every API request in a JSON object, including the requester's IP address. A little bit of string interpolation via the ```format()``` method is all that's needed here (the "200 OK" bit is hardcoded because I figure if you're getting the message, it's a 200 OK).

# Artist Info

This is a fun feature that will, for any musical artist, give you common tags used for the artist as well as their five most popular songs. Both of these bits of data are taken from the Last.fm API. You use it like so:

```https://92h6vidxpg.execute-api.us-east-1.amazonaws.com/dev/artist/[artist name]```

And don't forget to use pluses in lieu of spaces if you're looking for an artist whose name is more than one word, i.e.:

```https://92h6vidxpg.execute-api.us-east-1.amazonaws.com/dev/artist/the+beatles```

So using that Beatles example, we get this response:

```
Here's a little info about The Beatles. This artist has been tagged as classic rock, rock, british, 60s, and pop.
Their most popular songs are:
Come Together
Let It Be
Yesterday
Help!
Here Comes the Sun
```

Neat, huh? This method makes two calls to Last.fm's API, one for general info about the artist and one for the artist's most popular songs. The calls are made using the ```urlopen``` function from the ```urllib``` library. The responses come back as Python objects, which then have to be converted to JSON using the ```json``` library. Between these two calls, however, we have all the info we need. We simply interpolate them into a nice multi-line string, again using the ```format()``` function. I also figured it'd be a good idea to take the artist's name from the JSON rather than the user's request, that way I avoid nasty lowercase letters and '+' characters when interpolating.

# Image Publisher

Finally, we have this image publishing service. We're using a query parameter for this one, like so: 

```https://92h6vidxpg.execute-api.us-east-1.amazonaws.com/dev/image/?image-file=[image address]```

What this does it take the image's address and uploads an HTML file containing an IMG tag with the source attribute pointing to the image. This is accomplished using the ```boto3``` library, which interfaces between Python and AWS, and specifically the library's ```put_object``` method. The ```put_object``` method had a few attributes that needed to calibrated, such as the bucket to be uploaded to and the key of the file. Most importantly though, I had to set the ```ContentType``` to 'text/html' so that it would be recognized as an HTML file, and the body of the file to simply ```<html><img src={0}></html>``` with the image's address interpolated in. Finally, since permissions are denied by default with any upload, I used the ```put_object_acl``` method of ```boto3``` to set permissions to 'public-read', allowing anyone to access the file. The API then returns a string which carries the URL of the HTML file.


