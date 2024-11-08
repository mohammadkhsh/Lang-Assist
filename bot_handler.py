from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
from datetime import datetime
import os
import csv
import llm_responder

# Define states for conversation
ASK_NAME, ASK_AGE, ASK_TASK_SELECTION, ASK_TASK1_PHOTO, ASK_TASK1_QUESTION, ASK_TASK2_QUESTION, ASK_TASK1_ANSWER, ASK_TASK2_ANSWER = range(8)

# Paths for CSV file and image storage
CSV_FILE_PATH = "ielts_data.csv"
TASK1_IMAGE_PATH = "T1_images/"

# Function to check if user ID exists in CSV
def user_exists(user_id):
    with open(CSV_FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        return any(row[0] == str(user_id) for row in reader)

# Function to save user data to CSV
def save_to_csv(data):
    with open(CSV_FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Dummy LLM function for assessment
def dummy_llm_assessment(image_path, question, sample_answer):
    # Simulate assessment process; replace with actual LLM processing if available
    return f"Assessment result based on image at {image_path}, question '{question}', and sample answer."

# Start command to initiate the bot conversation
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    context.user_data["user_id"] = user_id

    if user_exists(user_id):
        await update.message.reply_text("Welcome back! Please enter your name:")
    else:
        await update.message.reply_text("Welcome to the IELTS Writing Review Bot!\nPlease enter your name:")
    
    return ASK_NAME

# Ask for age after receiving name if the user ID was new
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Thank you! Now, please enter your age:")
    return ASK_AGE

# Show buttons for task selection after receiving age
async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["age"] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Task 1", callback_data="1")],
        [InlineKeyboardButton("Task 2", callback_data="2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Would you like to assess Task 1 or Task 2?", reply_markup=reply_markup)
    return ASK_TASK_SELECTION

# Handle task selection based on button pressed
async def ask_task_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    selection = query.data

    if selection == "1":
        context.user_data["task_selection"] = "Task 1"
        await query.edit_message_text("You selected Task 1. Please upload the photo for Task 1 (e.g., process, chart, or graph):")
        return ASK_TASK1_PHOTO
    elif selection == "2":
        context.user_data["task_selection"] = "Task 2"
        await query.edit_message_text("You selected Task 2. Please enter the question for Task 2:")
        return ASK_TASK2_QUESTION

# Save Task 1 photo and proceed to ask for Task 1 question
async def ask_task1_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    photo = update.message.photo[-1]
    user_id = context.user_data["user_id"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    photo_path = f"{TASK1_IMAGE_PATH}{user_id}_exam_{timestamp}.jpg"
    
    # Corrected: Use download_to_drive method to save the image
    photo_file = await photo.get_file()
    await photo_file.download_to_drive(photo_path)
    context.user_data["task1_photo"] = photo_path

    await update.message.reply_text("Thank you! Now, please enter the question for Task 1:")
    return ASK_TASK1_QUESTION

# Ask for Task 1 answer after receiving Task 1 question
async def ask_task1_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["task1_question"] = update.message.text
    await update.message.reply_text("Great! Now, please provide your answer for Task 1:")
    return ASK_TASK1_ANSWER

# Ask for Task 2 answer after receiving Task 2 question
async def ask_task2_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["task2_question"] = update.message.text
    await update.message.reply_text("Thank you! Please provide your answer for Task 2:")
    return ASK_TASK2_ANSWER

# Task 1: Pass data to dummy LLM assessment function and send response
async def ask_task1_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["task1_answer"] = update.message.text

    # Dummy LLM assessment
    gen_resp, gram_resp, vocab_resp, TaskAchieve_resp  = dummy_llm_assessment(
        image_path=context.user_data.get("task1_photo", ""),
        question=context.user_data["task1_question"],
        sample_answer=context.user_data["task1_answer"]
    )
    await update.message.reply_text(f"GeneralAnalysis:\n{gen_resp}")
    await update.message.reply_text(f"Grammer Analysis:\n{gram_resp}")
    await update.message.reply_text(f"Vocabulary Analysis:\n{vocab_resp}")
    await update.message.reply_text(f"Task Achievement Analysis:\n{TaskAchieve_resp}")

    # Save to CSV
    save_to_csv([
        context.user_data["user_id"],
        context.user_data["name"],
        context.user_data["age"],
        context.user_data["task_selection"],
        context.user_data["task1_question"],
        "",
        context.user_data["task1_answer"],
        "",
        context.user_data.get("task1_photo", ""),
        gen_resp,
        gram_resp, 
        vocab_resp,
        TaskAchieve_resp,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])
    return ConversationHandler.END

# Task 2: Pass data to dummy LLM assessment function and send response
async def ask_task2_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["task2_answer"] = update.message.text

    # Dummy LLM assessment (no image required for Task 2)
    llm_response = dummy_llm_assessment(
        image_path="",
        question=context.user_data["task2_question"],
        sample_answer=context.user_data["task2_answer"]
    )

    await update.message.reply_text(f"Here is the assessment for Task 2:\n{llm_response}")

    # Save to CSV
    save_to_csv([
        context.user_data["user_id"],
        context.user_data["name"],
        context.user_data["age"],
        context.user_data["task_selection"],
        "",
        context.user_data["task2_question"],
        "",
        context.user_data["task2_answer"],
        "",
        llm_response,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])
    return ConversationHandler.END

# Command to cancel the process
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("The process has been canceled. Start again anytime by sending /start.")
    return ConversationHandler.END

# Main function to start the bot and define handlers
def main():
    if not os.path.exists(TASK1_IMAGE_PATH):
        os.makedirs(TASK1_IMAGE_PATH)

    application = Application.builder().token("8098374761:AAHWjVgO-3hksTftUK3iySl_wdIymyHEocs").build()

    # Set up the conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            ASK_TASK_SELECTION: [CallbackQueryHandler(ask_task_selection)],
            ASK_TASK1_PHOTO: [MessageHandler(filters.PHOTO, ask_task1_photo)],
            ASK_TASK1_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_task1_question)],
            ASK_TASK2_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_task2_question)],
            ASK_TASK1_ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_task1_answer)],
            ASK_TASK2_ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_task2_answer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()