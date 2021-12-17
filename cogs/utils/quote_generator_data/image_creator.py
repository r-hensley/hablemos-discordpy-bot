from os import path
import imgkit

dir_path = path.dirname(path.dirname(path.realpath(__file__)))


def create_image(user_name, user_avatar, message_content):
    options = {
        'format': 'png',
        'crop-w': '639',
        'encoding': "UTF-8",
        'enable-local-file-access': None
    }

    font_size = ""

    font_sizes = {
        60: 'x-large',
        100: 'large',
        150: 'medium',
    }

    for fs in font_sizes:
        if len(message_content) <= fs:
            font_size = font_sizes[fs]
            break

    html = f'''
            <html>
            <head>
            <style>   
        @font-face {{
        font-family: 'Satisfy Pro';
        src: url('{dir_path}/quote_generator_data/fonts/SatisfyPro.eot');
        src: url('{dir_path}/quote_generator_data/fonts/SatisfyPro.eot?#iefix') format('embedded-opentype'),
             url('{dir_path}/quote_generator_data/fonts/SatisfyPro.woff') format('woff'),
             url('{dir_path}/quote_generator_data/fonts/SatisfyPro.ttf') format('truetype'),
             url('{dir_path}/quote_generator_data/fonts/SatisfyPro.svg#SatisfyPro') format('svg');
        font-weight: normal;
        font-style: normal;
        font-display: swap;
    }}
    
    @font-face {{
        font-family: 'Helvetica Neue';
        src: url('{dir_path}/quote_generator_data/fonts/HelveticaNeue-Roman.eot');
        src: url('{dir_path}/quote_generator_data/fonts/HelveticaNeue-Roman.eot?#iefix') format('embedded-opentype'),
             url('{dir_path}/quote_generator_data/fonts/HelveticaNeue-Roman.woff') format('woff'),
             url('{dir_path}/quote_generator_data/fonts/HelveticaNeue-Roman.ttf') format('truetype'),
             url('{dir_path}/quote_generator_data/fonts/HelveticaNeue-Roman.svg#HelveticaNeue-Roman') format('svg');
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
            width: 258px;
            height: 256px;
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
            font-family: Helvetica Neue;
            font-size: {font_size};
            padding: 10% 5% 5%;
            }}

            .author {{
                color: white;
                font-size: 135%;
                font-family: Satisfy Pro;
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
# create_image('Priúñaku',
#              'https://cdn.discordapp.com/avatars/463728003038576640/fc146df4c3096017d93f26511a6d1798.png?size=256',
#              'These hées ñare dusty')



