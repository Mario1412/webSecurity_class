# Chrome extension for detecting Tabnabbing Attacks
[toc] 
## Author
Tianhao Ma, AngeloOlcese

## Background
Based on the paper [TabShots: Client-Side Detection of Tabnabbing Attacks](https://www.securitee.org/files/tabnabbing_asiaccs2013.pdf), we implement a tabnabbing attacks detection tool

## How to run it
1. Use the chrome to open ```chrome://extensions```
2. Select ```Load unpacked``` and load the root directory of tabnabbing attacks detection tool

## How to use it
1. Navigate to any website and the detection tool will automatically and regularly take screenshots of the page.
2. Navigate back to the page, the detection tool capture a new screenshot and compare it with the existed screenshot.
3. There are three sign to signify the changes:
    - Blue sign(low change or no change): this sign have a threshold of 5% change
    - Yellow sign(medium change): this sign have a threshold of 30% change
    - Red sign(high change): this sign signify over %30 change
4. Click at the tabnabbing tool icon and check the specific change of the page, which is highlighted on red color. 

## Test case
http://www.azarask.in/blog/post/a-new-type-of-phishing-attack/