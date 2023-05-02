# Pico_GardenWaterer_v2
Contains code for an automated container garden watering system using a Raspberry Pi Pico and Chirp moisture sensors.  Moisture levels and pump activity are uploaded to a ThingSpeak.com dashboard for monitoring.

The sensors and relay board use the I2C protocol to communicate so you could expand this up to 100+ devices with appropriate power supply, relay boards and I2C multiplexors.

Give yourself ample lead time if ordering the items from Tindie.com as one of them comes from Latvia and the other comes from Lithuania.

Links below are NOT affiliate links.  I make no money if you choose to purchase these items.

Parts needed:
  1. Raspberry Pi Pico W
  3. Rain barrel with spigot
  4. 5-gallon bucket (for the reservoir)
  5. 4-channel I2C relay board from https://www.tindie.com/products/bugrovs2012/4-channel-i2c-electromagnetic-relay-module/
  6. 1/4" soaker tubing (https://www.amazon.com/dp/B000LNSX82)
  7. 12V motorized ball-valve (https://www.amazon.com/dp/B06X9LWXMW)
  8. 2 float switches for the reservoir (https://www.amazon.com/dp/B0B7WPBPBC)
  9. Voltage booster board (https://www.amazon.com/dp/B089JYBF25)
  10. Container/case for electronics (https://www.amazon.com/dp/B0000B12YQ)
  11. 5V power supply (https://www.amazon.com/dp/B0833WXT7F)
  12. Various wire, heat shrink tubing, tools and other accessories for connecting everything
  
For each plant:
  1. I2C moisture sensors https://www.tindie.com/products/miceuz/i2c-soil-moisture-sensor/
  2. 5-gallon bucket
  3. 5V DC pump (https://www.amazon.com/dp/B07BHD6KXS)

Notes:
  I DO stongly recommend that you buy the moisture sensors linked above.  They're a bit on the expensive side but I tried the cheap ones and they're just more trouble than they're worth.

  The motorized ball valve was more expensive than I'd hoped as well.  I first tried a solenoid and then a pump.  There is a reason that this project is labelled v2.

