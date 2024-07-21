# Supermarket Chatbot

The Supermarket Chatbot is designed to assist users in finding the location of goods within a supermarket. It uses Natural Language Processing (NLP) to understand your queries and provide accurate responses. The chatbot can handle various user intents, such as greetings, item searches, and exit commands. Additionally, it generates a PDF report of the items you searched for, indicating whether they are available or not.

## Project Directory

The project directory is organized as follows:

- **supermarketbot.py**: The main script that runs the chatbot.
- **data/goods_location_data.json**: JSON file contains the rack positions of various goods available in the supermarket.

## Features

- **Natural Language Understanding**: The chatbot can understand and respond to natural language inputs, making it easy for you to interact with it.
- **Item Location Search**: Provides the exact location of items within the supermarket.
- **PDF Report Generation**: Generates a PDF report listing the items found and their locations, as well as items that are not available.
- **Friendly Interaction**: Engages in a conversation with you, making the experience pleasant and user-friendly.

- ![image](https://github.com/user-attachments/assets/fe68c71e-fdd6-4244-b005-3900250539e4)
- ![image](https://github.com/user-attachments/assets/80a18716-3f17-4c8e-a285-55a4e5cb1cd9)



## Getting Started

To start using the Supermarket Chatbot, follow the instructions in the installation and usage sections below. This guide will walk you through setting up the chatbot, interacting with it, and generating your item location report.

## Installation

1. Install Python on your system.
2. Install the required libraries using the following command:
   ```bash
   pip install nltk reportlab
