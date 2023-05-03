# Pico_GardenWaterer_v2
Contains MicroPython code for an automated container garden watering system using a Raspberry Pi Pico and Chirp moisture sensors.  Moisture levels and pump activity are uploaded to a [ThingSpeak.com](http://www.thingspeak.com) dashboard for monitoring.

The sensors and relay board use the I2C protocol to communicate so you could expand this up to 100+ devices with appropriate power supply, relay boards and I2C multiplexors.

All materials can be found in the [BOM](https://github.com/TazwellJ/Pico_GardenWaterer_v2/blob/main/BOM.txt) file.

#Background
This whole project started because I decided I needed a hobby.  I like to work with my hands but I don't have space for something like a full woodworking workshop.  So I thought about what I could do that didn't require a lot of large machines and would be relatively inexpensive to get into.  I have a degree in electronics (that I haven't used for 30 years) and a career as a programmer.  That being said, I realized that the world of Arduino/Raspberry Pi could be interesting to investigate.  I started watching videos about projects I could try and I ended up here.  A fully-automated garden watering system.  

Maybe this year I won't eventually kill any plants I try to grow.

#Hardware
I chose a Raspberry Pi Pico because they're:
  1. Inexpensive
  2. Perfectly suited to the task
  3. Readily available

The Chirp sensors (link available in the [BOM](https://github.com/TazwellJ/Pico_GardenWaterer_v2/blob/main/BOM.txt)) were purchased after much research and a disasterous first attempt with cheap capacitive moisture sensors.  You get what you pay for.

The motorized ball valve was the final solution to refilling the reservoir from the rain barrel.  A low power solenoid didn't have enough water pressure (via gravity feed) to actuate.  A pump didn't have any way to actually stop the flow of water when the bucket was full.  I suppose I could have used a combination of the two but I just didn't want to.  The ball valve also served the function of turning refilling of the reservoir off if power was lost to prevent overfilling/flooding.
