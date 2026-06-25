"""
Telegram delivery module for Ethiopian Payroll Engine
Handles sending payslips via Telegram bot
"""
import os
import logging
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update  # Corrected import

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token - set via environment variable for security
TELEGRAM_BOT_TOKEN=os.getenv('TELEGRAM_BOT_TOKEN', '8385040050:AAH_vBRJLw0XVlZ0EJ4kl3lUdCvnWHxcMJ4')

def get_bot() -> Bot:
    """Get a Telegram bot instance"""
    return Bot(token=TELEGRAM_BOT_TOKEN)

async def send_telegram_message(telegram_id: str, message: str) -> bool:
    """
    Send a message to a Telegram user
    
    Args:
        telegram_id: The user's Telegram ID or username (without @)
        message: The message to send
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        bot = get_bot()
        # Clean the telegram_id - remove @ if present
        clean_id = telegram_id.lstrip('@')
        
        # Send message
        await bot.send_message(chat_id=clean_id, text=message, parse_mode='HTML')
        logger.info(f"Message sent to Telegram user {clean_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send Telegram message to {telegram_id}: {str(e)}")
        return False

async def send_payslip_via_telegram(telegram_id: str, employee_name: str, payslip_url: str, pay_period: str) -> bool:
    """
    Send a payslip notification via Telegram
    
    Args:
        telegram_id: Employee's Telegram ID/username
        employee_name: Employee's full name
        payslip_url: URL where the payslip can be downloaded
        pay_period: e.g., "June 2026"
    
    Returns:
        bool: True if sent successfully
    """
    try:
        message = f"""
<b>💰 Your Payslip is Ready!</b>

Hello {employee_name},

Your payslip for {pay_period} is now available for download.

📥 <a href="{payslip_url}">Click here to download your payslip</a>

This is an automated message from Ethiopian Payroll Engine.
        """.strip()
        
        return await send_telegram_message(telegram_id, message)
    except Exception as e:
        logger.error(f"Error sending payslip via Telegram: {str(e)}")
        return False

def send_payslip_notification_sync(telegram_id: str, employee_name: str, payslip_url: str, pay_period: str) -> bool:
    """
    Synchronous wrapper for sending payslip notification
    (for use in Flask routes where we can't use async/await directly)
    """
    import asyncio
    try:
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            send_payslip_via_telegram(telegram_id, employee_name, payslip_url, pay_period)
        )
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Error in sync Telegram send: {str(e)}")
        return False

# Optional: Simple command handler for testing
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! "
        f"I am the Ethiopian Payroll Engine bot. "
        f"I will send you payslip notifications when your employer processes payroll."
    )

def setup_bot_handlers(application: Application) -> None:
    """Set up command handlers for the bot"""
    application.add_handler(CommandHandler("start", start_command))
    # Add more handlers as needed

if __name__ == "__main__":
    # For testing the bot directly
    import asyncio
    
    async def test():
        # Test sending a message
        result = await send_telegram_message("your_test_telegram_id", "Test message from Ethiopian Payroll Engine")
        print(f"Test message sent: {result}")
    
    # asyncio.run(test())
    print("Telegram module loaded. Configure TELEGRAM_BOT_TOKEN environment variable.")