# Iridium

## Description
Iridium - selenium wrapper. The easiest way to write autotests 

## Installition
pip install iridium

## Example

```python
from iridium import ChromeBrowser
from iridium.actions import OpenPage, Sleep, Input, Click, Read, MakeScreen, Exists


list_script = [
    OpenPage('https://google.com'),
    Input('The best Python framework', '//*[@id="lst-ib"]'),
    Click('//*[@id="tsf"]/div[2]/div[3]/center/input[1]'),
    MakeScreen(),
]


def function_script(bro: ChromeBrowser):
    element_exists = bro.run(Exists('//*[@id="fbar"]/div[1]/div/span'))
    if element_exists:
        text = bro.run(Read('//*[@id="fbar"]/div[1]/div/span'))
        print('Your country is', text)
    bro.run(Sleep(3))


if __name__ == '__main__':
    browser = ChromeBrowser(headless=True, logging_file='example.log')
    browser.execute(list_script, delay=0.05)
    function_script(browser)

```
