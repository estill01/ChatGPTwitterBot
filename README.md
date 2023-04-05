# GPTwitterBot 🤖 🐦
Welcome to GPTwitterBot! This bot auto-engages the twitterverse to maximize engagement. 

Worried about the cost of running the bot? Well don't! GPTwitterBot comes with a built-in Budget Tracker to limit its expenditures on API usage. 🎉

## Features
- 😇 Automatically engages with mentions and replies on Twitter
- 🧠 Generates responses using cutting-edge OpenAI GPT models
- 💸 Integrated Budget Tracker works to ensure you don't blast all your money (though, if you do that's on you. No warranty!)
- 🔧 Easily extendable to support additional functionality

## Prerequisites
To get this bot up and running, you'll need:

- Python 3.6+
- Twitter API credentials
- OpenAI API key


## Installation
To set up the ChatGPTwitterBot project using poetry, follow these steps:

1. Make sure you have python and poetry installed on your system. If you don't have poetry installed, you can follow the official installation guide.

2. Clone the repository:
```
git clone https://github.com/yourusername/ChatGPTwitterBot.git
```

3. Change into the project directory:
```
cd ChatGPTwitterBot
```

4. Install the dependencies using poetry:
```
poetry install
```

5. Activate the virtual environment created by poetry:
```
poetry shell
```

6. Set up the required environment variables. You can either set them directly in your terminal session, or you can create a .env file in the project directory with the following contents:
```
TWITTER_API_KEY=<your_twitter_api_key>
TWITTER_API_SECRET_KEY=<your_twitter_api_secret_key>
TWITTER_ACCESS_TOKEN=<your_twitter_access_token>
TWITTER_ACCESS_TOKEN_SECRET=<your_twitter_access_token_secret>
OPENAI_API_KEY=<your_openai_api_key>
```
Replace `<your_twitter_api_key>`, `<your_twitter_api_secret_key>`, `<your_twitter_access_token>`, `<your_twitter_access_token_secret>`, and `<your_openai_api_key>` with your actual API keys and access tokens.

7. You're all set! Now you can run the ChatGPTwitterBot by executing the main script, or you can import the module into your own Python project.


## Running the ChatGPTwitterBot
To run the ChatGPTwitterBot as a standalone application, follow these steps:

1. Make sure you have completed the installation steps mentioned in the previous section.

2. Run the main script, which starts the Twitter stream listener:
```
python main.py
```

3. The bot is now running and will automatically reply to tweets mentioning its handle according to its budget. 🚀

## Including ChatGPTwitterBot as a Module in Your Project
If you'd like to include the ChatGPTwitterBot in your own Python project, follow these steps:

1. Make sure you have completed the installation steps mentioned in the "Installation" section.

2. Import the ChatGPTwitterBot module in your Python script:
```
from chatgptwitterbot import TwitterBot, TwitterBotStreamListener, BudgetTracker, Pricing
```

3. Create an instance of the TwitterBot class, passing in the necessary arguments, such as budget, pricing, Twitter handle, and models:
```
twitter_bot = TwitterBot(initial_budget, chosen_pricing, handle, models)
```

4. Create an instance of the TwitterBotStreamListener class and pass in the TwitterBot instance:
```
stream_listener = TwitterBotStreamListener(api, twitter_bot)
```

5. Set up the Tweepy stream with the stream listener:
```
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
```

6. Start the Tweepy stream, filtering tweets mentioning the TwitterBot handle:
```
stream.filter(track=[handle], is_async=True)
```

7. The ChatGPTwitterBot is now integrated into your project and will respond to tweets as configured. You can use the various classes and methods provided by the module to customize its behavior as needed.


## Extending Functionality
To add new features or modify existing functionality, edit the corresponding Python files in the src directory:

`config.py`: Configuration and environment variable loading

`pricing.py`: OpenAI API pricing data and Pricing class

`budget_tracker.py`: Budget tracking and cost calculation with the BudgetTracker class

`twitter_bot.py`: Main functionality of the Twitter bot with the TwitterBot and TwitterBotStreamListener classes

## Contributing
Feel free to submit pull requests, report issues, or suggest new features. All ideas are welcome! 🙌

## License
This project is licensed under the MIT License. See the LICENSE file for details.


