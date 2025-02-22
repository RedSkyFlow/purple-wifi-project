import os
from flask import Blueprint, render_template, request, redirect, url_for, send_file
from PIL import Image
import colorgram
import requests
from bs4 import BeautifulSoup
from jinja2 import Template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('base.html')

@main.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            # Ensure the uploads directory exists
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            image_path = os.path.join('uploads', image.filename)
            image.save(image_path)
            colors = extract_colors_from_image(image_path)
            generate_html(colors)
            return send_file(os.path.join(os.getcwd(), 'output.html'))
    elif 'url' in request.form:
        url = request.form['url']
        if url != '':
            colors = extract_colors_from_website(url)
            generate_html(colors)
            return send_file(os.path.join(os.getcwd(), 'output.html'))
    return redirect(url_for('main.index'))

def extract_colors_from_image(image_path):
    image = Image.open(image_path)
    colors = colorgram.extract(image, 6)
    # Convert colors to CSS format
    css_colors = [f"rgb({color.rgb.r}, {color.rgb.g}, {color.rgb.b})" for color in colors]
    return css_colors

def extract_colors_from_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Placeholder logic to extract colors from the website
    # Replace this with actual color extraction logic
    colors = ['#ffffff', '#000000']  # Example colors
    return colors

def generate_html(colors):
    template = Template('''
    <!DOCTYPE html>
    <!--[if lt IE 9]><html class="lte-ie8"><![endif]-->
    <!--[if lte IE 9 ]><html class="ie9down"> <![endif]-->
    <!--[if IE 9 ]><html class="ie9"> <![endif]-->
    <!--[if (gt IE 9)|!(IE)]><!--><html lang="en"><!--<![endif]-->
    <html class="no-js" lang="">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <title>Chicago Cafe WiFi</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        [[!GoogleFont &font=`Roboto`]]
        <style>
            body {
                background-color: {{ colors[0] }};
                color: {{ colors[1] }};
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 20px;
            }
            .header-logo {
                background-color: {{ colors[2] }};
            }
            .cta-button {
                background-color: {{ colors[1] }};
                color: {{ colors[0] }};
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                font-size: 16px;
                margin-top: 20px;
            }
            .cta-button:hover {
                background-color: {{ colors[3] }};
            }
        </style>
    </head>
    <body>
        [[!Spinner]]
        <div class="page-wrapper">
            <section class="header-logo">
                <div class="content-wrapper">
                    <div class="logo-container">
                        <img src="[[!ImageUrl &id=`chicago-cafe-logo.png`]]" alt="">
                    </div>
                </div>
            </section>
            <section class="login-form">
                <div class="content-wrapper">
                    <p>Login to our WiFi with social media</p>
                    <div class="social-login-buttons cf">
                        <a href="#" [[!FacebookAuthAttr]]><img src="[[!ImageUrl &id=`facebook-btn.png`]]"></a>
                        <a href="#" [[!XAuthAttr]]><img src="[[!ImageUrl &id=`x-btn.png`]]"></a>
                        <a href="#" [[!AppleAuthAttr]]><img src="[[!ImageUrl &id=`apple-btn.png`]]"></a>
                    </div>
                    <p>Or login with our <a href="#" [[!RegistrationFormAuthAttr]]>form</a>. Already <a id="btn-login" href="#">registered?</a></p>
                    <div class="login-form-container cf">
                        [[!LoginForm]]
                    </div>
                </div>
            </section>
            <section class="language-switcher cf">
                <div class="content-wrapper">
                    <form>
                        <div class="form-field switch-language">
                            <label>Set Language</label>
                            [[!SelectLanguage]]
                        </div>
                    </form>
                </div>
            </section>
        </div>
        [[!PoweredBy]]
    </body>
    </html>
    ''')
    html_content = template.render(colors=colors)
    output_path = os.path.join(os.getcwd(), 'output.html')
    with open(output_path, 'w') as f:
        f.write(html_content)