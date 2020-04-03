# Air Quality Index (AQI) Monitor
[![Open Source Love png2](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

> Measure air quality by measuring PM2.5 and PM10.

> PM2.5 refers to atmospheric particulate matter (PM) that have a diameter of less than 2.5 micrometers, which is about 3% the diameter of a human hair.  PM10 is particulate matter 10 micrometers or less in diameter.


<table>
<thead>
	<tr>
		<th>AQI</th>
		<th>PM : Human Hair Comparison</th>
	</tr>
</thead>
<tbody>
	<tr>
		<td><img src="https://miro.medium.com/max/2000/0*vzT6W-NevzPXAKls.png" width=400 align=center></td>
		<td><img src="https://www.epa.gov/sites/production/files/2016-09/pm2.5_scale_graphic-color_2.jpg" width=400 align=center></td>
	</tr>
</tbody>
</table>


## Requirements

### Hardware

<table>
<thead>
	<tr>
		<th><a href="https://www.amazon.com/CanaKit-Raspberry-Power-Supply-Listed/dp/B07BC6WH7V/ref=sr_1_3?crid=1UWQJWRZPS97T&dchild=1&keywords=raspberry+pi+3+b%2B&qid=1585869622&sprefix=rasp%2Caps%2C153&sr=8-3" target="_blank">Raspberry Pi 3 Model B+</a></th>
		<th><a href="https://www.amazon.com/gp/product/B07M9TP393/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1" target="_blank">WINGONEER PM Sensor SDS011</a></th>
	</tr>
</thead>
<tbody>
	<tr>
		<td><img src="https://cdn.sparkfun.com//assets/parts/1/2/8/2/8/14643-Raspberry_Pi_3_B_-05.jpg" width=400 align=center></td>
		<td><img src="https://images-na.ssl-images-amazon.com/images/I/61j%2BtLFRTQL._AC_SL1000_.jpg" width=400 align=center></td>
	</tr>
</tbody>
</table>

### Prototype build
![Prototype AQI Monitor](https://i.imgur.com/Hh3Xk6f.jpg)


### Software
#### Python3
> My preferred Python3 distribution is <a href="https://docs.conda.io/en/latest/miniconda.html" target="_blank">miniconda</a>)_

#### Python libraries
> All python requirements are defined in the **requirements.txt** file.  
*Instructions on how to install dependencies in the installation section.*

#### Streaming
> The two streaming services that I have configured are <a href="https://www.initialstate.com/" target="_blank">Initial State</a> and <a href="https://io.adafruit.com/" target="_blank">adafruit.io</a>.  There are many other options available, you will just need to make the necessary code modifications.

#### Alerting
> I like <a href="https://pushover.net/" target="_blank">Pushover</a> and this is the service I have configured in the code.  Again there are many other options available, you will just need to make the necessary code modifications.

## Installation
### Get the code from GitHub
```
git clone https://github.com/rbocchinfuso/aqi.git
```  
***Note: If you don't have Git installed you can also just grab the zip:***
```
https://github.com/rbocchinfuso/aqi/archive/master.zip
```
### Install the Python requirements
```sh
pip3 install -r requirements.txt
```

## Configuration
#### Copy the config.ini.example file to config.ini
#### Modify the config.ini file
```
[local]
# serial device interface
device = /dev/ttyUSB0
# cycle time in seconds
cycle_time = 10
# service options = initialstate | adafruitio | both
services = initialstate
# mode options = dev | prod
mode = dev

[initialstate]
is_bucket_name = xxxxxxxxxxxxxxxxxxxxxxx
is_bucket_key = xxxxxxxxxxxxxxxxxxxxxxx
is_access_key = xxxxxxxxxxxxxxxxxxxxxxx

[adafruit_io]
adafruitio_username = xxxxxxxxxxxxxxxxxxxxxxx
adafruitio_key = xxxxxxxxxxxxxxxxxxxxxxx
pmtwofive_feed = group.feed
pmten_feed = group.feed

[pushover]
api_token = xxxxxxxxxxxxxxxxxxxxxxx
user_key = xxxxxxxxxxxxxxxxxxxxxxx
```

#### Notes
- Assumed that the air sensor is addressable using the /dev/ttyUSB0 device file.  Adjust accordingly if it is at a addressable on a different device file.
- If you want to run aqi.py as a non-root user you will need to give the user access to the device file by executing: `sudo usermod -a -G dialout user`

## Usage example

```
python3 aqi.py
```
#### AQI in action
![AQI Running](https://imgur.com/9PpWukl.gif)


## Live feeds
- <a href="https://go.init.st/79kh78w" target="_blank">Initial State</a>
- <a href="https://io.adafruit.com/rbocchinfuso/dashboards/air-quality" target="_blank">adafruit.io</a>

## TODO
- Demonize the app or call from cron (TBD).
- Migrate build from my prototype Raspberry Pi configuration to an older spare Raspberry Pi B+ board for permanent deployment.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request ツ

## History
-  version 0.1 (initial release) - 2020/03/28


## Credits
- Rich Bocchinfuso – [@rbocchinfuso](https://twitter.com/rbochcinfuso) – <<rbocchinfuso@gmail.com>>
- Eden Bochinfuso - <<edenbocc@gmail.com>>

## License
MIT License

Copyright (c) [2020] [Richard J. Bocchinfuso]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
