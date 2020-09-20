from webbot import Browser


def fetch_html(url, show_window=True, save=False):
    driver = Browser(showWindow=show_window)
    driver.go_to(url)
    driver.click('Login', tag='button', classname='inline-btn-2')
    driver.click(tag='input', classname='int-text', id='login-username1')
    driver.type('offers15816')
    driver.click(tag='input', classname='int-text', id='login-password1')
    driver.type('8simpsons8')
    driver.click('Login', tag='button', classname="inline-btn-2", number=3)
    driver.go_to(url)
    driver.scrolly(800)
    driver.click('0:0')
    html = driver.get_page_source()
    # driver.close_current_tab()
    if save:
        with open('test.html', "w") as file:
            file.write(html)

    return html


