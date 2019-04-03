from flask import Flask, url_for, request, render_template
from flask import Markup
import parser

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html', style_css=style_css)


@app.route('/temp')
def temp():
    selector = request.args['selector']
    link = request.args['css-text']
    text = ''

    try:
        css_parser = parser.CSSParser(link)
        styles = css_parser.search_selector(selector)

        text += '<div class="common">'
        for item in styles[0]:
            text += f'<span class="selector">{item.selectorText}' + ' {<br></span>'
            text += f'<span class="cssText">{item.style.cssText}' + '</span>'
            text += '<span class="selector">}</span><br>'
        text += '</div>'

        text += '<div class="media">'
        for key, value in styles[1].items():
            text += '<span class="selector">@media {} {}'.format(key, ' {</span>')
            for rule in value:
                text += f'<span class="s selector">{rule.selectorText}' + ' {</span>'
                text += f'<span class="cssText">{rule.style.cssText}' + '</span>'
                text += '<span class="s selector">}</span><br>'
            text += '<span class="selector">}</span><br><script>alert("eee");</script>'
        text += '</div>'

        text = text.replace('\n', '<br>').replace(', .', ',<br>.')
    except Exception as err:
        text = '<div class="media"><span class="selector">Что-то сломалось :('
        text += f'<br>{err}</span></div>'

    text = Markup(text)
    return render_template('temp.html', style_css=style_css, text=text)


with app.test_request_context():
    style_css = url_for('static', filename='style.css')


if __name__ == '__main__':
    app.run(debug=True)
