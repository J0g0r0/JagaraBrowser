def translate_page(tab, target_lang='id'):
    url = tab.url().toString()
    translate_url = f"https://translate.google.com/translate?hl={target_lang}&sl=auto&tl={target_lang}&u={url}"
    tab.navigate(translate_url)