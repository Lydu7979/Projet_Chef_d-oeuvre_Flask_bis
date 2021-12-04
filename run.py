from tomatopredict import create_app
import config

app = create_app(config.Baseconfig)

if __name__ == '__main__':
    app.run(debug=True)