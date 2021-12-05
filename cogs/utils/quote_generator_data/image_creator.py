from os import path
from htmlwebshot import WebShot, Config

dir_path = path.dirname(path.dirname(path.realpath(__file__)))


def create_image(user_name, user_avatar, message_content):
    shot = WebShot()
    # shot.config = Config(wkhtmltopdf="/app/bin/wkhtmltopdf")
    shot.quality = 100
    shot.params = {"--crop-h": 266, "--crop-w": 637, "--encoding": "utf-8"}
    font_size = ""
    print("I reached here")
    print(shot)
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
            <img src="{user_avatar}" class="myImage"/>
            <div class="quote">
                <p class="main-quote">{message_content}</p>
                <p class="author"><span> {user_name} </span></p>
            </div>
    '''
    css = f'''
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
        color: antiquewhite;
        font-family: sans-serif;
        font-size: {font_size};
        font-style: italic;
        padding: 10% 5% 5%;
      }}

      .author {{
          color: antiquewhite;
          font-size: larger;
          font-family: cursive;
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

    '''

    img_path = f"{dir_path}/quote_generator_data/picture.png"
    shot.create_pic(html=html, css=css, output=img_path)
    print("Here too")
    return img_path
