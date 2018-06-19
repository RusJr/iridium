# Iridium

## Description
Iridium - selenium wrapper. The easiest way to write autotests 

## Installition
pip install iridium

## Example

```python
from iridium import ChromeBrowser
from iridium.actions import OpenPage, Sleep, Input, Click, Read, MakeScreen


my_script = [
    OpenPage('https://google.com'),
    Input('The best Python framework', '//*[@id="lst-ib"]'),
    Click('//*[@id="tsf"]/div[2]/div[3]/center/input[1]'),
    Read('//*[@id="fbar"]/div[1]/div/span'),
    MakeScreen(),
    Sleep(30),
]


if __name__ == '__main__':
    browser = ChromeBrowser(headless=False, logging_file='my_test.log')
    browser.execute(my_script, delay=0.1)
```
