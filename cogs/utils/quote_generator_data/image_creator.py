from os import path
import imgkit
import emoji


def give_emoji_free_text(text):
    return emoji.get_emoji_regexp().sub(r'', text)[:28]


dir_path = path.dirname(path.dirname(path.realpath(__file__)))


def create_image(user_name, user_avatar, message_content):
    options = {
        'format': 'png',
        'crop-w': '637',
        'encoding': "UTF-8",
        'enable-local-file-access': None
    }

    user_name = give_emoji_free_text(user_name)

    font_size = ""

    font_sizes = {
        60: 'x-large',
        100: 'large',
        150: 'small',
    }

    for fs in font_sizes.keys():
        if len(message_content) <= fs:
            font_size = font_sizes[fs]
            break

    html = f'''
            <html>
            <head>
            <style>
            @font-face {{
        font-family: 'Baline Script';
        src: url('{dir_path}/quote_generator_data/fonts/BalineScript.eot');
        src: url('{dir_path}/quote_generator_data/fonts/BalineScript.eot?#iefix') format('embedded-opentype'),
             url('{dir_path}/quote_generator_data/fonts/BalineScript.woff') format('woff'),
             url('{dir_path}/quote_generator_data/fonts/BalineScript.ttf') format('truetype'),
             url('{dir_path}/quote_generator_data/fonts/BalineScript.svg#BalineScript') format('svg');
        font-weight: normal;
        font-style: normal;
        font-display: swap;
    }}
        .myImage {{
            float: left;
            -webkit-filter: grayscale(100%); /* Safari 6.0 - 9.0 */
            filter: grayscale(100%);
            border: 2px solid white;
            border-right: 0;
            }}


            .quote {{
                float: left;
                width: 376px;
                height: 256px;
                margin-top: 0;
                margin-bottom: 0;
                background-color: #0c0c0c;
                border: 2px solid white;
                border-left: 0;

                text-align: center;
                }}

            .main-quote {{
            color: white;
            font-family: sans-serif;
            font-size: {font_size};
            font-style: italic;
            padding: 10% 5% 5%;
            }}

            .author {{
                color: white;
                font-size: 135%;
                font-family: Baline Script;
            }}

            span:after,
        span:before{{
            content:"\\00a0\\00a0\\00a0\\00a0\\00a0";
            text-decoration:line-through;
        }}

        body {{
            padding: 0;
            margin: 0;
        }}
            </style>
            </head>
            <body>
                <img src="{user_avatar}" class="myImage"/>
                <div class="quote">
                    <p class="main-quote">{message_content}</p>
                    <p class="author"><span> {user_name} </span></p>
                </div>
            </body>
            </html>
        '''

    img_path = f"{dir_path}/quote_generator_data/picture.png"
    imgkit.from_string(html, img_path, options=options)
    return img_path

# for testing
# name = give_emoji_free_text('Loxisito (^ω^)ﾉ♪')
# create_image(name,
#              'https://cdn.discordapp.com/avatars/196705465885786112/3e4665bf01e91d4569380c1ae4c811b1.png?size=256',
#              'Párale a tu pedo')


# font-family: 'Alex Brush';
#         src: url('{dir_path}/quote_generator_data/fonts/AlexBrush-Regular.eot');
#         src: url('{dir_path}/quote_generator_data/fonts/AlexBrush-Regular.eot?#iefix') format('embedded-opentype'),
#              url('{dir_path}/quote_generator_data/fonts/AlexBrush-Regular.woff') format('woff'),
#              url('{dir_path}/quote_generator_data/fonts/AlexBrush-Regular.ttf') format('truetype'),
#              url('{dir_path}/quote_generator_data/fonts/AlexBrush-Regular.svg#AlexBrush-Regular') format('svg');
#         font-weight: normal;
#         font-style: normal;
#         font-display: swap;