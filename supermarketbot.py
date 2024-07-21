#________________________________________________________________________________________________
# Name   : G.N.K Lakshan
# Index  :21_ENG_031
# Reg no :EN102941
# ________________________________________________________________________________________________

import os
import random
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tkinter as tk
from tkinter import scrolledtext
from tkinter import font

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def preprocess(input_sentence):
    words = word_tokenize(input_sentence)
    pos_tags = pos_tag(words)
    return pos_tags

def recognize_intent(tokens):
    greeting_keywords = ['hello', 'hi', 'greetings', 'hey']
    exit_keywords = ['quit', 'exit', 'bye', 'goodbye', 'stop']
    negative_responses = ["no", "nope", "nah", "not really", "don't think so"]
    positive_responses = ["yess", "yep", "yer","yes"]
    tokens = [token.lower() for token, pos in tokens]

    if any(token in greeting_keywords for token in tokens):
        return "greeting"
    if any(token in exit_keywords for token in tokens):
        return "exit"
    if any(token in negative_responses for token in tokens):
        return "negative"
    if any(token in positive_responses for token in tokens):
        return "positive"

    return "list_goods"

def generate_response(intent):
    if intent == "greeting":
        return "Hello! How can I assist you today?"
    elif intent == "exit":
        return "Ok, have a nice day!"
    else:
        return "Please tell me the items you are looking for."

def extract_goods(tokens, goods_list):
    extracted_goods = []
    for token, pos in tokens:
        if pos in ['NN', 'NNS'] and token.lower() not in ['i', 'we', 'you', 'they']:
            token_lower = token.lower()
            matched_good = None
            for good in goods_list:
                if good == token_lower or token_lower in good:
                    matched_good = good
                    break
            if matched_good:
                extracted_goods.append(matched_good)
            else:
                extracted_goods.append((token_lower, "not available"))
    return extracted_goods

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

class SupermarketBot:
    negative_responses = ["no", "nope", "nah", "not really", "don't think so"]


    def __init__(self):
        self.random_questions = ["\nWhat can I help you find today?", "\nPlease tell me the items you are looking for:",
                                 "\nWhich goods are you searching for?"]
        self.continue_commands = ["\nDo you want to continue? (yes/no): ",
                                  "\nDo you have another item to find location?"]
        self.found_goods = {}
        self.unavailable_goods = []
        self.goods_locations_file = "data/goods_locations.json"
        self.goods_locations = self.load_goods_locations()

    def load_goods_locations(self):
        return load_data(self.goods_locations_file)

    def generate_pdf(self, name):
        if not self.found_goods and not self.unavailable_goods:
            return

        pdf_filename = os.path.join(os.getcwd(), f'{name}_goods_locations.pdf')
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title = Paragraph("Welcome to Lakshan Supermarket", styles['Title'])
        elements.append(title)

        subtitle = Paragraph("Here are the locations of the goods you requested:", styles['Heading3'])
        elements.append(subtitle)

        data = [["Item", "Location"]]
        for good, location in self.found_goods.items():
            data.append([good.capitalize(), location])
        for good in self.unavailable_goods:
            data.append([good.capitalize(), "Not Available"])

        table_width = doc.width - 40
        table = Table(data, colWidths=[table_width * 0.4, table_width * 0.6])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, 'BLACK'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        elements.append(table)

        elements.append(Paragraph("<br/><br/>", styles['Normal']))

        thank_you_message = "Thank you for using our chatbot service."
        centered_style = styles["Normal"]
        centered_style.alignment = 1
        elements.append(Paragraph(thank_you_message, centered_style))
        elements.append(Paragraph('Come again!', centered_style))

        doc.build(elements)

    def handle_input(self, tokens):
        intent = recognize_intent(tokens)
        if intent == "greeting":
            response = generate_response(intent)
            return response
        elif intent == "exit":
            return generate_response(intent)
        elif intent == "positive":
            return generate_response(intent)

        else:
            goods = extract_goods(tokens, list(self.goods_locations.keys()))
            return self.process_goods(goods)

    def process_goods(self, goods):
        responses = []
        for good in goods:
            responses.append(self.handle_good(good))
        return "\n".join(responses)

    def handle_good(self, good):
        if isinstance(good, tuple):
            good, status = good
            if status == "not available":
                self.unavailable_goods.append(good)
                return f"{good} - not available"

        good = good.lower().strip()
        if good in self.goods_locations:
            self.found_goods[good] = self.goods_locations[good]
            return f"{good.capitalize()} : {self.goods_locations[good]}"
        else:
            self.unavailable_goods.append(good)
            return f"{good} - not available"

class ChatApp:
    def __init__(self, root, bot):
        self.root = root
        self.bot = bot
        self.root.title("Chat Bot | Lakshan Supermarket ")

        # Customize fonts
        self.font = font.Font(family="Helvetica", size=12)
        self.bold_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Chat window with custom styling
        self.chat_window = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=self.font, bg="#f0f0f0", fg="#333333")
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_window.tag_config('human', foreground='blue', justify='left', font=self.bold_font)
        self.chat_window.tag_config('bot', foreground='black', justify='right', font=self.font)

        # Entry frame with custom styling
        self.entry_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.entry_frame.pack(fill=tk.X, padx=10, pady=5)

        self.entry_field = tk.Entry(self.entry_frame, font=self.font, bg="white", fg="#333333", relief=tk.FLAT)
        self.entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.send_button = tk.Button(self.entry_frame, text="Send", font=self.bold_font, bg="#4CAF50", fg="white", relief=tk.FLAT, command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        self.greet()

    def send_message(self):
        user_message = self.entry_field.get().strip()
        if user_message:
            self.display_message(user_message, 'human')
            self.entry_field.delete(0, tk.END)
            self.bot_response(user_message)

    def display_message(self, message, tag):
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, message + "\n", tag)
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.see(tk.END)

    def bot_response(self, user_message):
        tokens = preprocess(user_message)
        response = self.bot.handle_input(tokens)
        self.display_message(response, 'bot')

        intent = recognize_intent(tokens)
        if intent == "exit" or intent == "negative":
            self.handle_exit()
        elif intent == "list_goods":
            self.ask_continue()

    def greet(self):
        greeting_message = "Hello! I'm your Supermarket Bot. How can I assist you today?"
        self.display_message(greeting_message, 'bot')

    def ask_for_goods(self):
        question = random.choice(self.bot.continue_commands)  #random command
        self.display_message(question, 'bot')

    def ask_continue(self):
        continue_command = random.choice(self.bot.continue_commands)
        self.display_message("\n"+continue_command, 'bot')

    def handle_exit(self):
        self.bot.generate_pdf("user")
        self.display_message("Ok, have a nice day!\nPdf generated", 'bot')


if __name__ == "__main__":
    bot = SupermarketBot()
    root = tk.Tk()
    app = ChatApp(root, bot)
    root.mainloop()