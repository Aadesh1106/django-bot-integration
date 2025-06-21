import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
import django
django.setup()
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from django.conf import settings
from django.contrib.auth.models import User
from .models import TelegramUser
from api.models import UserProfile
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Setup command and message handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Store user information in database
        telegram_user, created = TelegramUser.objects.get_or_create(
            telegram_id=user.id,
            defaults={
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        )
        
        if created:
            # Try to link with existing Django user by username
            if user.username:
                try:
                    django_user = User.objects.get(username=user.username)
                    telegram_user.django_user = django_user
                    telegram_user.save()
                    
                    # Update user profile with telegram username
                    user_profile = UserProfile.objects.get(user=django_user)
                    user_profile.telegram_username = user.username
                    user_profile.save()
                    
                    welcome_message = f"""
🎉 Welcome back, {user.first_name}!

Your Telegram account has been linked to your existing Django account: @{django_user.username}

You can now receive notifications and updates through this bot.
                    """
                except User.DoesNotExist:
                    welcome_message = f"""
👋 Hello {user.first_name}!

Welcome to our Django API Bot! 

Your Telegram information has been saved:
- Username: @{user.username if user.username else 'Not set'}
- Telegram ID: {user.id}

To fully integrate with our API, please register at our website using the same username.
                    """
            else:
                welcome_message = f"""
👋 Hello {user.first_name}!

Welcome to our Django API Bot! 

Your Telegram information has been saved with ID: {user.id}

Please set a username in Telegram and use /start again for better integration.
                """
        else:
            welcome_message = f"""
👋 Welcome back, {user.first_name}!

You're already registered in our system.
Use /help to see available commands.
            """
        
        await update.message.reply_text(welcome_message)
        logger.info(f"User {user.id} ({user.username}) started the bot")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 Django API Bot Commands:

/start - Register your Telegram account
/help - Show this help message  
/stats - Show API statistics

📝 About this bot:
This bot is integrated with our Django REST API project and can store your Telegram information for future notifications and updates.

🔗 API Endpoints:
- Public: /api/public/
- Protected: /api/protected/ (requires authentication)

For more information, visit our API documentation.
        """
        await update.message.reply_text(help_text)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        try:
            total_users = User.objects.count()
            total_telegram_users = TelegramUser.objects.count()
            
            stats_text = f"""
📊 API Statistics:

👥 Total Django Users: {total_users}
📱 Total Telegram Users: {total_telegram_users}
🔗 Linked Accounts: {TelegramUser.objects.filter(django_user__isnull=False).count()}

📈 System Status: Online
🤖 Bot Status: Active
            """
            await update.message.reply_text(stats_text)
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            await update.message.reply_text("Sorry, couldn't fetch statistics right now.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        user = update.effective_user
        message_text = update.message.text
        
        # Log the message
        logger.info(f"Message from {user.username}: {message_text}")
        
        # Simple echo response
        response = f"Thanks for your message! You said: '{message_text}'\n\nUse /help to see available commands."
        await update.message.reply_text(response)

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")

    def run(self):
        """Run the bot"""
        self.application.add_error_handler(self.error_handler)
        logger.info("Starting Telegram bot...")
        self.application.run_polling()

# Function to run the bot
def run_telegram_bot():
    """Function to run the telegram bot"""
    bot = TelegramBot()
    bot.run()

if __name__ == '__main__':
    run_telegram_bot()